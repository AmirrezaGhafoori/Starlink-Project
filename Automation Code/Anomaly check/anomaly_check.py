import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_and_plot(csv_filename, value_column, title):
    # Load data from CSV
    data = pd.read_csv(csv_filename)

    # Assuming the value column contains the throughput or RTT values
    values = data[value_column]

    # Calculate mean and standard deviation
    mean = np.mean(values)
    std_dev = np.std(values)

    # Filter out outliers beyond 2 standard deviations
    filtered_values = values[np.abs(values - mean) <= 2 * std_dev]

    # Calculate new averages for each 10-second interval
    interval_avg = [np.mean(filtered_values[i:i+10]) for i in range(0, len(filtered_values), 10)]

    # Plot for second-by-second data without outliers
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_values, marker='o', label=f'{title} (Filtered)')
    plt.xlabel('Time (seconds)')
    plt.ylabel(value_column)
    plt.title(f'{title} Every Second (Filtered)')
    plt.legend()
    plt.savefig(f'{title.lower()}_every_second_filtered.png')
    plt.show()

    # Plot for interval averages without outliers
    plt.figure(figsize=(10, 6))
    plt.plot(interval_avg, marker='o', label=f'{title} Interval Average (Filtered)')
    plt.xlabel('Interval')
    plt.ylabel(value_column)
    plt.title(f'{title} Interval Average (Filtered)')
    plt.legend()
    plt.savefig(f'{title.lower()}_interval_avg_filtered.png')
    plt.show()

# Analyze and plot throughput data
analyze_and_plot('rtt_results.csv', 'RTT (ms)', 'RTT')

# Analyze and plot RTT data
# Note: Adjust the file name and column name as per your RTT data CSV
# analyze_and_plot('rtt_results.csv', 'RTT (ms)', 'RTT')

