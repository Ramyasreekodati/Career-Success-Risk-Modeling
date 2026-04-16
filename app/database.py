import json
import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "data", "audit_logs.jsonl")

def log_decision(student_data, prediction, decision):
    """
    Logs every inference and underwriting decision for audit and future retraining.
    """
    os.makedirs('data', exist_ok=True)
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "input": student_data,
        "prediction": prediction,
        "underwriting": decision
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_learning_stats():
    """
    Reads logs to show dashboard stats on decision trends.
    """
    if not os.path.exists(LOG_FILE):
        return {"total_inferences": 0, "approvals": 0}
    
    count = 0
    approvals = 0
    with open(LOG_FILE, "r") as f:
        for line in f:
            count += 1
            data = json.loads(line)
            # Check for 'Approved' or 'Fast-Track' in decision string
            decision = data.get('underwriting', {}).get('decision', "")
            if "Approved" in decision:
                approvals += 1
    return {"total_inferences": count, "approvals": approvals}
