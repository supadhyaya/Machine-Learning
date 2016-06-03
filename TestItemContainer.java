package spaceSaving;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class TestItemContainer {

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void testItemContainer() {
		
		ItemContainer ic = new ItemContainer("Sanjiv",0);
		assertEquals("Sanjiv", ic.item);
		assertEquals(0,ic.error);
	}

	@Test
	public void testIncrement() {
		
		ItemContainer ic = new ItemContainer("Sanjiv", 1);
		assertEquals(1,ic.itemFrequency);
		
	}

	@Test
	public void testCompareTo() {
		
		ItemContainer one = new ItemContainer("Sanjiv",1);
		ItemContainer two = new ItemContainer("SanjivUpadhyaya",2);
		int result = one.compareTo(two);
		assertEquals(0,result);
	}

}
