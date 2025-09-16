import pandas as pd

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fault_detector import detect_faults

def test_fault_detection(tmp_path):
    # Setup temporary input file
    input_file = tmp_path / "sensor_log.csv"
    output_file = tmp_path / "fault_log.csv"

    # Create fake sensor log
    df = pd.DataFrame([
        {"temperature": 85, "voltage": 5.0, "current": 1.0, "vibration": 0.5},  # Overheat
        {"temperature": 25, "voltage": 4.0, "current": 0.9, "vibration": 0.2},  # Undervoltage
        {"temperature": 25, "voltage": 5.0, "current": 1.0, "vibration": 0.5},  # OK
    ])
    df.to_csv(input_file, index=False)

    # Run detector once
    last_index, summary = detect_faults(str(input_file), str(output_file))

    # Read results
    out_df = pd.read_csv(output_file)

    assert "fault_status" in out_df.columns
    assert out_df.loc[0, "fault_status"] == "Overheat"
    assert out_df.loc[1, "fault_status"] == "Undervoltage"
    assert out_df.loc[2, "fault_status"] == "OK"
    assert summary["faults_found"] == 2
