import com.google.gson.Gson;
import com.mongodb.*;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;

/**
 * Created by Rocky on 2017/12/25.
 */
public class LocalTest {
    public static void main(String args[]) throws IOException {
        MongoClient mc= new MongoClient(); //local
//        MongoClient mc= new MongoClient("192.168.68.11",30000);
        DB tset = mc.getDB("lawCase");
        DBCollection law = tset.getCollection("lawreference");
        DBCursor dbCursor = law.find();
        Gson gson=new Gson();

        MongoClient lawClient= new MongoClient();
        DB loyalDB = lawClient.getDB("loyalDB");
        DBCollection compareLaw = loyalDB.getCollection("loyalUpdata");
        while (dbCursor.hasNext()) {

            DBObject dbObject = dbCursor.next();
            LawList law1 = gson.fromJson(dbObject.toString(), LawList.class);
            for (LawForMongo lawForMongo : law1.getReferences()){
                String realName = lawForMongo.getName().replace("《","").replace("》","");
                BasicDBObject queryObject = new BasicDBObject("lname",realName);
                DBObject dbObject1 = compareLaw.findOne(queryObject);
                if (dbObject1!=null){
                    System.out.println(realName+"存在于法条数据库中");
                }
                else {
                    File indexrepository_file = new File("D:/indexFromMongoDB/");
                    Path path = indexrepository_file.toPath();
                    Directory directory = FSDirectory.open(path);
                    IndexReader indexReader = DirectoryReader.open(directory);
                    // 创建一个IndexSearcher对象
                    IndexSearcher indexSearcher = new IndexSearcher(indexReader);
                    // 创建一个查询对象
                    QueryParser parser = new QueryParser("name",new StandardAnalyzer());
                    try {
                        org.apache.lucene.search.Query query1 = parser.parse(realName);
                        System.out.println("");
                        TopDocs topDocs1 = indexSearcher.search(query1, 1);
//                        System.out.println("可能有关联的查询结果数：" + topDocs1.totalHits);
                        System.out.println("=======================");
                        ScoreDoc[] scoreDocs = topDocs1.scoreDocs;
                        System.out.println("最相近的结果是"+ indexSearcher.doc(scoreDocs[0].doc).get("name"));
//
                        indexReader.close();
                    } catch (ParseException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
}
