
package functionaldependency;

import java.lang.*;

// Do not change anything in this file

public class Test {

  // Test Output for threshold=0.8
  public static void printTestOutput(){
    System.out.println("\n Expected Output \n");
    System.out.println("\n------------Function Dependency-------------\n");
    System.out.println("\n1. id2->id1\n2. id2->id3\n3. id3->id1\n4. id3->id2\n");
    System.out.println("\n------------Fuzzy Function Dependency-------------\n");
    System.out.println("\n1. id1->id2\n2. id1->id3\n3. id2->id1\n4. id2->id3\n5. id3->id1\n6. id3->id2\n");
    System.out.println("\n---------------------------------------------\n");
  }

  public static void main(String args[]){

    if (args.length != 2){
      System.out.println("Usage : java -ea -cp ./src functionaldependency.Test ./test.csv 0.8");
      System.exit(0);
    }

    double threshold = Double.parseDouble(args[1]);
    Table t = new Table();
    t.createTable(args[0]);
    Dependency d = new Dependency();

    printTestOutput();
    System.out.println("\n Your Output \n");
    System.out.println("\n------------Function Dependency-------------\n");
    d.getAllDependency(t);
    System.out.println("\n------------Fuzzy Function Dependency-------------\n");
    d.getAllFuzzyDependency(t,threshold);
    System.out.println("\n---------------------------------------------\n");
  }

}
