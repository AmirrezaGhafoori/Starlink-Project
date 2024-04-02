import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

def aggregate_rtt_values(pattern):
    """Aggregate RTT values from all files matching the pattern."""
    files = glob.glob(pattern)
    all_rtt_values = []
    for file in files:
        df = pd.read_csv(file)
        all_rtt_values.extend(df['RTT (ms)'].values)
    return all_rtt_values

def plot_cdf(data, title):
    """Plot a CDF graph of the data."""
    sorted_data = np.sort(data)
    cdf = np.arange(len(sorted_data)) / (len(sorted_data) - 1)
    plt.figure()
    plt.plot(sorted_data, cdf)
    plt.title(f'CDF of {title}')
    plt.xlabel('RTT (ms)')
    plt.ylabel('CDF')
    plt.grid(True)
    plt.savefig(f'{title}_CDF.png')
    plt.close()

def plot_histogram(data, title):
    """Plot a histogram of the data."""
    plt.figure()
    plt.hist(data, bins=30, alpha=0.75, edgecolor='black')
    plt.title(f'Histogram of {title}')
    plt.xlabel('RTT (ms)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(f'{title}_histogram.png')
    plt.close()

def main():
    # Pattern to match all RTT results files
    pattern = "rtt_results_*.csv"
    
    # Aggregate RTT values from all matching files
    rtt_values = aggregate_rtt_values(pattern)
    
    # Generate and save the CDF and histogram plots
    plot_cdf(rtt_values, "RTT")
    plot_histogram(rtt_values, "RTT")

if __name__ == "__main__":
    main()

