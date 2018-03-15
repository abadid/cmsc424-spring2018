package functionaldependency;

import java.util.*;

// Do not change anything in this file

class Dependency{

  // get the column name of colIndex from Table t
  private ArrayList<String> getCol(Table t, int colIndex){
    assert colIndex >= 0 && colIndex < t.colNames.size() : "INVALID COLUMN INDEX" ;
    ArrayList<String> col = new ArrayList<String>();
    for( ArrayList<String> row: t.table){
      col.add(row.get(colIndex));
    }
    return col;
  }

  // get all dependencies for every column pair (i,j)
  public void getAllDependency(Table t){
    int k=0;
    for(int i=0;i<t.colNames.size();i++){
        for(int j=0;j<t.colNames.size();j++){
          if( i!=j && CheckFD.checkDependency(getCol(t,i),getCol(t,j)) ){
            System.out.println(++k+". "+t.colNames.get(i)+"->"+t.colNames.get(j));
          }
        }
    }
  }

  // get all fuzzy dependencies for every column pair (i,j)
  public void getAllFuzzyDependency(Table t, double threshold){
    int k=0;
    for(int i=0;i<t.colNames.size();i++){
        for(int j=0;j<t.colNames.size();j++){
          if( i!=j && CheckFD.checkFuzzyDependency(getCol(t,i),getCol(t,j),threshold) ){
            System.out.println(++k+". "+t.colNames.get(i)+"->"+t.colNames.get(j));
          }
        }
    }
  }

}
