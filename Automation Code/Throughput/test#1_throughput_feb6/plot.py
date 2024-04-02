import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

def aggregate_throughput_values(pattern):
    """Aggregate throughput values from all files matching the pattern."""
    files = glob.glob(pattern)
    all_throughputs = []
    for file in files:
        df = pd.read_csv(file)
        all_throughputs.extend(df['Throughput (Mbits/sec)'].values)
    return all_throughputs

def plot_cdf(data, title):
    """Plot a CDF graph of the data."""
    sorted_data = np.sort(data)
    cdf = np.arange(len(sorted_data)) / (len(sorted_data) - 1)
    plt.figure()
    plt.plot(sorted_data, cdf)
    plt.title(f'CDF of Throughput for {title}')
    plt.xlabel('Throughput (Mbits/sec)')
    plt.ylabel('CDF')
    plt.grid(True)
    plt.savefig(f'throughput_{title.lower()}_CDF.png')
    plt.close()

def plot_histogram(data, title):
    """Plot a histogram of the data."""
    plt.figure()
    plt.hist(data, bins=30, alpha=0.75, edgecolor='black')
    plt.title(f'Histogram of Throughput for {title}')
    plt.xlabel('Throughput (Mbits/sec)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(f'throughput_{title.lower()}_histogram.png')
    plt.close()

def main():
    # Aggregate throughput values for downlink and uplink
    downlink_throughputs = aggregate_throughput_values("*downlink_throughput_results*.csv")
    uplink_throughputs = aggregate_throughput_values("*uplink_throughput_results*.csv")

    # Plot CDF and histogram for downlink
    plot_cdf(downlink_throughputs, "Downlink")
    plot_histogram(downlink_throughputs, "Downlink")

    # Plot CDF and histogram for uplink
    plot_cdf(uplink_throughputs, "Uplink")
    plot_histogram(uplink_throughputs, "Uplink")

if __name__ == "__main__":
    main()

