package queryproc;

public class TupleType1 {

    private int cId;
    private String cLoc;

    public TupleType1(final int companyId, final String companyLocation) {
        this.cId = companyId;
        this.cLoc = companyLocation;
    }

    public int getcId() {
        return cId;
    }

    public String getcLoc() {
        return cLoc;
    }
}
