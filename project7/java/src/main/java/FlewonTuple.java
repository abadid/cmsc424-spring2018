
public class FlewonTuple {
    private String flightid;
    private String customerid;
    private String flightdate;

    public FlewonTuple(String flightid, String customerid, String flightdate) {
        this.flightid = flightid;
        this.customerid = customerid;
        this.flightdate = flightdate;
    }

    public String getFlightID() {
        return this.flightid;
    }

    public String getCustomerID() {
        return this.customerid;
    }

    public String getFlightDate() {
        return this.flightdate;
    }

    public String toString() {
        return "(" + this.flightid + ", " + this.customerid + ", " + this.flightdate + ")";
    }
}
