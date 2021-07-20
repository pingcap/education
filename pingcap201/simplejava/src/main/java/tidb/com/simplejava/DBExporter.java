package tidb.com.simplejava;

import java.io.*;
import java.sql.*;

public class DBExporter {
    public static void main(String[] args) {
        String jdbcURL = "jdbc:mysql://localhost:3306/CustomerDB";
        String username = "root";
        String password = "";

        String csvFilePath = "Customer-export.csv";

        try (Connection connection = DriverManager.getConnection(jdbcURL, username, password)) {
            String sql = "SELECT * FROM customer";

            Statement statement = connection.createStatement();

            ResultSet result = statement.executeQuery(sql);

            BufferedWriter fileWriter = new BufferedWriter(new FileWriter(csvFilePath));

            // write header line containing column names
            fileWriter.write("id, firstname,lastname,username,membership");

            while (result.next()) {
                //String id= Integer.toString(result.getInt("id"));
                Integer id= result.getInt("id");
                String firstname= result.getString("firstname");
                String lastname = result.getString("lastname");
                String customerUsername = result.getString("username");
                String membership= result.getString("membership");

                String line = String.format("%d,%s,%s,%s,%s",
                        id, firstname, lastname, username, membership);

                fileWriter.newLine();
                fileWriter.write(line);
            }

            statement.close();
            fileWriter.close();

        } catch (SQLException e) {
            System.out.println("Datababse error:");
            e.printStackTrace();
        } catch (IOException e) {
            System.out.println("File IO error:");
            e.printStackTrace();
        }

    }
}
