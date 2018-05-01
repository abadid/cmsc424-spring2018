package queryproc;

public class JoinOperators {

    public static Relation<TupleType3> MergeJoinOnIntegerAttributes(Relation<TupleType1> leftRelation, Relation<TupleType2> rightRelation,
                                                     int lrJoinAttributeIndex, int rrJoinAttributeIndex) {

        Relation<TupleType3> resultRelation = new Relation<TupleType3>();
        int pos;
        /*
        
        // You may use the following code snippet in your code.
        // tuple from the left relation at row corresponding to variable: pos
        TupleType1 lrTuple = leftRelation.getTuple(pos);
        // tuple from the right relation at row corresponding to variable: pos
        TupleType2 rrTuple = rightRelation.getTuple(pos);
        // this is how you will insert attributes into the result relation
        resultRelation.insert(new TupleType3(lrTuple.getAllAttributes(), rrTuple.getAllAttributes()));
        */

        return resultRelation;
    }
}
