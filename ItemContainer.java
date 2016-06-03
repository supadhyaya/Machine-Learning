package spaceSaving;



public class ItemContainer implements Comparable<ItemContainer> {

	// define the status of the items to be inserted in a data structure
	public final String item;
	public int itemFrequency;
	public int error;
	
	
	public ItemContainer(String i, int error) {
		
		item = i;
		itemFrequency = 1;
		this.error = error;
	}
	
	public void increment(){
		itemFrequency = itemFrequency + 1;
	}
	
	public String toString() {
		return item ;
	}


    @Override
    public int compareTo(ItemContainer that) {
        return 0;
    }
}
