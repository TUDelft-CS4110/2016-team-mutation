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

def plotGraph(branchData, mutData):
	

	mutCovMap = {}
	for mutOp in mutData:
		branchCoverage = []
		mutationCoverage = []
		zeroMutCov = []
		fullMutCov = []
		for className in mutData[mutOp]:
			if mutData[mutOp][className][KILLED]+mutData[mutOp][className][SURVIVED] > 0 and branchData[className][COVERED]+branchData[className][MISSED] > 0:
				mutCov = 100*mutData[mutOp][className][KILLED]/(mutData[mutOp][className][KILLED]+mutData[mutOp][className][SURVIVED])
				branchCov = 100*branchData[className][COVERED]/(branchData[className][COVERED]+branchData[className][MISSED])

				if not className in mutCovMap:
					mutCovMap[className] = {}
					mutCovMap[className][0] = 0
					mutCovMap[className][100] = 0
				if mutCov == 0:
					mutCovMap[className][0] += 1
				if mutCov == 100:
					mutCovMap[className][100] += 1

				
				branchCoverage.append(branchCov)
				mutationCoverage.append(mutCov)
		plt.scatter(branchCoverage, mutationCoverage)
		plt.xlabel('Branch Coverage')
		plt.ylabel('Mutation Coverage')
		plt.title(mutOp)
		plt.show()
		plt.cla()
		plt.clf()
		plt.close()
	return mutCovMap

def parseJacocoCSV(file, data):
	if os.path.isfile(file):
		reader = csv.reader(open(file),delimiter=',')

		for row in reader:
			if row[5].isdigit() and row[6].isdigit():
				missed = float(row[5])
				covered = float(row[6])
				if missed+covered > 0:
					for key in data:
						if key in row[2] or key == row[2]:
							data[key][MISSED] += missed
							data[key][COVERED] += covered
							break
	else:
		print("Jacoco file or folder does not exist.")

def parsePitestCSV(file, mutData, branchData):
	if os.path.isfile(file):
		reader = csv.reader(open(file),delimiter=',')

		for row in reader:
			# Add mutation operator
			if not row[2] in mutData:
				mutData[row[2]] = {}
				
			# Add class
			className = row[0].replace(".java","")
			if not className in branchData:
				branchData[className] = {}
				branchData[className][MISSED] = 0
				branchData[className][COVERED] = 0

			if not className in mutData[row[2]]:
				mutData[row[2]][className] = {}
				mutData[row[2]][className][KILLED] = 0
				mutData[row[2]][className][SURVIVED] = 0
				mutData[row[2]][className][NO_COVERAGE] = 0

			if row[5] == KILLED :
				mutData[row[2]][className][KILLED] += 1
			elif row[5] == SURVIVED :
				mutData[row[2]][className][SURVIVED] += 1
			elif row[5] == NO_COVERAGE:
				mutData[row[2]][className][NO_COVERAGE] +=1 
	else:
		print("Pitest file or folder does not exist.")

if len(sys.argv) != 3:
	print("Please provide relative path + name of a jacoco .csv file and a pitest .csv file.")
else:
	mutData = {}
	branchData = {}
	jacocofile = sys.argv[1]
	pitestfile = sys.argv[2]
	parsePitestCSV(pitestfile, mutData, branchData)
	parseJacocoCSV(jacocofile, branchData)
	mutCovMap = plotGraph(branchData, mutData)

	print("============================================")
	print("Zero Mutation Coverage: number of operators")
	print("============================================")
	for className in mutCovMap:
		if mutCovMap[className][0] >= 2:
			print(className + ": " + str(mutCovMap[className][0]))

	print("")
	print("============================================")
	print("Full Mutation Coverage: number of operators")
	print("============================================")
	for className in mutCovMap:
		if mutCovMap[className][100] >= 4:
			print(className + ": " + str(mutCovMap[className][100]))

	


