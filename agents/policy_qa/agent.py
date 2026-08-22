import uuid
import re
from typing import Dict, Any, List
from datetime import datetime
from pydantic import ValidationError
from groq import Groq

from schemas import (
    PolicyQuestionRequest,
    PolicyQAResponse,
    PolicySource,
    PolicySection,
    PolicySearchResult
)
from tools import (
    search_policy,
    get_policy_section,
    ToolError,
    PermissionError
)
from audit import log_action
from config import get_groq_api_key, get_model_name, get_relevance_threshold

ACTION_PATTERNS = [
    r"\b(approve|reject|apply for|cancel|submit|modify|update|change|delete|create)\b.*\b(leave|attendance|salary|profile|role|request|record|time)\b",
    r"\b(change|update|reset)\s+(my\s+)?(password|salary|role|designation|profile)\b",
    r"\b(approve|reject)\s+(my\s+)?leave\b"
]

PERSONAL_DATA_PATTERNS = [
    r"\bwhat\s+is\s+my\s+(salary|pay|compensation|bank\s+account|leave\s+balance|password)\b",
    r"\bhow\s+much\s+is\s+my\s+(salary|bonus|pay)\b",
    r"\bshow\s+me\s+.*\s+(salary|attendance|record|profile)\b",
    r"\bwho\s+is\s+the\s+ceo\b",
    r"\bwhat\s+is\s+the\s+weather\b"
]

