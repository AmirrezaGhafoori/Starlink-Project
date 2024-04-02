import subprocess
import time
import csv
import sys
import requests
from datetime import datetime, timedelta

def run_traceroute():
    """Run the traceroute command and return the output."""
    try:
        # Use '-n' flag to avoid DNS resolution; speeds up the process
        result = subprocess.run(["traceroute", "-n", "google.com"], capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Failed to run traceroute: {e}")
        return ""

def ip_geolocation(ip):
    """Perform an IP geolocation lookup and return the result."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to perform IP geolocation lookup: {e}")
        return {}

def main(duration_minutes):
    end_time = datetime.now() + timedelta(minutes=duration_minutes)

    with open('traceroute_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Hop', 'IP', 'Country', 'RegionName', 'City', 'ISP'])

        while datetime.now() < end_time:
            timestamp = datetime.now().isoformat()
            print(f"Running traceroute at {timestamp}...")  # Verbose output
            traceroute_output = run_traceroute()

            if traceroute_output:
                # Parse the output and perform geolocation lookup for each IP
                for line in traceroute_output.splitlines():
                    parts = line.split()
                    if len(parts) >= 3 and parts[1].isdigit():
                        # This is an IP line in the traceroute output
                        ip = parts[2]
                        print(f"Looking up geolocation for IP: {ip}")  # Verbose output
                        geolocation_result = ip_geolocation(ip)
                        writer.writerow([
                            timestamp, 
                            parts[1],  # Hop number
                            ip, 
                            geolocation_result.get('country', ''),
                            geolocation_result.get('regionName', ''),
                            geolocation_result.get('city', ''),
                            geolocation_result.get('isp', '')
                        ])
            else:
                print("No output received from traceroute.")

            # Wait for 60 seconds before the next run
            time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python traceroute.py <duration in minutes>")
        sys.exit(1)

    duration_minutes = int(sys.argv[1])
    main(duration_minutes)

