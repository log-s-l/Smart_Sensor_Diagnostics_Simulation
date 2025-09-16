from simulator import simulate_sensors
from fault_detector import detect_faults
import threading, time, os

def run_test_pipeline(duration=10):
    # Start with a fresh fault log
    if os.path.exists("data/fault_log.csv"):
        os.remove("data/fault_log.csv")

    # Setup stop flag
    stop_flag = threading.Event()

    # Run simulator in background (with stop_flag)
    sim_thread = threading.Thread(target=simulate_sensors, kwargs={"interval":1, "stop_flag":stop_flag})
    sim_thread.start()

    last_index = 0
    summary = {}

    start_time = time.time()
    while time.time() - start_time < duration:  # run for `duration` seconds
        last_index, summary = detect_faults(last_index=last_index)
        time.sleep(2)

    # Tell simulator to stop
    stop_flag.set()
    sim_thread.join()

    print("\n✅ Test pipeline complete")
    print("📊 Summary:", summary)

if __name__ == "__main__":
    run_test_pipeline(duration=10)  # run for 10s
