package queryproc;

public class QueryProcessing {

    public static boolean testOutput(Relation<TupleType3> actualOutput) {

        Relation<TupleType3> correctOutput = new Relation<TupleType3>();
        correctOutput.insert(new TupleType3(1, "NY", 1, 1,  "IBM"));
        correctOutput.insert(new TupleType3(1, "NY", 2, 1, "MorganStanley"));
        correctOutput.insert(new TupleType3(2, "CA", 3, 2, "Google"));
        correctOutput.insert(new TupleType3(2, "CA", 4, 2, "Apple"));
        correctOutput.insert(new TupleType3(3, "WA", 5, 3, "Microsoft"));
        correctOutput.insert(new TupleType3(3, "WA", 7, 3, "Amazon"));
        correctOutput.insert(new TupleType3(3, "WA", 8, 3, "Boeing"));
        correctOutput.insert(new TupleType3(4, "MD", 9, 4, "Geico"));
        correctOutput.insert(new TupleType3(7, "TX", 10, 7, "AT&T"));
        correctOutput.insert(new TupleType3(8, "MA", 11, 8, "GE"));
        correctOutput.insert(new TupleType3(9, "NJ", 12, 9, "Johnson&Johnson"));
        correctOutput.insert(new TupleType3(10, "NC", 13, 10, "RedHat"));
        correctOutput.insert(new TupleType3(10, "NC", 14, 10, "Lenovo"));

        System.out.println("\n\n++++ Correct ResultTable ++++");
        printRelation(correctOutput);

        if (correctOutput.getSize() != actualOutput.getSize()) {
            return false;
        }

        for (int i = 0; i < actualOutput.getSize(); i++) {

            TupleType3 co = correctOutput.getTuple(i);
            TupleType3 ao = actualOutput.getTuple(i);

            if (co.getcId() != ao.getcId()) {
                return false;
            }

            if (co.getcLoc().compareTo(ao.getcLoc()) != 0) {
                return false;
            }

            if (co.getId() != ao.getId()) {
                return false;
            }

            if (co.getc_Id() != ao.getc_Id()) {
                return false;
            }

            if (co.getcName().compareTo(ao.getcName()) != 0) {
                return false;
            }
        }

        return true;
    }

    public static void printRelation1(Relation<TupleType1> relation) {

        for (TupleType1 t : relation.getRelation()) {
            System.out.println(t.getcId() + " " + t.getcLoc());
        }
    }

    public static void printRelation2(Relation<TupleType2> relation) {

        for (TupleType2 t : relation.getRelation()) {
            System.out.println(t.getId() + " " + t.getcId() + " " + t.getcName());
        }
    }

    public static void printRelation(Relation<TupleType3> relation) {

        for (TupleType3 t : relation.getRelation()) {
            System.out.println(t.getcId() + " " + t.getcLoc() + " " + t.getId() + " " + t.getc_Id() + " " + t.getcName());
        }
    }

    public static void main(String[] args) {

        Relation<TupleType1> companyLocation = new Relation<TupleType1>();
        companyLocation.insert(new TupleType1(1, "NY"));
        companyLocation.insert(new TupleType1(2, "CA"));
        companyLocation.insert(new TupleType1(3, "WA"));
        companyLocation.insert(new TupleType1(4, "MD"));
        companyLocation.insert(new TupleType1(5, "IL"));
        companyLocation.insert(new TupleType1(6, "GA"));
        companyLocation.insert(new TupleType1(7, "TX"));
        companyLocation.insert(new TupleType1(8, "MA"));
        companyLocation.insert(new TupleType1(9, "NJ"));
        companyLocation.insert(new TupleType1(10, "NC"));
        companyLocation.insert(new TupleType1(11, "AZ"));


        Relation<TupleType2> companyName = new Relation<TupleType2>();
        companyName.insert(new TupleType2(1, 1, "IBM"));
        companyName.insert(new TupleType2(2, 1, "MorganStanley"));
        companyName.insert(new TupleType2(3, 2, "Google"));
        companyName.insert(new TupleType2(4, 2, "Apple"));
        companyName.insert(new TupleType2(5, 3, "Microsoft"));
        companyName.insert(new TupleType2(7, 3, "Amazon"));
        companyName.insert(new TupleType2(8, 3, "Boeing"));
        companyName.insert(new TupleType2(9, 4, "Geico"));
        companyName.insert(new TupleType2(10, 7, "AT&T"));
        companyName.insert(new TupleType2(11, 8, "GE"));
        companyName.insert(new TupleType2(12, 9, "Johnson&Johnson"));
        companyName.insert(new TupleType2(13, 10, "RedHat"));
        companyName.insert(new TupleType2(14, 10, "Lenovo"));

        System.out.println("\n\n++++ CompanyLocation ++++");
        printRelation1(companyLocation);

        System.out.println("\n\n++++ CompanyName ++++");
        printRelation2(companyName);

        Relation<TupleType3> resultTable = JoinOperators.SortMergeJoin(companyLocation, companyName);

        System.out.println("\n\n++++ Your ResultTable ++++");
        printRelation(resultTable);


        if (testOutput(resultTable)){
            System.out.println("\n\nTest: Pass!");
        }
        else {
            System.out.println("\n\nTest: Fail!");
        }
    }
}
