package functionaldependency;

import java.sql.DriverManager;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.DatabaseMetaData;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.sql.Statement;

// Do not modify any other part of the code
// other than the place marked below as "TO-DO"

public class FDFinder {

	public static void main(String[] argv) {

		System.out.println("-------- PostgreSQL "
				+ "JDBC Connection Testing ------------");

		try {

			Class.forName("org.postgresql.Driver");

		} catch (ClassNotFoundException e) {

			System.out.println("Where is your PostgreSQL JDBC Driver? "
					+ "Include in your library path!");
			e.printStackTrace();
			return;

		}

		System.out.println("PostgreSQL JDBC Driver Registered!");

		Connection connection = null;

		try {

			connection = DriverManager.getConnection(
					"jdbc:postgresql://127.0.0.1:5432/fddb", "test1",
					"asdf");

		} catch (SQLException e) {

			System.out.println("Connection Failed! Check output console");
			e.printStackTrace();
			return;

		}

		if (connection != null) {
			doWork(connection);
		} else {
			System.out.println("Failed to make connection!");
		}
	}
	public static void doWork(Connection c) {
		try {
			DatabaseMetaData dbmd = c.getMetaData();
			ResultSet rs = dbmd.getColumns(null, "%", "%dataset%", "%");
			ArrayList<String> obj = new ArrayList<String>();
			ArrayList<String> aboveThreshold = new ArrayList<String>();
			while (rs.next()) {
				obj.add(rs.getString("COLUMN_NAME"));
			}
			System.out.println(obj);
			for (int i = 0; i < obj.size(); i++) {
				for (int j = 0; j < obj.size(); j++) {
					if (i != j) {
						String col1 = obj.get(i);
						String col2 = obj.get(j);
						double r = doQuery(c, col1, col2);
						System.out.println("Confidence(" + col1 + "," + col2 + ") = " + r);
						if (r > 1.5)
							aboveThreshold.add("Confidence(" + col1 + "," + col2 + ") = " + r);

					}
				}
			}
			System.out.println("Confidences above threshold:\n" + aboveThreshold);
		}
		catch (SQLException e) {
			e.printStackTrace();
		}
	}

	public static double doQuery(Connection c, String col1, String col2) {

		// TO-DO
		// Replace the existing SQL query in the string below with your SQL query.
		// Your query should return a single row with a single column
		// that contains the confidence calculation for col1 and col2 which are parameters to this method
		// In other words, your SQL query returns confidence(col1,col2)
		// Do not use stored procedures --- just a regular SQL query
		// See the README for a hint about how to cast integers as floats in Postgres (which you may need to do)

		/*String query = "select count(" + col1 + ") from dataset;";*/

		String query = "with cardinality as (select a, 1.0/count(*) as card from (select distinct "+col1 +" as a, "+col2+" as b from dataset) d group by a),";
		query+=" dup as (select dataset."+col1+" as a, dataset."+col2+" as b from dataset, (select "+col1+" ,count(*) from dataset group by "+col1+" having count("+col1+") > 1) counts where dataset."+col1 +"= counts."+col1+"), ";
		query+="consistency as (select distinct d1.a as a, 1.0*(select max(c) from (select count(*) c from dup d2 where d1.a=d2.a group by d2.b) foo)/(select count(*) from dup d2 where d1.a=d2.a group by d2.a) as const from dup d1) ";
		query+="select (select avg(card) from cardinality) + CASE WHEN (select count(*) from dup)=0 THEN 1 ELSE (select (1.0+sum(const))/(1.0+(select count(*) from consistency)) from consistency) END as confidence;";


		try {
			Statement s = c.createStatement();
			ResultSet rs = s.executeQuery(query);
			rs.next();
			return rs.getFloat(1);
		}
		catch (SQLException e) {
			e.printStackTrace();
			return 0;
		}
	}

}
