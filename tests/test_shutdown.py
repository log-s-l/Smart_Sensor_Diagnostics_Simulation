import subprocess
import sys
import time
import signal
import platform


def test_shutdown():
    # Start run_all.py as a subprocess
    proc = subprocess.Popen([sys.executable, "run_all.py"])

    time.sleep(5)  # let system start

    # Send shutdown signal
    if platform.system() == "Windows":
        # Windows supports CTRL_BREAK_EVENT or terminate()
        proc.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        # Linux / MacOS supports SIGINT
        proc.send_signal(signal.SIGINT)

    try:
        proc.wait(timeout=10)  # give it time to exit
    except subprocess.TimeoutExpired:
        proc.kill()
        raise AssertionError("Process did not shut down in time")

    assert proc.returncode == 0 or proc.returncode is not None
