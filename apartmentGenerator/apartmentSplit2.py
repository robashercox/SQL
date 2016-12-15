import itertools
import operator
import math
import collections

floorNo = 12
floorArea = 800
apartmentAreas = [55,75,85]
desiredSplit = [5,4,1]
corners = [0,200,300,700] #index of corner

def bestFitMulti(floorAreas,apartmentAreas, looseness, targetSplit):
	'''given a series of areas (normally straights) finds vectors of partners for each straight that sum to desired split'''
	sequence = []
	for i in range(int(math.ceil(max(floorAreas)/apartmentAreas[0]))+1):
	    sequence.append(i)
	floorSplits = list(itertools.combinations_with_replacement(sequence, len(apartmentAreas)))
	vectors = []
	areaVector = []
	for floorArea in floorAreas:
	    lowerTarget = floorArea - looseness
	    upperTarget = floorArea + looseness
	    for floor in floorSplits:
	        floorPermsDupes = itertools.permutations(floor)
	        floorPerms = list(set(list(floorPermsDupes)))
	        for perm in floorPerms:
	            tempArea = sum(itertools.imap(operator.mul,perm, apartmentAreas))
	            if lowerTarget < tempArea < upperTarget:
	                areaVector.append(perm)
	    vectors.append(areaVector)
	    areaVector = []

	closeness = []
	combos = list(itertools.product(*vectors))
	newVectors = []
	for combo in combos:
	    comboL = list(combo)
	    newVectors.append([sum(x) for x in zip(*comboL)])

	for newVector in newVectors:
	    closeness.append(math.degrees(angle(newVector, targetSplit)))

	closest = closeness.index(min(closeness))
	return list(combos[closest])

