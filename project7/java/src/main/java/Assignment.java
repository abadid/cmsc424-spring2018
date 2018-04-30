import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.api.java.*;
import scala.Tuple2;
import org.json.*;
import java.util.*;

public class Assignment {

    public static void main(String[] args) {
        SparkSession spark = SparkSession.builder().appName("Project 7").getOrCreate();
        JavaSparkContext jsc = new JavaSparkContext(spark.sparkContext());
        jsc.setLogLevel("OFF");

        JavaRDD<String> playRDD = jsc.textFile("/vagrant/datafiles/play.txt");
        JavaRDD<String> nobelRDD = jsc.textFile("/vagrant/datafiles/prize.json");
        JavaRDD<String> logsRDD = jsc.textFile("/vagrant/datafiles/NASA_logs_sample.txt");
        JavaRDD<String> amazonInputRDD = jsc.textFile("/vagrant/datafiles/amazon-ratings.txt");
        JavaPairRDD<String, String> amazonBipartiteRDD = amazonInputRDD.map(x -> x.split(" ")).mapToPair(x -> new Tuple2<String, String>(x[0], x[1])).distinct();
        JavaRDD<FlewonTuple> flewonRDD = jsc.textFile("/vagrant/datafiles/flewon.csv").map(line -> {
            String[] attributes = line.split(",");
            return new FlewonTuple(attributes[0], attributes[1], attributes[2]);
        });

        // Task 1
        System.out.println("*** Task 1 ***");
        JavaPairRDD<String, Integer> resultTask1 = Tasks.task1(playRDD);
        if (resultTask1 != null) {
            resultTask1.foreach(x -> System.out.println(x));
        } else {
            System.out.println("No result.");
        }
        System.out.println();

        // Task 2
        System.out.println("*** Task 2 ***");
        JavaRDD<Integer> resultTask2 = nobelRDD.map(line -> new JSONObject(line)).flatMap(json -> Tasks.task2(json));
        if (resultTask2 != null) {
            resultTask2.foreach(x -> System.out.println(x));
        } else {
            System.out.println("No result.");
        }
        System.out.println();

        // Task 3
        System.out.println("*** Task 3 ***");
        JavaPairRDD<String, Iterable<Integer>> resultTask3 = Tasks.task3(nobelRDD);
        if (resultTask3 != null) {
            resultTask3.foreach(x -> System.out.println(x));
        } else {
            System.out.println("No result.");
        }
        System.out.println();

        // Task 4
        System.out.println("*** Task 4 ***");
        List<String> hosts = new ArrayList<String>();
        hosts.add("/facilites/vab.html");
        hosts.add("/images/vab-small.gif");
        JavaRDD<String> resultTask4 = Tasks.task4(logsRDD, hosts);
        if (resultTask4 != null) {
            resultTask4.foreach(x -> System.out.println(x));
        } else {
            System.out.println("No result.");
        }
        System.out.println();

        // Task 5
        System.out.println("*** Task 5 ***");
        JavaPairRDD<Long, Long> resultTask5 = Tasks.task5(amazonBipartiteRDD);
        if (resultTask5 != null) {
            resultTask5.foreach(x -> System.out.println(x));
        } else {
            System.out.println("No result.");
        }
        System.out.println();

        // Task 6
        System.out.println("*** Task 6 ***");
        JavaPairRDD<String, Tuple2<Iterable<String>, Iterable<String>>> resultTask6 = Tasks.task6(logsRDD, "ppp199.aix.or.jp", "drjo002a099.embratel.net.br");
        if (resultTask6 != null) {
            resultTask6.foreach(x -> System.out.println(x));
        } else {
            System.out.println("No result.");
        }
        System.out.println();

        // Task 7
        System.out.println("*** Task 7 ***");
        JavaPairRDD<String, Long> resultTask7 = Tasks.task7(nobelRDD);
        if (resultTask7 != null) {
            resultTask7.foreach(x -> System.out.println(x));
        } else {
            System.out.println("No result.");
        }
        System.out.println();

        // Task 8
        System.out.println("*** Task 8 ***");
        JavaRDD<Tuple2<String, Long>> resultTask8 = Tasks.task8(flewonRDD, 2, 2);
        if (resultTask8 != null) {
            resultTask8.foreach(x -> System.out.println(x));
        } else {
            System.out.println("No result.");
        }
        System.out.println();

        spark.stop();
    }

}