def run_policy_qa(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entrypoint for the Policy Q&A Agent.
    Accepts a dictionary or PolicyQuestionRequest and returns a validated PolicyQAResponse dictionary.
    """
    execution_id = str(uuid.uuid4())
    warnings: List[str] = []

    # 1. Validate Input Request
    try:
        if isinstance(request_data, PolicyQuestionRequest):
            req = request_data
        else:
            req = PolicyQuestionRequest(**request_data)
    except ValidationError as e:
        err_msg = f"Request validation failed: {str(e)}"
        log_action(
            request_id=request_data.get("request_id", execution_id) if isinstance(request_data, dict) else execution_id,
            agent_name="Policy Q&A Agent",
            action_type="validation_error",
            tool_called="N/A",
            tool_result="failed",
            details=err_msg
        )
        return _build_response(
            request_id=request_data.get("request_id", execution_id) if isinstance(request_data, dict) else execution_id,
            execution_id=execution_id,
            success=False,
            answer="Invalid request format or parameters. Please ensure all required fields are provided correctly.",
            sources=[],
            confidence="LOW",
            ask_hr=True,
            reasoning_summary="Input failed schema validation.",
            warnings=[err_msg]
        )

    log_action(
        request_id=req.request_id,
        agent_name="Policy Q&A Agent",
        action_type="start_query",
        tool_called="N/A",
        tool_result="success",
        details=f"Received policy question from user '{req.user_id}', employee '{req.employee_id}': '{req.question}'"
    )

    question_lower = req.question.lower().strip()

    # 2. Check for Action Requests (Prohibited for Read-Only Agent)
    for pattern in ACTION_PATTERNS:
        if re.search(pattern, question_lower):
            warning = "Prohibited action request detected."
            warnings.append(warning)
            refusal_msg = (
                "I am a read-only Policy Q&A assistant and cannot perform actions such as applying, "
                "updating, or approving leaves or attendance records. Please submit action requests "
                "directly through the appropriate portal in Dayflow HRMS."
            )
            log_action(
                request_id=req.request_id,
                agent_name="Policy Q&A Agent",
                action_type="refusal",
                tool_called="N/A",
                tool_result="blocked",
                details=f"Refused action request: '{req.question}'"
            )
            return _build_response(
                request_id=req.request_id,
                execution_id=execution_id,
                success=True,
                answer=refusal_msg,
                sources=[],
                confidence="LOW",
                ask_hr=True,
                reasoning_summary="The query requested an operational action which is outside the scope of a read-only policy agent.",
                warnings=warnings
            )

    # 3. Check for Personal/PII or Out-of-Scope Requests
    for pattern in PERSONAL_DATA_PATTERNS:
        if re.search(pattern, question_lower):
            warning = "Personal data or out-of-scope question requested."
            warnings.append(warning)
            refusal_msg = (
                "I cannot access private employee records, individual salary details, or unindexed "
                "corporate information. For specific personal inquiries or individual payroll details, "
                "please check your employee portal or contact HR directly."
            )
            log_action(
                request_id=req.request_id,
                agent_name="Policy Q&A Agent",
                action_type="refusal",
                tool_called="N/A",
                tool_result="blocked",
                details=f"Refused private/out-of-scope query: '{req.question}'"
            )
            return _build_response(
                request_id=req.request_id,
                execution_id=execution_id,
                success=True,
                answer=refusal_msg,
                sources=[],
                confidence="LOW",
                ask_hr=True,
                reasoning_summary="The query requested personal or out-of-scope data not available in the public policy knowledge base.",
                warnings=warnings
            )

    # 4. Search Policy Knowledge Base
    try:
        search_results: List[PolicySearchResult] = search_policy(req.question, req.request_id)
    except ToolError as e:
        warnings.append(f"Tool error during policy search: {str(e)}")
        return _build_response(
            request_id=req.request_id,
            execution_id=execution_id,
            success=False,
            answer="An error occurred while accessing the policy knowledge base. Please contact HR directly for assistance.",
            sources=[],
            confidence="LOW",
            ask_hr=True,
            reasoning_summary="Policy search tool failed to retrieve records.",
            warnings=warnings
        )
    except Exception as e:
        warnings.append(f"Unexpected error: {str(e)}")
        return _build_response(
            request_id=req.request_id,
            execution_id=execution_id,
            success=False,
            answer="A system error occurred. Please contact HR for clarification.",
            sources=[],
            confidence="LOW",
            ask_hr=True,
            reasoning_summary="An unexpected exception occurred during policy search.",
            warnings=warnings
        )

    # 5. Evaluate Search Results
    threshold = get_relevance_threshold()
    relevant_results = [r for r in search_results if r.score >= threshold]

    if not relevant_results:
        log_action(
            request_id=req.request_id,
            agent_name="Policy Q&A Agent",
            action_type="no_match",
            tool_called="search_policy",
            tool_result="empty",
            details="No relevant policy sections matched the query."
        )
        return _build_response(
            request_id=req.request_id,
            execution_id=execution_id,
            success=True,
            answer="I could not find sufficient information in the available HR policies to answer this question accurately. Please contact HR for clarification.",
            sources=[],
            confidence="LOW",
            ask_hr=True,
            reasoning_summary="No policy sections in the knowledge base met the minimum relevance threshold for the given query.",
            warnings=warnings
        )

    # Retrieve full section details for top matches
    top_results = relevant_results[:3]
    sections: List[PolicySection] = []
    sources: List[PolicySource] = []

    for r in top_results:
        try:
            sec = get_policy_section(r.policy_name, r.section, req.request_id)
            sections.append(sec)
            sources.append(PolicySource(
                policy_name=sec.policy_name,
                section=sec.section,
                title=sec.title
            ))
        except ToolError as e:
            warnings.append(f"Failed to retrieve full section {r.policy_name} {r.section}: {str(e)}")

    if not sections:
        return _build_response(
            request_id=req.request_id,
            execution_id=execution_id,
            success=False,
            answer="Could not retrieve matching policy section details. Please contact HR.",
            sources=[],
            confidence="LOW",
            ask_hr=True,
            reasoning_summary="Matching policy sections could not be fetched from the database.",
            warnings=warnings
        )

    # 6. Check for Ambiguity / Confidence Level
    top_score = top_results[0].score
    clean_tokens = [w for w in re.sub(r'[^\w\s]', ' ', question_lower).split() if len(w) > 1]
    
    # If query is short/broad (<= 4 words) or weak score match
    is_ambiguous = len(clean_tokens) <= 4 or top_score < 3.0

    if is_ambiguous:
        confidence = "MEDIUM"
        ask_hr = True
    elif top_score >= 3.0:
        confidence = "HIGH"
        ask_hr = False
    else:
        confidence = "MEDIUM"
        ask_hr = True

    # 7. Generate Answer (Using LLM or Deterministic Fallback)
    answer = _synthesize_answer(req.question, sections, confidence)
    
    # Build citation explanation in reasoning
    source_labels = [f"{s.policy_name} Section {s.section} ({s.title})" for s in sources]
    reasoning_summary = f"The answer was directly supported by {', '.join(source_labels)}."
    if is_ambiguous:
        reasoning_summary += " The question was broad, so HR consultation is recommended for specific scenarios."

    log_action(
        request_id=req.request_id,
        agent_name="Policy Q&A Agent",
        action_type="answer_generated",
        tool_called="N/A",
        tool_result="success",
        details=f"Generated answer with confidence {confidence} citing {len(sources)} sources."
    )

    return _build_response(
        request_id=req.request_id,
        execution_id=execution_id,
        success=True,
        answer=answer,
        sources=sources,
        confidence=confidence,
        ask_hr=ask_hr,
        reasoning_summary=reasoning_summary,
        warnings=warnings
    )

def _synthesize_answer(question: str, sections: List[PolicySection], confidence: str) -> str:
    """Generate a clean answer using Groq LLM if configured, or deterministic fallback."""
    api_key = get_groq_api_key()
    
    if api_key and api_key != "mock":
        try:
            client = Groq(api_key=api_key)
            context = "\n\n".join([
                f"Policy: {s.policy_name}\nSection {s.section}: {s.title}\nContent: {s.content}"
                for s in sections
            ])
            prompt = (
                "You are the Dayflow HRMS Policy Q&A Agent. Answer the employee's question strictly "
                "using the provided policy context below. Do not invent any rules, numbers, or facts. "
                "Keep the answer clear, professional, and concise. Mention the specific policy name and section.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {question}\n\n"
                "Answer:"
            )
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=get_model_name(),
                temperature=0.0
            )
            llm_text = completion.choices[0].message.content.strip()
            if llm_text:
                return llm_text
        except Exception:
            # Fall back safely to deterministic generation on any LLM failure
            pass

    # Deterministic Fallback Generation
    if len(sections) == 1:
        sec = sections[0]
        return f"According to {sec.policy_name} Section {sec.section} ({sec.title}): {sec.content}"
    else:
        parts = [f"- According to {s.policy_name} Section {s.section} ({s.title}): {s.content}" for s in sections]
        return "Here is the relevant policy information:\n" + "\n".join(parts)

def _build_response(
    request_id: str,
    execution_id: str,
    success: bool,
    answer: str,
    sources: List[PolicySource],
    confidence: str,
    ask_hr: bool,
    reasoning_summary: str,
    warnings: List[str]
) -> Dict[str, Any]:
    """Helper to build and validate a PolicyQAResponse model dump."""
    res = PolicyQAResponse(
        request_id=request_id,
        agent_name="Policy Q&A Agent",
        success=success,
        answer=answer,
        sources=sources,
        confidence=confidence,  # type: ignore
        ask_hr=ask_hr,
        reasoning_summary=reasoning_summary,
        warnings=warnings,
        audit_id=execution_id
    )
    return res.model_dump(mode='json')
