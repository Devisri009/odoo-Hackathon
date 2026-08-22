import uuid
import json
from datetime import datetime
from pydantic import ValidationError
from groq import Groq

from schemas import AttendanceAnomalyRequest, AttendanceAnomalyResponse, AttendanceRecord
from tools import (
    get_attendance_records, get_attendance_summary,
    send_attendance_reminder, escalate_systemic_anomaly, ToolError, PermissionError
)
from audit import log_action
from config import get_groq_api_key, get_model_name, get_systemic_threshold

def run_attendance_anomaly(request_data: dict) -> dict:
    execution_id = str(uuid.uuid4())
    warnings = []
    
    try:
        req = AttendanceAnomalyRequest(**request_data)
    except ValidationError as e:
        return _build_error_response(request_data.get("request_id", str(uuid.uuid4())), execution_id, f"Validation Error: {str(e)}")

    log_action(execution_id, "Attendance Anomaly Agent", "start", "N/A", "success", f"Started analysis for {req.target_date}")

    try:
        records_data = get_attendance_records(req.target_date, execution_id, req.employee_ids)
        summary = get_attendance_summary(req.target_date, execution_id)
    except (ToolError, PermissionError) as e:
        warnings.append(str(e))
        return _build_error_response(req.request_id, execution_id, "Attendance service failure. Manual HR review required.", warnings=warnings)

    records = [AttendanceRecord(**r) for r in records_data]
    anomalies = []
    
    for r in records:
        anomaly_type = None
        if not r.check_in and not r.check_out:
            anomaly_type = "INCOMPLETE_ATTENDANCE"
        elif not r.check_in:
            anomaly_type = "MISSING_CHECK_IN"
        elif not r.check_out:
            anomaly_type = "MISSING_CHECK_OUT"
        elif r.check_in > r.expected_check_in:
            anomaly_type = "LATE_CHECK_IN"
        elif r.check_out > "17:00:00": # simple logic for late checkout if needed, or expected_check_out
            pass
            
        if anomaly_type:
            anomalies.append({
                "employee_id": r.employee_id,
                "type": anomaly_type,
                "details": f"Expected: {r.expected_check_in}, Actual: {r.check_in or 'Missing'}"
            })

    # Systemic detection
    expected_headcount = summary.get("expected_headcount", 1)
    if expected_headcount == 0: expected_headcount = 1 # prevent div/0
    threshold = get_systemic_threshold()
    
    anomaly_ratio = len(anomalies) / expected_headcount
    is_systemic = anomaly_ratio >= threshold

    notification_sent = False
    requires_hr_review = False
    recommendation = ""
    severity = "LOW"
    reasoning = ""

    if is_systemic:
        severity = "CRITICAL"
        requires_hr_review = True
        recommendation = "Possible attendance/biometric system outage. Manual HR investigation required."
        reasoning = f"Systemic anomaly detected. {len(anomalies)} out of {expected_headcount} expected employees reported anomalies."
        escalate_systemic_anomaly(req.target_date, reasoning, execution_id)
    elif anomalies:
        severity = "MEDIUM"
        requires_hr_review = False
        recommendation = "Individual anomalies detected. Sending reminders."
        reasoning = f"{len(anomalies)} individual anomalies detected."
        # Generate and send reminders
        for anomaly in anomalies:
            message = _generate_reminder_message(anomaly, req.target_date, execution_id)
            send_attendance_reminder(anomaly["employee_id"], req.target_date, anomaly["type"], message, execution_id)
        notification_sent = True
    else:
        severity = "LOW"
        requires_hr_review = False
        recommendation = "No anomalies detected."
        reasoning = "All attendance records within expected parameters."

    res = AttendanceAnomalyResponse(
        request_id=req.request_id,
        agent_name="Attendance Anomaly Agent",
        success=True,
        anomalies_detected=anomalies,
        systemic_issue=is_systemic,
        recommendation=recommendation,
        severity=severity,
        notification_sent=notification_sent,
        requires_hr_review=requires_hr_review,
        reasoning_summary=reasoning,
        warnings=warnings,
        audit_id=execution_id
    )
    return res.model_dump(mode='json')

def _generate_reminder_message(anomaly, date, execution_id):
    api_key = get_groq_api_key()
    if not api_key or api_key == "mock":
        return f"Please review your attendance for {date}. Issue: {anomaly['type']}."
    
    client = Groq(api_key=api_key)
    prompt = f"Write a polite, one-sentence reminder for an employee regarding an attendance anomaly: {anomaly['type']} on {date}. Do not be aggressive."
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=get_model_name()
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return f"Please review your attendance for {date}. Issue: {anomaly['type']}."

def _build_error_response(req_id, exec_id, reason, warnings=None):
    res = AttendanceAnomalyResponse(
        request_id=req_id,
        agent_name="Attendance Anomaly Agent",
        success=False,
        anomalies_detected=[],
        systemic_issue=False,
        recommendation=reason,
        severity="HIGH",
        notification_sent=False,
        requires_hr_review=True,
        reasoning_summary=reason,
        warnings=warnings or [],
        audit_id=exec_id
    )
    return res.model_dump(mode='json')
