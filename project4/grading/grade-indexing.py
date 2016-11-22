import math
from disk_relations import *
import sys
import imp
import random
from btree import *
import traceback


# A simple class to keep track of the set of relations and indexes created together
class Database:
	def __init__(self, name):
		self.name = name
		self.relations = dict()
		self.indexes = dict()
	def newRelation(self, relname, rel_schema):
		self.relations[relname] = Relation(relname, rel_schema)
		return self.relations[relname]
	def getRelation(self, relname):
		return self.relations[relname]
	def newIndex(self, relname, attribute, keysize):
		self.indexes[(relname, attribute)] = BTreeIndex(keysize = keysize, relation = self.getRelation(relname), attribute = attribute)
		return self.indexes[(relname, attribute)]
	def getIndex(self, relname, attribute):
		return self.indexes[(relname, attribute)]


def deleteFromTree(relation, index, deleteKey):
	print "------------ Deleting the entry for key " + deleteKey
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


def createDatabase1ForTesting(name):
	## Let's first create a relation with a bunch of tuples 
 	db = Database(name)
	instr_schema = ["ID", "name", "dept_name", "salary"]
	instructor = db.newRelation("instructor", instr_schema)
	instructor.insertTuple(Tuple(instr_schema, ('10101', 'Srinivasan', 'Comp. Sci.', '65000')));
	instructor.insertTuple(Tuple(instr_schema, ('12121', 'Wu', 'Finance', '90000')));
	instructor.insertTuple(Tuple(instr_schema, ('15151', 'Mozart', 'Music', '40000')));
	instructor.insertTuple(Tuple(instr_schema, ('22222', 'Einstein', 'Physics', '95000')));
	instructor.insertTuple(Tuple(instr_schema, ('32343', 'El Said', 'History', '60000')));
	instructor.insertTuple(Tuple(instr_schema, ('33456', 'Gold', 'Physics', '87000')));
	instructor.insertTuple(Tuple(instr_schema, ('45565', 'Katz', 'Comp. Sci.', '75000')));
	instructor.insertTuple(Tuple(instr_schema, ('58583', 'Califieri', 'History', '62000')));
	instructor.insertTuple(Tuple(instr_schema, ('76543', 'Singh', 'Finance', '80000')));
	instructor.insertTuple(Tuple(instr_schema, ('76766', 'Crick', 'Biology', '72000')));
	instructor.insertTuple(Tuple(instr_schema, ('83821', 'Brandt', 'Comp. Sci.', '92000')));
	instructor.insertTuple(Tuple(instr_schema, ('98345', 'Kim', 'Elec. Eng.', '80000')));

	# With the given settings, the following B+-Tree is identical to the one shown in
	# Figure 11.9 in the textbook
	db.newIndex(keysize = 20, relname = "instructor", attribute = "name")
	#db.newIndex(keysize = 20, relname = "instructor", attribute = "dept_name")

	return (db, instructor, db.getIndex("instructor", "name"))



def testIndex1():
	score = 0
	(db, R, index) = createTestIndexDatabase()
	index.printTree()
	for (vals, casedesc) in [ (['15','1'], 'redistribute at leaf: self underfull'), 
			(['7'], 'redistribute at leaf: otherBlock underfull'), 
			(['25','33','0','1','10','11', '35', '36','38'], 'redistribute at interior: otherBlock underfull'), 
			(['35','36','37','32','33','34','0','1','10','11'], 'redistribute at interior: self underfull')]:
		print "\n\n******** Case {} *****************************************************************************************".format(casedesc)
		try:
			(db, R, index) = createTestIndexDatabase()
			for key in vals:
				deleteFromTree(R, index, key)
			if checkValidityTree(index):
				score += 2
			else:
				index.printTree()
				print "Failed the case for: " + casedesc
		except:
			e = sys.exc_info()[0]
			print "Failed the case for: " + casedesc + " with exception" + str(sys.exc_info()[0])
			print sys.exc_info()[1]
			print traceback.format_exc()
	return score

