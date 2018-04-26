package queryproc;

public class TupleType3 {

    private Object[] tuple;

    public TupleType3(final int idleft, final String state, final String region, final int idright, final int locid, final String name) {

        this.tuple = new Object[6];
        this.tuple[0] = idleft;
        this.tuple[1] = state;
        this.tuple[2] = region;
        this.tuple[3] = idright;
        this.tuple[4] = locid;
        this.tuple[5] = name;
    }

    public TupleType3(final Object[] lt, final Object[] rt) {

        this.tuple = new Object[6];
        System.arraycopy(lt, 0, tuple, 0, lt.length);
        System.arraycopy(rt, 0, tuple, 3, rt.length);
    }

    // returns the attribute at position index in the tuple
    public Object getAttribute(int index) {
        return tuple[index];
    }
}
