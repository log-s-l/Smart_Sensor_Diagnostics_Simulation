import pandas as pd

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fault_detector import detect_faults


def test_resilience(tmp_path):
    input_file = tmp_path / "sensor_log.csv"
    output_file = tmp_path / "fault_log.csv"

    # Start with missing input file
    last_index, summary = detect_faults(str(input_file), str(output_file))
    assert summary["total_rows"] == 0

    # Now create input file after the fact
    df = pd.DataFrame([
        {"temperature": 25, "voltage": 5.0, "current": 1.0, "vibration": 0.3},
    ])
    df.to_csv(input_file, index=False)

    # Should now process row correctly
    last_index, summary = detect_faults(str(input_file), str(output_file))
    assert summary["total_rows"] == 1
    assert summary["last_status"] == "OK"
