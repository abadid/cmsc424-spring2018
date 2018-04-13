package queryproc;

public class QueryProcessing {

    public static boolean testOutput(Relation<TupleType3> actualOutput) {

        Relation<TupleType3> correctOutput = new Relation<TupleType3>();
        correctOutput.insert(new TupleType3(1, "NY", "NE",1, 1,  "IBM"));
        correctOutput.insert(new TupleType3(1, "NY", "NE",2, 1, "MorganStanley"));
        correctOutput.insert(new TupleType3(2, "CA", "W",3, 2, "Google"));
        correctOutput.insert(new TupleType3(2, "CA", "W",4, 2, "Apple"));
        correctOutput.insert(new TupleType3(3, "WA", "W",5, 3, "Microsoft"));
        correctOutput.insert(new TupleType3(3, "WA", "W",7, 3, "Amazon"));
        correctOutput.insert(new TupleType3(3, "WA", "W",8, 3, "Boeing"));
        correctOutput.insert(new TupleType3(4, "MD", "S",9, 4, "Geico"));
        correctOutput.insert(new TupleType3(7, "TX", "S",10, 7, "AT&T"));
        correctOutput.insert(new TupleType3(8, "MA", "NE",11, 8, "GE"));
        correctOutput.insert(new TupleType3(9, "NJ", "NE",12, 9, "Johnson&Johnson"));
        correctOutput.insert(new TupleType3(10, "NC", "S",13, 10, "RedHat"));
        correctOutput.insert(new TupleType3(10, "NC", "S",14, 10, "Lenovo"));

        System.out.println("\n\n++++ Correct ResultTable ++++");
        printRelation(correctOutput);

        if (correctOutput.getSize() != actualOutput.getSize()) {
            return false;
        }

        for (int i = 0; i < actualOutput.getSize(); i++) {

            TupleType3 co = correctOutput.getTuple(i);
            TupleType3 ao = actualOutput.getTuple(i);

            if (co.getAttribute(0) != ao.getAttribute(0)) {
                return false;
            }

            if (((String)co.getAttribute(1)).compareTo((String)ao.getAttribute(1)) != 0) {
                return false;
            }

            if (((String)co.getAttribute(2)).compareTo((String)ao.getAttribute(2)) != 0) {
                return false;
            }

            if (co.getAttribute(3) != ao.getAttribute(3)) {
                return false;
            }

            if (co.getAttribute(4) != ao.getAttribute(4)) {
                return false;
            }

            if (((String)co.getAttribute(5)).compareTo((String)ao.getAttribute(5)) != 0) {
                return false;
            }
        }

        return true;
    }

    public static void printRelation1(Relation<TupleType1> relation) {

        for (TupleType1 t : relation.getRelation()) {
            System.out.println(t.getAttribute(0) + " " + t.getAttribute(1) + " " + t.getAttribute(2));
        }
    }

    public static void printRelation2(Relation<TupleType2> relation) {

        for (TupleType2 t : relation.getRelation()) {
            System.out.println(t.getAttribute(0) + " " + t.getAttribute(1) + " " + t.getAttribute(2));
        }
    }

    public static void printRelation(Relation<TupleType3> relation) {

        for (TupleType3 t : relation.getRelation()) {
            System.out.println(t.getAttribute(0) + " " + t.getAttribute(1) + " " + t.getAttribute(2)
            + " " + t.getAttribute(3) + " " + t.getAttribute(4) + " " + t.getAttribute(5));
        }
    }

    public static void main(String[] args) {

        Relation<TupleType1> locations = new Relation<TupleType1>();
        locations.insert(new TupleType1(1, "NY", "NE"));
        locations.insert(new TupleType1(2, "CA", "W"));
        locations.insert(new TupleType1(3, "WA", "W"));
        locations.insert(new TupleType1(4, "MD", "S"));
        locations.insert(new TupleType1(5, "IL", "MW"));
        locations.insert(new TupleType1(6, "GA", "S"));
        locations.insert(new TupleType1(7, "TX", "S"));
        locations.insert(new TupleType1(8, "MA", "NE"));
        locations.insert(new TupleType1(9, "NJ", "NE"));
        locations.insert(new TupleType1(10, "NC", "S"));
        locations.insert(new TupleType1(11, "AZ", "W"));


        Relation<TupleType2> companies = new Relation<TupleType2>();
        companies.insert(new TupleType2(1, 1, "IBM"));
        companies.insert(new TupleType2(2, 1, "MorganStanley"));
        companies.insert(new TupleType2(3, 2, "Google"));
        companies.insert(new TupleType2(4, 2, "Apple"));
        companies.insert(new TupleType2(5, 3, "Microsoft"));
        companies.insert(new TupleType2(7, 3, "Amazon"));
        companies.insert(new TupleType2(8, 3, "Boeing"));
        companies.insert(new TupleType2(9, 4, "Geico"));
        companies.insert(new TupleType2(10, 7, "AT&T"));
        companies.insert(new TupleType2(11, 8, "GE"));
        companies.insert(new TupleType2(12, 9, "Johnson&Johnson"));
        companies.insert(new TupleType2(13, 10, "RedHat"));
        companies.insert(new TupleType2(14, 10, "Lenovo"));

        System.out.println("\n\n++++ Locations ++++");
        printRelation1(locations);

        System.out.println("\n\n++++ Companies ++++");
        printRelation2(companies);

        Relation<TupleType3> resultTable = JoinOperators.MergeJoinOnIntegerAttributes(locations, companies, 0, 1);

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
