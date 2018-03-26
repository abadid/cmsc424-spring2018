package queryproc;

import java.util.ArrayList;
import java.util.List;

public class Relation<T> {

    private List<T> table;

    /*
     You may add your code in the constructor
     */

    public Relation() {
        this.table = new ArrayList<T>();
    }

    public int getSize() {
        return table.size();
    }

    public void insert(T tuple) {
        table.add(tuple);
    }

    public T getTuple(int pos) {
        return table.get(pos);
    }

    public List<T> getRelation() {
        return table;
    }
}
