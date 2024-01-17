'''
python binFeatures.py [mat.tab] [bins=5]
'''

from sys import argv
import math

bins = 5.0
if len(argv) > 2:
	bins = int(argv[2])

def parseTab(fNm):
	f = open(fNm)

	for i in f:
		i = i.strip('\n').split('\t')
		for j in range(1,len(i)):
			# print i[j],
			i[j] = math.floor(float(i[j]) * bins)
			# print i[j],
			if i[j] >= bins:
				i[j] = bins - 1
			i[j] = str(i[j]/bins)
			# print i[j]
		print '\t'.join(i)

	f.close()

def main():
	parseTab(argv[1])

if __name__ == '__main__':
	main()