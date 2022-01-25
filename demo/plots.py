import ast
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def create_plot_fps(name):
    plt.figure()
    with open("fps.txt", mode="r") as f:
        data = ast.literal_eval(f.readline())

    plt.bar(data.keys(), data.values())
    plt.title("1000 frames transfer")
    plt.ylabel("FPS")
    plt.xlabel("Routine")
    plt.savefig("fps-" + name)
    plt.close()


def create_plot_travel_time(name):
    plt.figure()
    with open("travel_time.txt", mode="r") as f:
        data = eval(f.readline())

        num_bins = 100
        # the histogram of the data
        n, bins, patches = plt.hist(data, num_bins, facecolor='blue', alpha=0.5)

        # add a 'best fit' line
        plt.xlabel('Travel Time')
        plt.ylabel('Total transfers')
        plt.title(r'Histogram of Travel Time')

        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)
        plt.axvline(np.median(data), linestyle="dashed")
        plt.xticks(np.arange(0, max(data), 0.005), rotation=90)
        plt.savefig("travel_time-" + name)
        plt.close()
