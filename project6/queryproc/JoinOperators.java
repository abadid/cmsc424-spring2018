package queryproc;

public class JoinOperators {

    public static Relation<TupleType3> MergeJoinOnIntegerAttributes(Relation<TupleType1> leftRelation, Relation<TupleType2> rightRelation,
                                                     int lrJoinAttributeIndex, int rrJoinAttributeIndex) {

        Relation<TupleType3> resultRelation = new Relation<TupleType3>();

        /*
        
        // You may use the following code snippet in your code. Remember to follow the same order of attributes
        // in the ResultRelation as shown below

        // tuple from the left relation from row pos
        TupleType1 lrTuple = leftRelation.getTuple(pos);

        // tuple from the right relation from row pos
        TupleType2 rrTuple = rightRelation.getTuple(pos);

        // this is the order that you must follow while inserting attributes into the result relation
        resultRelation.insert(new TupleType3(lrTuple.getAllAttributes(), rrTuple.getAllAttributes()));

        */

        return resultRelation;
    }
}
