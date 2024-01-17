'''
python predictNormBin.py [pileup] [model dir] [norm max=False] [bin normal=True]
'''

from sys import argv
import math
from glob import glob
import xgboost as xgb
import parsePileup

TEST = False
# TEST = True

NORMMAX = False
# NORMMAX = True
BINNORM = True

if argv[2][-1] != '/':
	argv[2] += '/'

if len(argv) > 3 and argv[3][0].lower() == 't':
	NORMMAX = True
if len(argv) > 4 and argv[4][0].lower() == 'f':
	BINNORM = False

def binFeatures(arr, bins=5.0):
	for i in range(0,len(arr)):
		arr[i] = math.floor(float(arr[i]) * bins)
		if arr[i] >= bins:
			arr[i] = bins - 1
		arr[i] = arr[i] / bins

	return arr

def getPreditions(dNm, arr):
	dMat = xgb.DMatrix([arr])

	mLst = glob(dNm + 'all/*pkl')
	preds = []
	for i in mLst:
		# print i
		mod = xgb.Booster(model_file=i)
		pred = mod.predict(dMat)
		preds.append(pred[0])

	return preds

# must run from directory containing 
#   "MCoV-127316.phredParsedSum_bin5.tab"
def parseTest():
	f = open('MCoV-127316.phredParsedSum_bin5.tab')

	ln = f.readline()
	ln = ln.strip('\n').split('\t')
	gid = ln[0]
	arr = ln[1:]
	for i in range(0,len(arr)):
		arr[i] = float(arr[i])

	f.close()

	return gid, arr

def main():
	arr = parsePileup.parsePileup(argv[1], NORMMAX)
	arr = parsePileup.filterArr(arr)
	arr = parsePileup.catArr(arr)
	arr = binFeatures(arr)
	# arr = [0.0] + arr

	if TEST:
		gid2,arr2 = parseTest()
		# arr2 = [0.0] + arr2
		errHsh = {}
		for i in range(0,len(arr)):
			err = abs(arr[i] - arr2[i])
			if err not in errHsh:
				errHsh[err] = 0
			errHsh[err] += 1
		for i in sorted(errHsh):
			print i, errHsh[i]


	preds = getPreditions(argv[2], arr)

	for i in preds:
		print i

	# cntHsh = {}
	# for i in arr:
	# 	if i not in cntHsh:
	# 		cntHsh[i] = 0
	# 	cntHsh[i] += 1

	



if __name__ == '__main__':
	main()