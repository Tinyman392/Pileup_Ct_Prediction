'''
python parsePileup.py [pileup file]
'''

from sys import argv

MASKS = [[0,100], [22029,22033], [22340,22367], [22897,22897], [22899,22905], [23108,23122], [29770,29870]]

def getNum(s):
	lNum = -1
	for i in range(1,len(s)+1):
		if not s[:i].isdigit():
			break
		else:
			lNum = int(s[:i])

	return lNum

def normalizeArr(arr, byMax = False):
	D = 0
	if byMax:
		D = max(arr)
	else:
		D = sum(arr)

	if D == 0:
		return arr 

	for i in range(0,len(arr)):
		arr[i] /= float(D)

	return arr

def parsePileup(fNm, byMax = False):
	f = open(fNm)

	arr = []
	cHsh = {
		'A':0,
		'C':1,
		'G':2,
		'T':3,
		'+':4,
		'-':5
	}
	for i in f:
		i = i.strip('\n').split('\t')
		pos = int(i[1])
		ref = i[2].upper()
		if len(arr) < pos:
			arr.append([0]*6)
		sArr = [0] * 6

		pile = i[4]

		j = 0
		insdel = False
		while j < len(pile):
			if insdel:
				lNum = getNum(pile[j:])
				if lNum > 0:
					# prev = pile[j-1]
					# if prev == '-':
					# 	sArr[cHsh['-']] += lNum - 1
					# elif prev == '+':
					# 	sArr[cHsh['+']] += lNum - 1
					j += lNum + len(str(lNum))
				insdel = False

				if j >= len(pile):
					break

			if pile[j].isalpha() and pile[j].upper() in cHsh:
				sArr[cHsh[pile[j].upper()]] += 1
			elif pile[j] == '.' or pile[j] == ',':
				sArr[cHsh[ref]] += 1
			elif pile[j] == '+':
				sArr[cHsh['+']] += 1
				insdel = True
			elif pile[j] == '-':
				sArr[cHsh['-']] += 1
				insdel = True

			j += 1

		sArr = normalizeArr(sArr, byMax)
		arr.append(sArr)

	f.close()

	return arr

def filterArr(arr):
	dLst = []
	for i in range(0,len(arr)):
		for j in MASKS:
			if i >= j[0] and i <= j[1]:
				dLst.append(i)
				break

	for i in dLst[::-1]:
		del arr[i]

	return arr

def catArr(arr):
	cArr = []
	for i in arr:
		cArr += i

	return cArr

def printArr(arr):
	cArr = arr
	for i in range(0,len(cArr)):
		cArr[i] = str(cArr[i])
	print '\t'.join(cArr)

def main():
	arr = parsePileup(argv[1])
	arr = filterArr(arr)
	arr = catArr(arr)
	printArr(arr)

if __name__ == '__main__':
	main()