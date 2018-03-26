package queryproc;

public class JoinOperators {

    public static Relation<TupleType3> SortMergeJoin(Relation<TupleType1> leftRelation, Relation<TupleType2> rightRelation) {

        Relation<TupleType3> resultRelation = new Relation<TupleType3>();

        /*
        // You may use the following code snippet in your code. Remember to follow the same order of attributes
        // in the ResultRelation as shown below

        // tuple from the left relation
        TupleType1 lrTuple = leftRelation.getTuple();

        // tuple from the right relation
        TupleType2 rrTuple = rightRelation.getTuple();

        // this is the order that you must follow while inserting attributes into the result relation
        resultRelation.insert(new TupleType3(lrTuple.getcId(), lrTuple.getcLoc(), rrTuple.getId(),
                rrTuple.getcId(), rrTuple.getcName()));
        */


        return resultRelation;
    }
}
