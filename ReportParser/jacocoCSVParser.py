import sys
import csv
import os.path
import matplotlib.pyplot as plt
import numpy as np

def plotHistogram(data):
	hist, bins = np.histogram(data, bins=20)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.show()


if(len(sys.argv) == 1):
	print("Please provide relative path + name of a jacoco .csv file.")
else:
	file = sys.argv[1]
	if os.path.isfile(file):
		reader = csv.reader(open(file),delimiter=',')

		branchCoverage = []

		for row in reader:
			if row[5].isdigit() and row[6].isdigit():
				missed = float(row[5])
				covered = float(row[6])
				if missed+covered > 0:
					branchCoverage.append(100*covered/(missed+covered))
				#else:
				#	branchCoverage.append(0)

		plotHistogram(branchCoverage)
	else:
		print("File or folder does not exist.")

