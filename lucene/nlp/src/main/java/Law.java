import org.ietf.jgss.Oid;

/**
 * Created by Rocky on 2017/12/17.
 */
public class Law {
    private String lname;
    private String ltime;
    private String lcatagory;
    Oid _id;

    public String getLname() {
        return lname;
    }

    public void setLname(String lname) {
        this.lname = lname;
    }

    public String getLtime() {
        return ltime;
    }

    public void setLtime(String ltime) {
        this.ltime = ltime;
    }

    public String getLcatagory() {
        return lcatagory;
    }

    public void setLcatagory(String lcatagory) {
        this.lcatagory = lcatagory;
    }

    public class Oid{
        String $oid;
        public String get$oid() {
            return $oid;
        }

        public void set$oid(String $oid) {
            this.$oid = $oid;
        }

    }
}
