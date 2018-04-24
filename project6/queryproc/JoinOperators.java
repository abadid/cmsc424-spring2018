package queryproc;

public class JoinOperators {

    public static Relation<TupleType3> MergeJoinOnIntegerAttributes(Relation<TupleType1> leftRelation, Relation<TupleType2> rightRelation,
            int lrJoinAttributeIndex, int rrJoinAttributeIndex) {

        Relation<TupleType3> resultRelation = new Relation<TupleType3>();

        /*

        // You may use the following code snippet in your code. Remember to follow the same order of attributes
        // in the ResultRelation as shown below

        // tuple from the left relation from row pos
        TupleType1 lrTuple = leftRelation.getTuple(rowid);

        // tuple from the right relation from row pos
        TupleType2 rrTuple = rightRelation.getTuple(rowid);

        // this is the order that you must follow while inserting attributes into the result relation
        resultRelation.insert(new TupleType3(lrTuple.getAllAttributes(), rrTuple.getAllAttributes()));

         */

        int left = 0, right = 0;
        while (left < leftRelation.getSize() && right < rightRelation.getSize()) {
            TupleType1 lrTuple = leftRelation.getTuple(left);
            TupleType2 rrTuple = rightRelation.getTuple(right);

            int left_key = (Integer) lrTuple.getAttribute(lrJoinAttributeIndex);
            int right_key = (Integer) rrTuple.getAttribute(rrJoinAttributeIndex);

            if (left_key == right_key) {
                resultRelation.insert(new TupleType3(lrTuple.getAllAttributes(), rrTuple.getAllAttributes()));
                right++;
            } else if (left_key < right_key) {      
                left++;
            } else {
                right++;
            }
        }
        return resultRelation;
    }
}
