import java.sql.*;

public class JdbcQuery {
    public static void main(String[] args) throws Exception {
        Class.forName("oracle.jdbc.driver.OracleDriver");
        Connection conn = DriverManager.getConnection(
            "jdbc:oracle:thin:@1.1.1.1:1521/123", "123", "123");
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT SYSDATE FROM DUAL");
        while (rs.next()) {
            System.out.println(rs.getString(1));
        }
        conn.close();
    }
}
