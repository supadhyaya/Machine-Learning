package spaceSaving;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class Source {
	
    public String[] extractWords(String file) throws IOException {
    	
        byte[] buffer = new byte[(int)new File(file).length()];
        FileInputStream fis = new FileInputStream(file);
        try {
            fis.read(buffer);
            String[] words = new String(buffer).split("[^\\w]+");
            return words;
        } finally {
            fis.close();
        }
    }
  	
}
