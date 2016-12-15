import itertools
import operator
import math

def dotproduct(v1, v2):
  return sum(int(a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(round((dotproduct(v1, v2) / (length(v1) * length(v2))),5))

floorNo = 12
floorArea = 800
apartmentAreas = [45,65,80]
desiredSplit = [5,4,1]

totalArea = floorNo*floorArea
print totalArea

combinedBasis = sum(itertools.imap(operator.mul, apartmentAreas,desiredSplit))
print combinedBasis

print totalArea/combinedBasis

sequence = []
for i in range(int(math.ceil(floorArea/apartmentAreas[0]))+1):
    sequence.append(i)


floorSplits = list(itertools.combinations_with_replacement(sequence, len(apartmentAreas)))

lowerTarget = floorArea - 1
upperTarget = floorArea + 1
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
print vectors[closest]

a = vectors
b = areas



