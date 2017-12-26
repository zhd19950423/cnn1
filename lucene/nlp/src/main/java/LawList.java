import java.util.List;

/**
 * Created by Rocky on 2017/12/25.
 */
public class LawList {
    List<LawForMongo> references;

    public List<LawForMongo> getReferences() {
        return references;
    }

    public void setReferences(List<LawForMongo> references) {
        this.references = references;
    }

    Oid _id;
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
