import subprocess
import sys
from datetime import datetime
import os

def get_gps_coordinates():
    try:
        # Attempt to fetch GPS data using 'cgps -s'
        gps_output = subprocess.check_output(['cgps', '-s'], text=True, stderr=subprocess.STDOUT, timeout=30)
        # Process gps_output to extract the needed GPS data. This will vary based on your output format.
        # For demonstration, we'll just return the raw output or a placeholder.
        return gps_output  # Or parse and return specific latitude and longitude.
    except subprocess.CalledProcessError as e:
        # Handle cases where the cgps command fails (e.g., returns a non-zero exit status).
        print(f"Error fetching GPS data: {e.output}")
        return "GPS data not available"
    except subprocess.TimeoutExpired:
        # Handle case where cgps command times out.
        print("GPS data fetch timed out")
        return "GPS data fetch timed out"
    except Exception as e:
        # Handle any other exceptions.
        print(f"An error occurred while fetching GPS data: {e}")
        return "Error fetching GPS data"


def get_device_name():
    # Use 'whoami' to get the current user name as the device name.
    return subprocess.check_output(['whoami'], text=True).strip()

def run_iperf3(server, duration, test_type, device_name, directory):
    # Get the current time in the desired format for filenames.
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"{time_str}_{test_type}_{device_name}_{duration}_{server}"
    gps_filename = os.path.join(directory, f"{filename_base}_gps.txt")
    iperf_filename = os.path.join(directory, f"{filename_base}.json")

    # Get GPS coordinates and save to a file.
    gps_data = get_gps_coordinates()
    with open(gps_filename, 'w') as gps_file:
        gps_file.write(gps_data)

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
    device_name = get_device_name()

    # Determine the directory based on the server name. Adjust path as necessary.
    directory = f"/home/{device_name}/results/tcpdl/{server_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    run_iperf3(server_name, test_duration, test_type, device_name, directory)

if __name__ == "__main__":
    main()
