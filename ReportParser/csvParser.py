import sys
import csv
import os.path
import matplotlib.pyplot as plt
import numpy as np

# Mutationt test data
KILLED = "KILLED"
SURVIVED = "SURVIVED"
NO_COVERAGE = "NO_COVERAGE"
# Branch coverage data
MISSED = "MISSED"
COVERED = "COVERED"


def plotHistogram(data):
	hist, bins = np.histogram(data, bins=20)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.show()

def plotGraph(data):
	branchCoverage = []
	mutationCoverage = []
	for key in data:
		if data[key][KILLED]+data[key][SURVIVED] > 0 and data[key][COVERED]+data[key][MISSED] > 0:
			mutCov = 100*data[key][KILLED]/(data[key][KILLED]+data[key][SURVIVED])
			mutationCoverage.append(mutCov)
			branchCov = 100*data[key][COVERED]/(data[key][COVERED]+data[key][MISSED])
			branchCoverage.append(branchCov)
	plt.scatter(branchCoverage, mutationCoverage)
	plt.xlabel('Branch Coverage')
	plt.ylabel('Mutation Coverage')
	plt.show()

def parseJacocoCSV(file, data):
	if os.path.isfile(file):
		reader = csv.reader(open(file),delimiter=',')

		for row in reader:
			if row[5].isdigit() and row[6].isdigit():
				missed = float(row[5])
				covered = float(row[6])
				if missed+covered > 0:
					#branchCoverage = 100*covered/(missed+covered)
					for key in data:
						if key in row[2]:
							data[key][MISSED] += missed
							data[key][COVERED] += covered
							break
	else:
		print("Jacoco file or folder does not exist.")

def parsePitestCSV(file, data):
	if os.path.isfile(file):
		reader = csv.reader(open(file),delimiter=',')

		for row in reader:
			className = row[0].replace(".java","")
			if className in data:
				if row[5] == KILLED :
					data[className][KILLED] += 1
				elif row[5] == SURVIVED :
					data[className][SURVIVED] += 1
				elif row[5] == NO_COVERAGE:
					data[className][NO_COVERAGE] +=1 
			else:
				#init values
				data[className] = {}
				data[className][KILLED] = 0
				data[className][SURVIVED] = 0
				data[className][NO_COVERAGE] = 0
				data[className][MISSED] = 0
				data[className][COVERED] = 0
				#set first pitest value
				if row[5] == KILLED:
					data[className][KILLED] = 1
				elif row[5] == SURVIVED:
					data[className][SURVIVED] = 1
				elif row[5] == NO_COVERAGE:
					data[className][NO_COVERAGE] =1 
	else:
		print("Pitest file or folder does not exist.")

if len(sys.argv) != 3:
	print("Please provide relative path + name of a jacoco .csv file and a pitest .csv file.")
else:
	data = {}
	jacocofile = sys.argv[1]
	pitestfile = sys.argv[2]
	parsePitestCSV(pitestfile, data)
	parseJacocoCSV(jacocofile, data)
	plotGraph(data)
	


