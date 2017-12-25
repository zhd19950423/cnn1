/**
 * Created by Rocky on 2017/12/17.
 */
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Properties;

public class DBManager {
    private static String driver = "com.mysql.jdbc.Driver";
    private static String url = "jdbc:mysql://localhost:3306/loyal";
    private static String userName = "root";
    private static String password = "root";

//    static{
//        InputStream in = null;
//
//
//        try {
//            in = DBManager.class.getClassLoader().getResourceAsStream("jdbc.properties");
//            Properties p = new Properties();
//            p.load(in);
//            driver = p.getProperty("jdbc.driverClassName");
//            url = p.getProperty("jdbc.url");
//            userName = p.getProperty("jdbc.username");
//            password = p.getProperty("jdbc.password");
//        } catch (IOException e) {
//            // TODO Auto-generated catch block
//            e.printStackTrace();
//        }finally{
//            if(in!=null){
//                try {
//                    in.close();
//                } catch (IOException e) {
//                    // TODO Auto-generated catch block
//                    e.printStackTrace();
//                }
//            }
//        }
//    }
    public static Connection getConn(){
        Connection conn = null;
        try {
            Class.forName(driver);
            conn = DriverManager.getConnection(url, userName, password);
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return conn;
    }

}
