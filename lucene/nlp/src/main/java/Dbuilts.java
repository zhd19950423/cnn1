/**
 * Created by Rocky on 2017/12/17.
 */
import java.sql.Connection;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

import org.apache.commons.dbutils.DbUtils;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.ArrayListHandler;
import org.apache.commons.dbutils.handlers.BeanHandler;
import org.apache.commons.dbutils.handlers.BeanListHandler;
public class Dbuilts {
    public List getList(String sql, Class clazz, Object params[])throws SQLException {
        Connection conn = DBManager.getConn();
        QueryRunner runner = new QueryRunner();
        List list = (List)runner.query(conn, sql, new BeanListHandler<Object>(clazz));
        DbUtils.close(conn);
        return list;
    }
    public Object getSingle(String sql, Class clazz, Object params[])throws SQLException {
        Connection conn = DBManager.getConn();
        QueryRunner runner = new QueryRunner();
        Object objet = runner.query(conn, sql, new BeanHandler<Object>(clazz), params);
        DbUtils.close(conn);
        return objet;
    }

    public static void main(String args[]) {
        //test
        String sql ="select * from loyal";
        Dbuilts db = new Dbuilts();
        List<Law> result = null;
        try {
              result= db.getList(sql, Law.class, (Object[]) null);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        for (Law p :result){
            System.out.println(p.getLname());
        }
    }
}
