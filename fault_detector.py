# PURPOSE: Reads the log and checks for problems
# HOW IT WORKS:
# Opens the CSV file with pandas
# Defines safe ranges for each sensor (temperature < 80 C, etc.)
# For each row, it checks values and labels the status as "ok" or with an error message
# Saves the annotated data to a new file (fault_log.csv)
# Uses retry + backoff logic so if the log file isn't ready yet, it waits and retries instead of crashing

import pandas as pd, os, time

THRESHOLDS = {
    "temperature": {"max": 80, "min": 0},
    "voltage": {"max": 5.5, "min": 4.5},
    "current": {"max": 1.2, "min": 0.8},
    "vibration": {"max": 1.5, "min": 0}
}

def check_row(row):
    faults = []
    if row["temperature"] > THRESHOLDS["temperature"]["max"]:
        faults.append("Overheat")
    if row["temperature"] < THRESHOLDS["temperature"]["min"]:
        faults.append("Too cold")

    if row["voltage"] > THRESHOLDS["voltage"]["max"]:
        faults.append("Overvoltage")
    if row["voltage"] < THRESHOLDS["voltage"]["min"]:
        faults.append("Undervoltage")

    if row["current"] > THRESHOLDS["current"]["max"]:
        faults.append("Overcurrent")
    if row["current"] < THRESHOLDS["current"]["min"]:
        faults.append("Undercurrent")

    if row["vibration"] > THRESHOLDS["vibration"]["max"]:
        faults.append("Excess vibration")

    return ", ".join(faults) if faults else "OK"

def run_fault_detector(
    input_file="data/sensor_log.csv",
    output_file="data/fault_log.csv",
    interval=2
):
    print("⚡ Fault detector running...")
    while True:
        if os.path.exists(input_file):
            try:
                df = pd.read_csv(input_file)
                if not df.empty:
                    df["fault_status"] = df.apply(check_row, axis=1)
                    df.to_csv(output_file, index=False)
                    print(f"✅ Fault detection updated → {output_file} ({len(df)} rows)")
            except Exception as e:
                print(f"⚠️ Error reading {input_file}: {e}")
        else:
            print(f"⚠️ Waiting for {input_file}...")

        time.sleep(interval)

def detect_faults(
    input_file="data/sensor_log.csv",
    output_file="data/fault_log.csv",
    last_index=0
):
    """
    Processes all new rows once (no infinite loop).
    Appends results to fault_log.csv.
    Returns (new_last_index, summary).
    """
    if not os.path.exists(input_file):
        return last_index, {"total_rows": 0, "faults_found": 0, "last_status": None}

    try:
        df = pd.read_csv(input_file)
        if len(df) > last_index:
            new_rows = df.iloc[last_index:].copy()
            new_rows["fault_status"] = new_rows.apply(check_row, axis=1)

            if os.path.exists(output_file):
                new_rows.to_csv(output_file, mode="a", index=False, header=False)
            else:
                new_rows.to_csv(output_file, index=False)

            last_index = len(df)
            summary = {
                "total_rows": int(last_index),
                "faults_found": int((new_rows["fault_status"] != "OK").sum()),
                "last_status": new_rows["fault_status"].iloc[-1]
            }
            print(f"✅ Processed {len(new_rows)} new rows → {output_file}")
            return last_index, summary

    except Exception as e:
        print(f"⚠️ Error reading {input_file}: {e}")

    return last_index, {"total_rows": 0, "faults_found": 0, "last_status": None}


if __name__ == "__main__":
    run_fault_detector()