def dotproduct(v1, v2):
  return sum(int(a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(round((dotproduct(v1, v2) / (length(v1) * length(v2))),5))

def bestFit(floorArea,apartmentAreas,desiredSplit,looseness):
	sequence = []
	for i in range(int(math.ceil(floorArea/apartmentAreas[0]))+1):
	    sequence.append(i)


	floorSplits = list(itertools.combinations_with_replacement(sequence, len(apartmentAreas)))

	lowerTarget = floorArea - looseness
	upperTarget = floorArea + looseness
	areas=[]
	vectors = []


	for floor in floorSplits:
	    floorPermsDupes = itertools.permutations(floor)
	    floorPerms = list(set(list(floorPermsDupes)))
	    for perm in floorPerms:
	        tempArea = sum(itertools.imap(operator.mul,perm, apartmentAreas))
	        if lowerTarget < tempArea < upperTarget:
	            areas.append(tempArea)
	            vectors.append(perm)

	closeness = []
	for vector in vectors:
	  closeness.append(math.degrees(angle(vector, desiredSplit)))


	closest = closeness.index(min(closeness))
	return vectors[closest]

class apartment:
	def __init__(self, start, end, floorArea):
		self.floorArea = floorArea
		self.start = start%floorArea
		self.end = end%floorArea
		self.size = self.end - self.start
		if self.end < self.start:
			self.mid = (self.end + self.start) %floorArea
		else:
			self.mid = (self.end+self.start)/2

	def move(self, d):
		self.start = (d+self.start)%floorArea
		self.end += (d+self.end)%floorArea
		self.mid += (d+self.mid)%floorArea

	def moveTo(self,t):
		self.start = t
		self.end = t + self.size
		self.mid = t + self.size/2

	def changeSize(self, x):
		self.end = self.start + x
		self.size = x
		self.mid = self.start + self.size/2

def apartmentDistance(x,y):
	'''sort apartments then return start of second minus end of first, can be negative'''
	sortedapartment = sorted((x,y), key = lambda k:k.start)
	return sortedapartment[1].start - sortedapartment[0].end

def bigUnitsOnCorners(apartList,corners,floorArea):
	'''not cyclical'''
	cornerApartments = []
	cornerApartments.append(apartment(0, apartList[0], floorArea))
	for i in range(len(corners)-2):
		i+=1
		corner = corners[i]
		area = apartList[i]
		cornerApartments.append(apartment(((corner - (area/2))%floorArea),((corner + (area/2))%floorArea), floorArea))
	cornerApartments.append(apartment(corners[-1]-apartList[len(corners)], corners[-1],floorArea))
	return [sorted(cornerApartments, key = lambda x:x.start), apartList[len(cornerApartments):]]

bestFitted =  bestFit(floorArea,apartmentAreas,[3,5,1],10)

apartList = []
for i in range(len(bestFitted)):
    for k in range(bestFitted[i]):
        apartList.append(apartmentAreas[i])
apartList = list(reversed(apartList))
print apartList
apartments = bigUnitsOnCorners(apartList,corners,floorArea)
cornerApartments = apartments[0]
straightApartments = apartments[1]

# for a in cornerApartments:
 	# print a.size
	# print a.end
#permute over size order of apartments (split corners first)
permos = list(set(list(itertools.permutations(cornerApartments))))
mixedCornerAreas = []
for permo in permos:
	areasMixerT = []
	for a in permo:
		areasMixerT.append(min(apartmentAreas, key=lambda x:abs(x-a.size)))
	mixedCornerAreas.append(areasMixerT)
	# print '==============='

# print mixedCornerAreas
permos = list(set(tuple(i) for i in mixedCornerAreas))



print len(permos)
print permos
areaDiff = 1000

for permo in permos:
	#change apartment sizes
	cornerApartmentsT = cornerApartments
	# print len(permo)
	# for a in permo:
	# 	print a
	for i in range(len(permo)):	
 		cornerApartmentsT[i].changeSize(permo[i])
	#bundle corner cornerApartments that are close to eachother
	bundledApartments = []
	for i in range(len(cornerApartments)):
		distance = apartmentDistance(cornerApartments[i],cornerApartments[(i+1)%len(cornerApartments)])
		if distance < apartmentAreas[0]:
			bundledApartments[-1].append(cornerApartments[(i+1)%len(cornerApartments)])
		else:
			bundledApartments.append([cornerApartments[(i+1)%len(cornerApartments)]])
	# sort bundles
	for a in bundledApartments:
		a = sorted(a, key = lambda x: x.mid)

	# print straightApartments

	straightTSplit = [] #straights total target split
	straightTSplit.append(straightApartments.count(apartmentAreas[0]))
	straightTSplit.append(straightApartments.count(apartmentAreas[1]))
	straightTSplit.append(straightApartments.count(apartmentAreas[2]))


	# for a in bundledApartments:
		# print [x.mid for x in a]

	#adjust close bundles inward OR OUTWARD
	for bundle in bundledApartments:
		if len(bundle) > 1:
			totalFat = 0
			for i in range(len(bundle)-1):
				increment = apartmentDistance(bundle[i], bundle[i+1])
				totalFat += increment
			start = bundle[0].start
			end = bundle[-1].end
			# print start
			# print bundle[0].end
			if start > 0 and end < floorArea:
				bundle[0].moveTo(start+totalFat/2)
			if end == floorArea:
				bundle[0].moveTo(start+totalFat)
			for i in range(len(bundle[1:])):
				# print bundle[i].end
				bundle[i+1].moveTo(bundle[i].end)


	bundleStarts = []
	bundleEnds = []
	for bundle in bundledApartments:
		bundleStarts.append(bundle[0].start)
		bundleEnds.append(bundle[-1].end)



	bundleStarts = sorted(bundleStarts)
	bundleEnds =  sorted(bundleEnds)

	straights = itertools.izip(bundleEnds[:-1], bundleStarts[1:])
	straightSplitAreas = []
	straightAreas =  [a[1]-a[0] for a in straights]
	# print straightAreas
	straightSplits = bestFitMulti(straightAreas,apartmentAreas, 60, straightTSplit)
	for split in straightSplits:
		straightSplitAreas.append(dotproduct(split,apartmentAreas))
	# print straightTSplit
	# print straightSplits
	# print straightSplitAreas
	# print '--------------'
	# print areaDiff
	areaDifft = length(list(itertools.imap(operator.sub, straightAreas,straightSplitAreas)))
	# print areaDifft
	if areaDifft < areaDiff:
		areaDiff = areaDifft
		cornerBundles = bundledApartments
		straightBundles = straightSplits
		chosenPermo = permo
	"""
	for k in bundledApartments:
		if len(k)>1:
	"""
for bundle in bundledApartments:
	print [x.end for x in bundle]
print straightBundles
print areaDiff
print permo