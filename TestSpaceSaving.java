package spaceSaving;

import static org.junit.Assert.*;

import java.util.Iterator;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;




public class TestSpaceSaving {

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void testSpaceSavingAlgorithm() {
		
		SpaceSavingAlgorithm ssa = new SpaceSavingAlgorithm(5);
		assertEquals(5, ssa.getTopK());
		assertEquals(0, ssa.getNum());
		assertEquals(1, ssa.getCurrentIteration());
	}

	@Test
	public void testInsertItem() {
		
		SpaceSavingAlgorithm ssa = new SpaceSavingAlgorithm(2);
		
		String name = "Sanjiv";
		String name2 = "Upadhyaya";
		
		ItemContainer ic = new ItemContainer(name,0);
		ssa.insertItem(name);
		
		assertEquals(name,ic.item);
		assertEquals(0,ic.error);
		assertEquals(1,ic.itemFrequency);
		
		// insert a duplicate name, then the frequency should become 4 in the itemContainer
		ssa.insertItem(name);
		// Addition of a new item
		ssa.insertItem(name2);
		
		// Container should now hold the value of 4 as the frequency for the duplicate name
		for(Iterator<ItemContainer> iterators = ssa.getContainer().iterator(); iterators.hasNext();){
		ItemContainer items = iterators.next();

		System.out.println(items.item + ": "+ items.itemFrequency );
		}
		}
	
	
	@Test
	public void deleteItem() {
		
		SpaceSavingAlgorithm ss = new SpaceSavingAlgorithm(2);
		
		ss.insertItem("Sanjiv");
		ss.insertItem("NOTHING");
		ss.insertItem("Upadhyaya");
		
		for(Iterator<ItemContainer> iterators = ss.getContainer().iterator(); iterators.hasNext();) {
		ItemContainer items = iterators.next();
		assertEquals("Upadhyaya",items.item);
		}
	}
}
