import csv
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

filename = 'battleStats_3_25'

if __name__ == '__main__':
    for filename in glob.glob('*_points.csv'):
        a = []
        with open(filename, 'rb') as search_file:
            points_reader = csv.reader(search_file, delimiter=',')
            n_points = 0
            points_reader.next()
            for point in points_reader:
                a.append(float(point[0]))

            np_hist = np.array(a)
            # np_hist -= 3

            plt.figure(figsize=[10, 8])

            n, bins, patches = plt.hist(x=np_hist, bins=20, range=(0,100), color='#0504aa', alpha=0.7, rwidth=0.95)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Value (distance to target)', fontsize=15)
            plt.ylabel('Frequency', fontsize=15)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            plt.ylabel('Frequency', fontsize=15)
            plt.title('Distance Distribution Histogram', fontsize=15)
            plt.savefig(os.path.splitext(filename)[0] + '.png')
            plt.show()
