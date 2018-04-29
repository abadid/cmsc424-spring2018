import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.api.java.*;
import scala.Tuple2;
import org.json.*;
import java.util.*;

public class Wordcount {

    public static void main(String[] args) {
        SparkSession spark = SparkSession.builder().appName("Wordcount").getOrCreate();
        JavaSparkContext jsc = new JavaSparkContext(spark.sparkContext());
        jsc.setLogLevel("OFF");

        // Read the contents of README.md as a RDD
        JavaRDD<String> textFile = jsc.textFile("/vagrant/README.md");

        // Split each line of the file into words
        JavaRDD<String> words = textFile.flatMap(line -> line.split(" "));

        // Initialize the count of each word to 1
        JavaPairRDD<String, Long> initCounts = words.map(word -> new Tuple2<String, Long>(word, 1L));

        // Count the number of occurrences of each word
        JavaPairRDD<String, Long> counts = initCounts.reduceByKey((c1, c2) -> c1 + c2);

        // Print out the result
        counts.foreach(kvp -> System.out.println(kvp));

        spark.stop();
    }

}
