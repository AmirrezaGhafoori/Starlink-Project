import subprocess
import sys
from datetime import datetime
import os

def run_iperf3(server, duration, test_type, device_name, directory):
    # Get the current time in the desired format for filenames.
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"{time_str}_{test_type}_{device_name}_{duration}_{server}"
    iperf_filename = os.path.join(directory, f"{filename_base}.json")

    # Construct and run the iperf3 command.
    iperf_command = ['iperf3', '-c', server, '-t', str(duration), '--json', '--logfile', iperf_filename]
    subprocess.run(iperf_command)

    print(f"Test completed: {filename_base}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 tcpdl.py <server_name> <duration>")
        sys.exit(1)

    server_name = sys.argv[1]
    test_duration = sys.argv[2]
    test_type = "tcpdl"
    device_name = "starlink"

    # Set the fixed directory to save the results.
    directory = "/home/starlink/Desktop/results/tcpdl/" + server_name
    if not os.path.exists(directory):
        os.makedirs(directory)

    run_iperf3(server_name, test_duration, test_type, device_name, directory)

if __name__ == "__main__":
    main()
