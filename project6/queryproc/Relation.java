package queryproc;

import java.util.ArrayList;
import java.util.List;

public class Relation<T> {

    private List<T> table;

    public Relation() {
        this.table = new ArrayList<T>();
    }

    // returns the size of the relation
    public int getSize() {
        return table.size();
    }

    // append a tuple to the relation 
    public void insert(T tuple) {
        table.add(tuple);
    }


    // returns the tuple from this relation at row pos
    public T getTuple(int pos) {
        return table.get(pos);
    }


    // returns the relation
    public List<T> getRelation() {
        return table;
    }
}
