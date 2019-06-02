package models;

import java.time.LocalDateTime;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.ByteArraySerializer;
import com.fasterxml.jackson.datatype.jsr310.deser.LocalDateTimeDeserializer;

public class KafkaRecord {
	
	public String timestamp;
	
	public float value;
	
	public KafkaRecord() {
		super();
	}

	public KafkaRecord(String timestamp, float value) {
		super();
		this.timestamp = timestamp;
		this.value = value;
	}
}