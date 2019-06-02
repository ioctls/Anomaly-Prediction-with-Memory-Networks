package kafka;

import java.util.Map;

import org.apache.kafka.common.serialization.Serializer;

import com.fasterxml.jackson.databind.ObjectMapper;

import models.KafkaRecord;

public class CustomSerializer implements Serializer<KafkaRecord> {

	public void close() {
		
	}

	public void configure(Map<String, ?> arg0, boolean arg1) {
			
	}

	public byte[] serialize(String arg0, KafkaRecord data) {
		byte[] retVal = null;
        ObjectMapper objectMapper = new ObjectMapper();
        try 
        {
        	retVal = objectMapper.writeValueAsString(data).getBytes();
        } 
        catch (Exception exception) 
        {
        	System.out.println("Error in serializing object"+ data);
        }
        return retVal;
	}

}
