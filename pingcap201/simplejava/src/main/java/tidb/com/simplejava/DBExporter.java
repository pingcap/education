package tidb.com.simplejava;

import java.io.*;
import java.sql.*;

public class DBExporter {
    public static void main(String[] args) {
        String jdbcURL = "jdbc:mysql://localhost:3306/customerdb";
        String username = "root";
        String password = "";

        String csvFilePath = "Customer-export.csv";

        try (Connection connection = DriverManager.getConnection(jdbcURL, username, password)) {
            String sql = "SELECT * FROM customer";

            Statement statement = connection.createStatement();

            ResultSet result = statement.executeQuery(sql);

            BufferedWriter fileWriter = new BufferedWriter(new FileWriter(csvFilePath));

            // write header line containing column names
            fileWriter.write("id, firstname,lastname,username,shirtsize");

            while (result.next()) {
                //String id= Integer.toString(result.getInt("id"));
                Integer id= result.getInt("id");
                String firstname= result.getString("first_name");
                String lastname = result.getString("last_name");
                String email = result.getString("email");
                String shirtsize= result.getString("shirtsize");

                String line = String.format("%d,%s,%s,%s,%s",
                        id, firstname, lastname, email, shirtsize);

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
