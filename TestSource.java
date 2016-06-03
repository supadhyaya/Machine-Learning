package spaceSaving;

import static org.junit.Assert.*;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Arrays;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class TestSource {

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void testExtractWords() throws IOException {
		
		Source src = new Source();
		String file = "/Users/sanjivupadhyaya/Desktop/java/send_MBR/test.txt";
		String[] words = src.extractWords(file);
		assertEquals("sanjiv",words[1]);
		}
}