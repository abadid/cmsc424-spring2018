import math
import random
from disk_relations import *
from btree import *
from queryprocessing import *
from create_sample_databases import *
import sys

def deleteFromTree(relation, index, deleteKey):
	print "============================================== Deleting the entry for key " + deleteKey
	results = index.searchByKey(deleteKey)
	relation.deleteTuple(results[0])
	
def checkValidityTree(index):
	violations = list()
	checkValidityNode(index.root(), minValue = None, maxValue = None, parentptr = None, violations = violations)
	if len(violations) == 0: 
		print "----------------> The tree is valid"
		return True
	else:

		print "----------------> Invalid tree:\n" + ",\n".join([x[0] + "; block = " + str(x[1]) for x in violations])
		return False

def checkValidityNode(node, minValue, maxValue, parentptr, violations): 
	# check whether full
	if node.isUnderfull() or len(node.keysAndPointers) > node.maxlen:
		violations.append(("Length Constraint Violated", node))
	# Check the parent pointer
	if node.parent is not None and ((parentptr is None) or (node.parent.blockNumber != parentptr.blockNumber)):
		violations.append(("Parent Pointer Incorrect", node))
	# Check the order of keys
	for i in range(3, len(node.keysAndPointers), 2):
		if node.keysAndPointers[i] < node.keysAndPointers[i-2]:
			violations.append(("Keys not ordered", node))
	# Check first key is more than and equal to minValue, and also the last value
	if minValue is not None and node.keysAndPointers[1] < minValue:
		violations.append(("Key smaller than minValue allowed", node))
	if maxValue is not None and node.keysAndPointers[-2] >= maxValue:
		violations.append(("Key larger than maxValue allowed", node))
	# If this is a leaf, check that the sibling pointer points to a larger value
	if node.isLeaf and node.keysAndPointers[-1] is not None:
		nextleaf = node.keysAndPointers[-1].getBlock()
		if not nextleaf.isLeaf or node.keysAndPointers[-2] > nextleaf.keysAndPointers[1]:
			violations.append(("Sibling key mismatch", node))

	# Follow the pointers
	if not node.isLeaf:
		checkValidityNode(node.keysAndPointers[0].getBlock(), minValue = None, maxValue = node.keysAndPointers[1], parentptr = node, violations = violations) 
		for i in range(2, len(node.keysAndPointers)-2, 2):
			checkValidityNode(node.keysAndPointers[i].getBlock(), minValue = node.keysAndPointers[i-1], 
					maxValue = node.keysAndPointers[i+1], parentptr = node, violations = violations)
		checkValidityNode(node.keysAndPointers[-1].getBlock(), minValue = node.keysAndPointers[-2], maxValue = None, parentptr = node, violations = violations) 

def createTestIndexDatabase():
	db = Database("test")
	R_Schema = ["A", "B", "C", "D"]
	R = db.newRelation("R", R_Schema)

	random.seed(0)
	for i in range(0, 100):
		R.insertTuple(Tuple(R_Schema, (str(i), str(random.randint(0, 100)), str(random.randint(0, 100000)), str(random.randint(0, 10)))))

	index = db.newIndex(keysize = 10, relname = "R", attribute = "A")
	return (db, R, index)


(db, R, index) = createTestIndexDatabase()
index.printTree()
checkValidityTree(index)

##### NOTE: Below is only one test case -- you need to try different situations to make sure your code works for other situations
#deleteFromTree(R, index, '15')
#deleteFromTree(R, index, '1')
#checkValidityTree(index)
