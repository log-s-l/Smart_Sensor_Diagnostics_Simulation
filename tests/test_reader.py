import sys, os
import pandas as pd

# add project root to sys.path (quick fix approach)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from reader import get_latest, get_summary

def test_get_latest(tmp_path):
    # make a fake fault log
    file = tmp_path / "fault_log.csv"
    pd.DataFrame([
        {"time": "t1", "temperature": 50, "voltage": 5, "current": 1, "vibration": 0.5, "fault_status": "OK"},
        {"time": "t2", "temperature": 90, "voltage": 6, "current": 1.5, "vibration": 2.0, "fault_status": "Overheat"},
    ]).to_csv(file, index=False)

    latest = get_latest(file)
    assert latest["time"] == "t2"
    assert latest["fault_status"] == "Overheat"


def test_get_summary(tmp_path):
    file = tmp_path / "fault_log.csv"
    pd.DataFrame([
        {"time": "t1", "temperature": 50, "voltage": 5, "current": 1, "vibration": 0.5, "fault_status": "OK"},
        {"time": "t2", "temperature": 90, "voltage": 6, "current": 1.5, "vibration": 2.0, "fault_status": "Overheat"},
    ]).to_csv(file, index=False)

    summary = get_summary(file)
    assert summary["total_rows"] == 2
    assert summary["faults_found"] == 1
    assert summary["last_status"] == "Overheat"
