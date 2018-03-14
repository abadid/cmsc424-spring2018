package queryproc;

public class TupleType3 {

    private int cId;
    private String cLoc;
    private int id;
    private int c_Id;
    private String cName;

    public TupleType3(int companyId, String companyLocation, int id, int company_Id, String companyName) {
        this.cId = companyId;
        this.cLoc = companyLocation;
        this.id = id;
        this.c_Id = company_Id;
        this.cName = companyName;
    }

    public int getcId() {
        return cId;
    }

    public String getcLoc() {
        return cLoc;
    }

    public int getId() {
        return id;
    }

    public int getc_Id() {
        return c_Id;
    }

    public String getcName() {
        return cName;
    }
}
