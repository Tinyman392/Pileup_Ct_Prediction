'''
python makeMatrix.py [dNm]
'''

from sys import argv,stderr
import os
from glob import glob

if argv[1][-1] != '/':
	argv[1] += '/'

def err(s):
	stderr.write(s)

def parseTab(fNm):
	f = open(fNm)

	arr = []
	for i in f:
		arr = i.strip('\n').split('\t')

	f.close()

	return arr

def parseDir(dNm):
	fLst = glob(dNm + '*.arr.tab')

	err("Parsing arrays...\n\t")
	cnt = 0
	inc = len(fLst) / 50.
	mat = []
	for i in fLst:
		if cnt >= inc:
			cnt = 0
			err('=')
		cnt += 1

		gid = os.path.basename(i).replace('.arr.tab', '')
		arr = [gid] + parseTab(i)
		mat.append(arr)
	err('\n')

	return mat

def printMat(mat):
	err("Printing matrix...\n\t")
	cnt = 0
	inc = len(mat) / 50.
	for i in mat:
		if cnt >= inc:
			err('=')
			cnt = 0
		cnt += 1

		print '\t'.join(i)
	err('\n')

def main():
	mat = parseDir(argv[1])
	printMat(mat)

if __name__ == '__main__':
	main()