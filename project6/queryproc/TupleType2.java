package queryproc;

import java.util.Arrays;

public class TupleType2 {

    private Object[] tuple;

    public TupleType2(final int id, final int locid, final String name) {

        this.tuple = new Object[3];
        this.tuple[0] = id;
        this.tuple[1] = locid;
        this.tuple[2] = name;
    }

    // returns the attribute at position index in the tuple
    public Object getAttribute(int index) {
        return tuple[index];
    }

    // returns all attributes in the tuple
    public Object[] getAllAttributes(){
        return Arrays.copyOf(tuple, tuple.length);
    }
}
