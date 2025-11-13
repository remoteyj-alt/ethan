import java.sql.*;

public class JdbcQuery {
    public static void main(String[] args) throws Exception {
        Class.forName("oracle.jdbc.driver.OracleDriver");
        Connection conn = DriverManager.getConnection(
            "jdbc:oracle:thin:@210.100.7.65:1521/kgcapp", "tph", "yplgcc9y");
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT SYSDATE FROM DUAL");
        while (rs.next()) {
            System.out.println(rs.getString(1));
        }
        conn.close();
    }
}
