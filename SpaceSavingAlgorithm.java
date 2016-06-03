package spaceSaving;


import com.google.common.collect.Lists;

import java.io.IOException;
import java.io.Serializable;
import java.util.*;

// interface might not be required
public class SpaceSavingAlgorithm implements Serializable {
	
	private int num; // Number of elements in the data structure
	private int currentIteration; // After n elements are added and data structure is full, new iteration begins
	private int topK;  // User specified top n elements 
	private final List<ItemContainer> container = Lists.newArrayList(); // Top elements container

	// Getter and setter for the testing purpose
	public int getNum() {
		return num;
	}

	public int getCurrentIteration() {
		return currentIteration;
	}

	public int getTopK() {
		return topK;
	}

	public List<ItemContainer> getContainer() {
		return container;
	}
	

	public SpaceSavingAlgorithm(int size) {
		topK = size ;
		num = 0; // initially all the counts are zero
		currentIteration = 1;
	}
	
	
	public synchronized void insertItem(String item) {	
		findOrInsert(item);
		 if(num % topK == 0) { 			// Check if the data structure is full or not
			deleteItem();	 	 		//  Deletion of items whose frequency is less than the current iteration 
			currentIteration++; 
		}
	}
	
	
	private void findOrInsert(String items) {
		ItemContainer item = null;
		for(ItemContainer it : container) {
			if(it.item.equalsIgnoreCase(items)) {
				it.increment();
				//System.out.println("Existing item: "+it.item + " frequency:"+it.item);	
			}
	}
		if(item == null){
			item = new ItemContainer(items, currentIteration - 1);
			container.add(item);
			num++;
			//System.out.println(" Added Item: "+item.item + " frequency:"+item.itemFrequency + " error:"+item.error);
		}
	}
	
	
	public void deleteItem() {
		for(Iterator<ItemContainer> iterators = container.iterator(); iterators.hasNext();) {
			ItemContainer items = iterators.next();
			if(items.itemFrequency  < currentIteration -1) {
				iterators.remove();
				//System.out.println("Removed item: "+items.item +" error: "+items.error+ " CurrentIteration:" + currentIteration);
			}
		}
	}
	
	
	public synchronized  Set<String> topKItems() {	
		Set<String> st = new HashSet<String>();
		for(Iterator<ItemContainer> iterators = container.iterator();iterators.hasNext();){
			ItemContainer items = iterators.next();
			st.add(items.item);
		}
		return st;
	}
	
	
	 public static void main(String[] args) throws IOException {
		 	int topKItem = Integer.parseInt(args[0]);
		 	String filename = args[1];
	        SpaceSavingAlgorithm buckets = new SpaceSavingAlgorithm(topKItem);
	        Source src = new Source();
	        String[] words = src.extractWords(filename);
			 
	        for (String item: words) {
	        	buckets.insertItem(item);
	        }
	        System.out.println(buckets.topKItems());
	    }
	
}
