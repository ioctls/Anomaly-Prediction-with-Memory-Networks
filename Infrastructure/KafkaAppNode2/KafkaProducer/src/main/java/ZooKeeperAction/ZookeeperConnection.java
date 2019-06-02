package ZooKeeperAction;
import java.io.IOException;
import java.util.concurrent.CountDownLatch;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.Watcher.Event.KeeperState;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.AsyncCallback.StatCallback;
import org.apache.zookeeper.KeeperException.Code;
import org.apache.zookeeper.data.Stat;
public class ZookeeperConnection {
	private ZooKeeper zoo;
	final CountDownLatch connectedSignal = new CountDownLatch(1);
	 // Method to connect zookeeper ensemble.
	public ZooKeeper connect(String host) throws IOException,InterruptedException {
		
	      zoo = new ZooKeeper(host,10000,new Watcher() {
			
	         public void process(WatchedEvent we) {

	            if (we.getState() == KeeperState.SyncConnected) {
	               connectedSignal.countDown();
	            }
	         }
	      });
			
	      connectedSignal.await();
	      return zoo;
	   }

	   // Method to disconnect from zookeeper server
    public void close() throws InterruptedException {
	      zoo.close();
	   }
	
	
}
