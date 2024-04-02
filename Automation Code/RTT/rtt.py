import subprocess
import re
import csv
import sys
import time
from datetime import datetime

def run_ping_test(target_ip, count):
    """Run a ping test and return the RTT of each ping."""
    try:
        print(f"Running ping test to {target_ip}...")
        result = subprocess.run(["ping", "-c", str(count), target_ip], capture_output=True, text=True)
        output = result.stdout
        rtt_times = re.findall(r'time=([\d.]+) ms', output)
        rtt_times = [float(rtt) for rtt in rtt_times]
        print(f"Ping test completed.")
        return rtt_times
    except Exception as e:
        print(f"Error running ping: {e}")
        return None

def main(duration_minutes):
    target_ip = '100.24.71.216'  # Replace with your target IP
    ping_count = duration_minutes * 60  # Assuming 1 ping per second
    all_rtt_values = []

    start_time = datetime.now()
    filename = f"rtt_results_{start_time.strftime('%Y%m%d_%H%M%S')}_{duration_minutes}min.csv"

    rtt_values = run_ping_test(target_ip, ping_count)
    if rtt_values:
        all_rtt_values.extend(rtt_values)
        print(f"Recorded {len(rtt_values)} RTT measurements.")

    # Saving results to a CSV file with the unique filename
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (seconds)', 'RTT (ms)'])
        for i, rtt in enumerate(all_rtt_values, start=1):
            writer.writerow([i, rtt])

    print(f"Results have been saved to {filename}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 rtt.py <duration in minutes>")
        sys.exit(1)
    duration_minutes = int(sys.argv[1])
    main(duration_minutes)

