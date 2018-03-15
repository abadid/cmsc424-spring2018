package functionaldependency;

import java.util.*;
import java.io.*;

// Do not change anything in this file

class Table{

  // ArrayList<String> corresponds to each record
  // ArrayList<ArrayList<String>> corresponds to a list of records
  ArrayList<ArrayList<String>> table;
  ArrayList<String> colNames;

  // Constructor to initialize the instance variables
  Table(){
    table = new ArrayList<ArrayList<String>>();
    colNames = new ArrayList<String>();
  }

  // Getting the column names from first line of the dataset
  // and adding to the instance variable colNames
  public void getColNames(String line){
    String[] parts = line.split(",");
    for(String part: parts){
      colNames.add(part.trim());
    }
  }

  // Adding each line of the input file
  // to the instance variable table
  public void addRecord(String line){
    String[] parts = line.split(",");
    ArrayList<String> record = new ArrayList<String>();
    for(String part: parts){
      record.add(part.trim());
    }
    table.add(record);
  }

  // Loads the instance variables table
  // and colNames from the input file
  public void createTable(String fileName){
    try {
        int i=1;
        String line = null;
        FileReader fileReader = new FileReader(fileName);
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        while((line = bufferedReader.readLine()) != null) {
            if (i==1)
              getColNames(line);
            else
              addRecord(line);
            i++;
        }
        bufferedReader.close();
    }
    catch(FileNotFoundException ex) {
        System.out.println(
            "Unable to open file '" +fileName + "'");
    }
    catch(IOException ex) {
        System.out.println(
            "Error reading file '"+ fileName + "'");
    }
  }


}
