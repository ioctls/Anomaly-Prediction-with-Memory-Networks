package models;

public class Result {
	private final String sourceId;
	private final String message;
	private final String status;
	 public Result(String sourceId,String message,String status) {
	        this.sourceId = sourceId;
	        this.message=message;
	        this.status=status;
	        
	    }
	 
	

	public String getSourceId() {
		return sourceId;
	}

	public String getMessage() {
		return message;
	}

	public String getStatus() {
		return status;
	}
}
