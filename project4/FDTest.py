import sys

### checks each line of answers.txt and your output

if len(sys.argv) !=3:
    print "Usage python FDTest.py <path-to-answers.txt> <path-to-your-output file>"
    sys.exit()

infile = sys.argv[1]
outfile = sys.argv[2]

try:
    f = open(infile,"r")
    indata = f.readlines()
    f.close()
except:
    print infile," does not exist"
    sys.exit()

try:
    f = open(outfile,"r")
    outdata = f.readlines()
    f.close()
except:
    print outfile+" does not exist"
    sys.exit()

print "\n\nCOMPARING OUTPUT OF "+sys.argv[0]+" AND "+sys.argv[1]
print "-------------------------------------------------\n"

if len(indata) != len(outdata):
    print "Number of lines in "+infile+" and "+outfile+" not the same"
    sys.exit()

### remove the first 3 lines
indata = indata[3:]
outdata = outdata[3:]

### Checking the number of fuzzy fd's returned
### the last line of both files
if len(indata[-1].split("[")[-1].split("]")[0].split(",")) != len(outdata[-1].split("[")[-1].split("]")[0].split(",")) :
    print "# FUZZY FUNCTIONAL DEPENDENCIES MATCHED"
    print "Expected number of fuzzy functional dependencies = ",len(indata[-1].split("[")[-1].split("]")[0].split(","))
    print "Number of fuzzy functional dependencies you returned =",len(outdata[-1].split("[")[-1].split("]")[0].split(","))
    print "\n"
else:
    print "# FUZZY FUNCTIONAL DEPENDENCIES MATCHED"
    print "\n"


### remove last line after check
indata = indata[:-1]
outdata = outdata[:-1]

### checking individual confidence outputs line by line
for l1,l2 in zip(indata,outdata):

    if l1 == l2 or "Confidences above threshold:" in l1 or "Confidences above threshold:" in l2:
        continue

    n1 = float(l1.split("\n")[0].split("=")[-1].strip())
    n2 = float(l2.split("\n")[0].split("=")[-1].strip())


    if round(n1,3)!=round(n2,3):
        print l1.split("\n")[0].split("=")[0],"DO NOT MATCH"
