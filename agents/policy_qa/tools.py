import re
from typing import List, Dict, Any, Optional
from schemas import PolicySearchResult, PolicySection
from mock_data import MOCK_POLICY_DATABASE
from audit import log_action
from permissions import check_permission

STOP_WORDS = {
    "what", "is", "the", "a", "an", "company", "policy", "policies", "regarding",
    "for", "and", "with", "are", "can", "you", "please", "tell", "about", "how",
    "much", "many", "does", "do", "any", "our", "my", "all", "per", "from", "when",
    "where", "who", "which", "why", "guidelines", "procedure", "procedures",
    "information", "details", "dayflow", "employees", "employee", "rules", "rule"
}

class ToolError(Exception):
    """Raised when a tool encounters an operational failure."""
    pass

class PermissionError(Exception):
    """Raised when an unauthorized tool is invoked."""
    pass

def _verify_permission(tool_name: str, request_id: str):
    """Enforces least-privilege tool execution permissions."""
    if not check_permission(tool_name):
        log_action(
            request_id=request_id,
            agent_name="Policy Q&A Agent",
            action_type="permission_denied",
            tool_called=tool_name,
            tool_result="failed",
            details=f"Execution of prohibited tool '{tool_name}' was blocked by policy."
        )
        raise PermissionError(f"Access to '{tool_name}' is denied: prohibited for Policy Q&A Agent.")

def _word_in_text(phrase: str, text: str) -> bool:
    """Exact word boundary match."""
    pattern = r'\b' + re.escape(phrase.lower()) + r'\b'
    return bool(re.search(pattern, text.lower()))

def search_policy(query: str, request_id: str) -> List[PolicySearchResult]:
    """
    Search the policy knowledge base using exact keyword and substantive token matching.
    """
    _verify_permission("search_policy", request_id)
    
    if query == "FORCE_TOOL_FAILURE":
        log_action(request_id, "Policy Q&A Agent", "tool_call", "search_policy", "failure", "Simulated tool failure occurred.")
        raise ToolError("Policy search service is currently unavailable.")

    clean_query = re.sub(r'[^\w\s]', ' ', query.lower())
    query_tokens = [w for w in clean_query.split() if len(w) > 1]
    substantive_tokens = set([w for w in query_tokens if w not in STOP_WORDS])

    results: List[PolicySearchResult] = []

    for policy_name, policy_data in MOCK_POLICY_DATABASE.items():
        for sec_id, sec_data in policy_data.get("sections", {}).items():
            title = sec_data.get("title", "")
            content = sec_data.get("content", "")
            keywords = sec_data.get("keywords", [])

            searchable_text = f"{policy_name.lower()} {title.lower()} {content.lower()} {' '.join(keywords).lower()}"
            
            score = 0.0
            matched_keywords_count = 0

            # 1. Exact phrase / keyword matching with word boundaries
            for kw in keywords:
                if _word_in_text(kw, clean_query):
                    score += 3.0
                    matched_keywords_count += 1

            # 2. Substantive query token matching
            if substantive_tokens:
                matched_substantive = [tok for tok in substantive_tokens if _word_in_text(tok, searchable_text)]
                coverage = len(matched_substantive) / len(substantive_tokens)
                
                # Boost if substantive coverage is high
                if coverage >= 0.3:
                    score += coverage * 3.0
                elif matched_keywords_count == 0:
                    # If very low token coverage and no domain keywords matched, do not match
                    score = 0.0
            elif query_tokens:
                # Query has only generic words (e.g. "What are the rules?")
                score = 0.5

            if score >= 2.0:
                snippet = content if len(content) <= 160 else content[:157] + "..."
                results.append(PolicySearchResult(
                    policy_name=policy_name,
                    section=sec_id,
                    title=title,
                    snippet=snippet,
                    score=round(score, 2)
                ))

    # Sort descending by score
    results.sort(key=lambda r: r.score, reverse=True)

    log_action(
        request_id=request_id,
        agent_name="Policy Q&A Agent",
        action_type="tool_call",
        tool_called="search_policy",
        tool_result="success",
        details=f"Searched policy DB for query '{query}'. Found {len(results)} matching sections."
    )

    return results

def get_policy_section(policy_name: str, section: str, request_id: str) -> PolicySection:
    """
    Retrieve the full text and metadata of a specific policy section.
    """
    _verify_permission("get_policy_section", request_id)

    if policy_name == "FAIL_POLICY":
        log_action(request_id, "Policy Q&A Agent", "tool_call", "get_policy_section", "failure", "Simulated retrieval failure.")
        raise ToolError(f"Failed to retrieve policy section {section} for {policy_name}")

    policy_data = MOCK_POLICY_DATABASE.get(policy_name)
    if not policy_data:
        raise ToolError(f"Policy '{policy_name}' not found in knowledge base.")

    sections = policy_data.get("sections", {})
    sec_data = sections.get(section)
    if not sec_data:
        raise ToolError(f"Section '{section}' not found in policy '{policy_name}'.")

    log_action(
        request_id=request_id,
        agent_name="Policy Q&A Agent",
        action_type="tool_call",
        tool_called="get_policy_section",
        tool_result="success",
        details=f"Retrieved {policy_name} Section {section} - {sec_data.get('title')}."
    )

    return PolicySection(
        policy_name=policy_name,
        section=section,
        title=sec_data.get("title", ""),
        content=sec_data.get("content", "")
    )

def create_audit_log(request_id: str, action_type: str, tool_called: str, tool_result: str, details: str) -> str:
    """Explicitly create an audit entry via tool registry."""
    _verify_permission("create_audit_log", request_id)
    return log_action(
        request_id=request_id,
        agent_name="Policy Q&A Agent",
        action_type=action_type,
        tool_called=tool_called,
        tool_result=tool_result,
        details=details
    )

def restricted_tool_stub(tool_name: str, request_id: str):
    """Helper method to test permission enforcement against prohibited tools."""
    _verify_permission(tool_name, request_id)
