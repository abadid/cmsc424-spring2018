package queryproc;

import java.util.Arrays;

public class TupleType1 {

    private Object[] tuple;

    public TupleType1(final int id, final String state, final String region) {

        this.tuple = new Object[3];
        this.tuple[0] = id;
        this.tuple[1] = state;
        this.tuple[2] = region;
    }

    // returns the attribute at position index in the tuple
    public Object getAttribute(int index) {
        return tuple[index];
    }

    // returns all attributes in the tuple
    public Object[] getAllAttributes() {
        return Arrays.copyOf(tuple, tuple.length);
    }
}
