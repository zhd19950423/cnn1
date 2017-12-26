import com.google.gson.Gson;
import com.mongodb.*;

import java.sql.SQLException;
import java.util.List;

/**
 * Created by Rocky on 2017/12/17.
 */
public class TestDB {
    public static boolean isRepeat(String name){
        MongoClient mc= new MongoClient();
        DB tset = mc.getDB("loyalDB");
        DBCollection law = tset.getCollection("loyalUpdata");
        BasicDBObject queryObject = new BasicDBObject("lname",name);
        DBObject dbObject = law.findOne(queryObject);
        Gson gson=new Gson();
//        Law law1= gson.fromJson(dbObject.toString(), Law.class);
        if (dbObject!=null){
            return true;
        }
        else return false;
    }

    public static void updataData(String name,String category,String time){
        MongoClient mc= new MongoClient();
        DB tset = mc.getDB("loyalDB");
        DBCollection law = tset.getCollection("loyalUpdata");
        DBObject updatedValue=new BasicDBObject();
        DBObject updateCondition=new BasicDBObject();
        updateCondition.put("lname",name);
        updatedValue.put("lcatagory", category);
        updatedValue.put("ltime",time);
        DBObject updateSetValue=new BasicDBObject("$set",updatedValue);
        law.update(updateCondition,updateSetValue);

    }
    public static void insertData(String name,String category,String time){
        MongoClient mc= new MongoClient();
        DB tset = mc.getDB("loyalDB");
        DBCollection law = tset.getCollection("loyalUpdata");
        DBObject insertValue=new BasicDBObject();
        insertValue.put("lname",name);
        insertValue.put("lcatagory", category);
        insertValue.put("ltime",time);

        law.insert(insertValue);

    }
    public static void main(String args[]) {

    }


}
