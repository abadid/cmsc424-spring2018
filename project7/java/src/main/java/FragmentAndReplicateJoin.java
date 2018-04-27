import org.apache.spark.api.java.*;
import scala.*;

public class FragmentAndReplicateJoin {

    /*
     * Joins leftRelation and rightRelation using the fragment-and-replicate join algorithm. Your implementation should partition
     * leftRelation into n partitions and rightRelation into m partitions.
     */
    public static JavaRDD<Tuple4<String, Double, String, Double>> fragmentAndReplicateJoin(JavaRDD<Tuple2<String, Double>> leftRelation, int n, JavaRDD<Tuple2<String, Double>> rightRelation, int m) {
        return null;
    }

}
