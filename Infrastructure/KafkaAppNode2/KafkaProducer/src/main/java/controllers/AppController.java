package controllers;


import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import ZooKeeperAction.ZookeeperConnection;
import kafka.CustomSerializer;
import models.KafkaRecord;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.ZooDefs;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.Properties;
import java.util.Set;
import java.util.concurrent.ExecutionException;

import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.CreateTopicsResult;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.errors.TopicExistsException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaAdmin;

import models.Result;

/**
 * Hello world!
 *
 */

@Controller
public class AppController 
{	
	
	@Autowired
	private KafkaAdmin KafkaAdmin;
	final short replicationFactor = 1;
	private static ZooKeeper zk;
	private static ZookeeperConnection zoo;
	
	
	
	@PostMapping("/register")
    @ResponseBody
    public Result register(@RequestParam(name="sourceID",required=true) String sourceID)
    {	try {
		AdminClient client = AdminClient.create(KafkaAdmin.getConfig());
    	final NewTopic newTopic = new NewTopic("Source-"+sourceID, 1, replicationFactor);
    	CreateTopicsResult createTopicsResult=client.createTopics(Collections.singleton(newTopic));
    	createTopicsResult.values().get("Source-"+sourceID).get();
		}
   
    catch (InterruptedException | ExecutionException e) {
    	 if ((e.getCause() instanceof TopicExistsException)) {
            return new Result(sourceID,"Topic 'Source-"+sourceID+"' already exists.","error"); 
         }
    	e.printStackTrace();
			// TODO Auto-generated catch block
    	
		}
    return new Result(sourceID,"Register Complete","success");
    }	
	
	@PostMapping("/stream")
    @ResponseBody
    public Result stream(@RequestParam(name="sourceID",required=true) String sourceID,@RequestParam(name="data",required=true) String data)
    {
		try {
		String topic = "Source-"+sourceID;
		AdminClient client = AdminClient.create(KafkaAdmin.getConfig());
		Set<String> topics=client.listTopics().names().get();
		boolean contains = topics.contains(topic);
		if (contains) {
			System.out.println("value"+data);
			Properties props = new Properties();
			props.put("bootstrap.servers", "152.46.18.218:9092,152.46.16.141:9092");
			props.put("acks", "all");
			props.put("retries", 0);
			props.put("batch.size", 16384);
			props.put("linger.ms", 1);
			props.put("buffer.memory", 33554432);
			props.put("key.serializer", 
			         "org.apache.kafka.common.serialization.StringSerializer");
			props.put("value.serializer", 
			         CustomSerializer.class.getName());
			
			Producer<String, KafkaRecord> producer = new KafkaProducer
			         <String, KafkaRecord>(props);
			Date date = new Date();
			String key = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(date);
			KafkaRecord kf = new KafkaRecord(key, Float.parseFloat(data));
           
		
			
			producer.send(new ProducerRecord<String, KafkaRecord>(topic, kf));

		}
		else {
			return new Result(sourceID,"Topic does not exists.","error");
		}
		
		}
   
    catch (Exception e) {
    	 
    	e.printStackTrace();
			// TODO Auto-generated catch block
    	
		}
    return new Result(sourceID,"data sent","success");
    }
	
	
	@PostMapping("/activate")
    @ResponseBody
    public Result activate(@RequestParam(name="sourceID",required=true) String sourceID)
    {
		
		zoo=new ZookeeperConnection();
		try {
			zk=zoo.connect("152.46.18.218:2181,152.46.16.141:2181" );
		String topic = "Source-"+sourceID;
		Stat stat = zk.exists("/inactiveProducer/"+topic, false);
		Stat stat2= zk.exists("/activeProducer/"+topic, false);
		if (stat!=null)
		{
			zk.delete("/inactiveProducer/"+topic, stat.getVersion());
		}else {
			if (stat2!=null)
			{
				return  new Result(sourceID,"Source already active","error");	
			}
			
		}
		zk.create("/activeProducer/"+topic, null, ZooDefs.Ids.OPEN_ACL_UNSAFE,CreateMode.PERSISTENT);
		//Runtime.getRuntime().exec("ssh  cmachan@152.46.19.38 java -jar ingestion.jar "+topic+" & ");
		//Runtime.getRuntime().exec("ssh  cmachan@152.46.19.38 java -jar prediction.jar "+topic+" & ");
		
		}
   
    catch (Exception e) {
    	 
    	e.printStackTrace();
			// TODO Auto-generated catch block
    	
		}
    return new Result(sourceID,"success","success");
    }
	
	
	@PostMapping("/inactivate")
    @ResponseBody
    public Result inactivate(@RequestParam(name="sourceID",required=true) String sourceID)
    {  	Date date = Calendar.getInstance().getTime();  
    	DateFormat dateFormat = new SimpleDateFormat("yyyy-mm-dd hh:mm:ss");  
    	String strDate = dateFormat.format(date);  
		
		zoo=new ZookeeperConnection();
		try {
			zk=zoo.connect("152.46.18.218:2181,152.46.16.141:2181" );
		String topic = "Source-"+sourceID;
		Stat stat = zk.exists("/inactiveProducer/"+topic, false);
		Stat stat2= zk.exists("/activeProducer/"+topic, false);
		if (stat2==null && stat==null)
		{		return new Result(sourceID,"Source not present","error");	
			
		}else {
			if (stat2!=null) {
			zk.delete("/activeProducer/"+topic, stat2.getVersion());
			}
			if (stat!=null)
			{
				zk.setData("/inactiveProducer/"+topic,strDate.getBytes(),stat.getVersion());
			}else {
				zk.create("/inactiveProducer/"+topic, strDate.getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE,CreateMode.PERSISTENT);
					
			}
			
		}
		
		}
   
    catch (Exception e) {
    	 
    	e.printStackTrace();
			// TODO Auto-generated catch block
    	
		}
    return new Result(sourceID,"success","success");
    }
}
