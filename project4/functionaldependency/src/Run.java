
package functionaldependency;

// Do not change anything in this file

public class Run {
  public static void main(String args[]){

    if (args.length != 2){
      System.out.println("Usage : java -ea -cp ./src functionaldependency.Test path-to-file threshold");
      System.exit(0);
    }

    double threshold = Double.parseDouble(args[1]);
    Table t = new Table();
    t.createTable(args[0]);
    Dependency d = new Dependency();
    System.out.println("\n------------Function Dependency-------------\n");
    d.getAllDependency(t);
    System.out.println("\n------------Fuzzy Function Dependency-------------\n");
    d.getAllFuzzyDependency(t,threshold);
    System.out.println("\n---------------------------------------------\n");
  }

}
