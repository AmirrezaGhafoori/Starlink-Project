import subprocess
import json
import csv
import sys
from datetime import datetime

def run_iperf_test(server_ip, test_duration, test_direction):
    """Run an iperf3 test to the specified server and return throughput for each second."""
    try:
        direction_flag = "-R" if test_direction == "downlink" else ""
        print(f"Starting {test_direction} iperf3 test to {server_ip} for {test_duration} seconds...")
        result = subprocess.run(["iperf3", "-c", server_ip, "-t", str(test_duration), direction_flag, "-i", "1", "--json"], capture_output=True, text=True)
        output = result.stdout
        json_output = json.loads(output)
        throughputs = [interval['sum']['bits_per_second'] / 1e6 for interval in json_output['intervals']]
        print(f"{test_direction.capitalize()} test completed successfully.")
        return throughputs
    except Exception as e:
        print(f"Error running iperf3 {test_direction} test: {e}")
        return None

def save_results(filename, throughputs, timestamps):
    """Save the test results to a CSV file."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (seconds)', 'Throughput (Mbits/sec)'])
        for time, tp in zip(timestamps, throughputs):
            writer.writerow([time, tp])
    print(f"Results have been saved to {filename}.")

def main(duration_minutes):
    server_ip = '100.24.71.216'  # Replace with your server IP
    test_duration = duration_minutes * 60  # Convert minutes to seconds for the test duration
    start_time = datetime.now()

    # Downlink test
    downlink_throughputs = run_iperf_test(server_ip, test_duration, "downlink")
    if downlink_throughputs:
        downlink_filename = f"downlink_throughput_results_{start_time.strftime('%Y%m%d_%H%M%S')}_{duration_minutes}min.csv"
        timestamps = list(range(test_duration))
        save_results(downlink_filename, downlink_throughputs, timestamps)

    # Uplink test
    uplink_throughputs = run_iperf_test(server_ip, test_duration, "uplink")
    if uplink_throughputs:
        uplink_filename = f"uplink_throughput_results_{start_time.strftime('%Y%m%d_%H%M%S')}_{duration_minutes}min.csv"
        save_results(uplink_filename, uplink_throughputs, timestamps)

    end_time = datetime.now()
    print(f"Experiment ended at {end_time.strftime('%Y-%m-%d %H:%M:%S')}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 throughput.py <duration in minutes>")
        sys.exit(1)
    duration_minutes = int(sys.argv[1])
    main(duration_minutes)

