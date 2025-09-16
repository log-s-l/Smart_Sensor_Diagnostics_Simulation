from fault_detector import detect_faults
import os, pandas as pd

def test_fault_detection_runs():
    os.makedirs("data", exist_ok=True)
    with open("data/sensor_log.csv", "w") as f:
        f.write("time,temperature,voltage,current,vibration\n0,85,5,1,2\n")
    detect_faults()
    df = pd.read_csv("data/fault_log.csv")
    assert "Overheat" in df["fault_status"].iloc[0]
