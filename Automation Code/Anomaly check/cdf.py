import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_cdf_from_csv(csv_file, column_name):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Extract the specific column
    values = data[column_name].dropna()

    # Calculate the CDF values
    sorted_values = np.sort(values)
    cdf = np.arange(1, len(sorted_values)+1) / len(sorted_values)

    # Plot the CDF
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_values, cdf, marker='.', linestyle='none')
    plt.title(f'CDF of {column_name}')
    plt.xlabel(column_name)
    plt.ylabel('CDF')
    plt.grid(True)
    plt.savefig(f'{csv_file[:-4]}_cdf_plot.png')
    plt.show()

# Example usage:
plot_cdf_from_csv('throughput_results.csv', 'Throughput (Mbits/sec)')
plot_cdf_from_csv('rtt_results.csv', 'RTT (ms)')