def testIndex2():
	score = 0
	casedesc = 'interior node -- otherblock underfull'
	print "\n\n\n******** Case {} *****************************************************************************************".format(casedesc)
	(db, R, index) = createDatabase1ForTesting("univ")
	index.printTree()
	try:
		R.insertTuple(Tuple(R.schema, ('98346', 'Bob', 'Comp. Sci.', '65000')))
		deleteFromTree(R, index, "Srinivasan")
		if checkValidityTree(index):
			score += 1
		else:
			index.printTree()
			print "Failed the case for: " + casedesc
	except:
		e = sys.exc_info()[0]
		print "Failed the case for: " + casedesc + " with exception" + str(sys.exc_info()[0])
		print sys.exc_info()[1]
		#sys.exc_info()[2].print_exc(file=sys.stdout)
		print traceback.format_exc()

	casedesc = 'interior node -- self underfull'
	print "\n\n\n******** Case {} *****************************************************************************************".format(casedesc)
	(db, R, index) = createDatabase1ForTesting("univ")
	index.printTree()
	try:
		R.insertTuple(Tuple(R.schema, ('98347', 'Z1', 'Comp. Sci.', '65000')))
		R.insertTuple(Tuple(R.schema, ('98348', 'Z2', 'Comp. Sci.', '65000')))
		R.insertTuple(Tuple(R.schema, ('98349', 'Z3', 'Comp. Sci.', '65000')))
		R.insertTuple(Tuple(R.schema, ('98350', 'Z4', 'Comp. Sci.', '65000')))
		deleteFromTree(R, index, "Brandt")
		deleteFromTree(R, index, "Califieri")
		deleteFromTree(R, index, "Crick")
		deleteFromTree(R, index, "Katz")
		deleteFromTree(R, index, "Einstein")
		deleteFromTree(R, index, "Gold")
		if checkValidityTree(index):
			score += 1
		else:
			index.printTree()
			print "Failed the case for: " + casedesc
	except:
		e = sys.exc_info()[0]
		print "Failed the case for: " + casedesc + " with exception" + str(sys.exc_info()[0])
		print sys.exc_info()[1]
		print traceback.format_exc()

	casedesc = 'leaf node -- otherBlock underfull'
	print "\n\n\n******** Case {} *****************************************************************************************".format(casedesc)
	(db, R, index) = createDatabase1ForTesting("univ")
	index.printTree()
	try:
		deleteFromTree(R, index, 'Einstein')
		if checkValidityTree(index):
			score += 1
		else:
			index.printTree()
			print "Failed the case for: " + casedesc
	except:
		e = sys.exc_info()[0]
		print "Failed the case for: " + casedesc + " with exception" + str(sys.exc_info()[0])
		print sys.exc_info()[1]
		print traceback.format_exc()

	casedesc = 'leaf node -- self underfull'
	print "\n\n\n******** Case {} *****************************************************************************************".format(casedesc)
	(db, R, index) = createDatabase1ForTesting("univ")
	try:
		R.insertTuple(Tuple(R.schema, ('98347', 'Z1', 'Comp. Sci.', '65000')))
		R.insertTuple(Tuple(R.schema, ('98348', 'Z2', 'Comp. Sci.', '65000')))
		R.insertTuple(Tuple(R.schema, ('98349', 'Z3', 'Comp. Sci.', '65000')))
		R.insertTuple(Tuple(R.schema, ('98350', 'Z4', 'Comp. Sci.', '65000')))
		deleteFromTree(R, index, "Brandt")
		deleteFromTree(R, index, "Califieri")
		deleteFromTree(R, index, "Crick")
		deleteFromTree(R, index, "Einstein")
		if checkValidityTree(index):
			score += 1
		else:
			index.printTree()
			print "Failed the case for: " + casedesc
	except:
		e = sys.exc_info()[0]
		print "Failed the case for: " + casedesc + " with exception" + str(sys.exc_info()[0])
		print sys.exc_info()[1]
		print traceback.format_exc()
	return score

score = testIndex2() + testIndex1()
print "Score " + str(score)

#with open("score-java.csv", "a") as myfile:
#myfile.write("---- {}, {}\n".format(sys.argv[1], score))
