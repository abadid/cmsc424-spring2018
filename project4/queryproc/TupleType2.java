package queryproc;

public class TupleType2 {

    private int id;
    private int cId;
    private String cName;

    public TupleType2(final int id, final int companyId, final String companyName) {
        this.id = id;
        this.cId = companyId;
        this.cName = companyName;
    }

    public int getId() {
        return id;
    }

    public int getcId() {
        return cId;
    }

    public String getcName() {
        return cName;
    }
}
