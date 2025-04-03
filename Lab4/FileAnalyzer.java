import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;
import java.util.Collections;


public class FileAnalyzer {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("No argument provided");
            return;
        }

        try {
            System.out.println(formatAsJson(fileStats(args[0])));
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }

/*
        try (Scanner input = new Scanner(System.in)) {
            System.out.print("Enter a file name: ");
            String fileName = input.nextLine().trim();
            System.out.println(formatAsJson(fileStats(fileName)));
        }
            */
    }


    static private Map<String,Object> fileStats(String fileName) {
        Map<Character, Integer> characterFrequency = new HashMap<>();
        Map<String, Integer> wordFrequency = new HashMap<>();
        int totalLines = 0;
        int totalChars = 0;
        int totalWords = 0;
        File file = new File(fileName);

        try (Scanner scanner = new Scanner(file, StandardCharsets.UTF_8)) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                totalLines++;
                totalChars += line.length() + 1; //extra one for '\n'

                for (char character : line.toCharArray()) {
                    characterFrequency.put(character, characterFrequency.getOrDefault(character, 0) + 1);
                }

                String[] words = line.split("\s+");
                for (String word : words) {
                    if (!word.isEmpty()) {
                        wordFrequency.put(word, wordFrequency.getOrDefault(word, 0) + 1);
                        totalWords++;
                    }
                }
            }
        } catch (FileNotFoundException e){

        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        Entry<Character, Integer> maxCharEntry = characterFrequency.isEmpty() ? null : Collections.max(characterFrequency.entrySet(), Map.Entry.comparingByValue());
        Entry<String, Integer> maxWordEntry = wordFrequency.isEmpty() ? null : Collections.max(wordFrequency.entrySet(), Map.Entry.comparingByValue());
        
        return Map.of(
            "file_path", file.getAbsolutePath(),
            "total_characters", totalChars,
            "total_words", totalWords,
            "total_lines", totalLines,
            "most_common_character", maxCharEntry != null ? String.valueOf(maxCharEntry.getKey()) : "",
            "most_common_character_count", maxCharEntry != null ? maxCharEntry.getValue() : 0,
            "most_common_word", maxWordEntry != null ? maxWordEntry.getKey() : "",
            "most_common_word_count", maxWordEntry != null ? maxWordEntry.getValue() : 0
        );
    }

    private static String formatAsJson(Map<String, Object> map) {
        StringBuilder json = new StringBuilder();
        json.append("{\n");
    
        int count = 0;  
        int size = map.size();
        
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            json.append("  \"").append(entry.getKey()).append("\": ");
    
            Object value = entry.getValue();
            if (value instanceof String) {
                json.append("\"")
                    .append(value.toString().replace("\\", "\\\\").replace("\"", "\\\""))
                    .append("\"");
            } else if (value == null) {
                json.append("null");
            } else {
                json.append(value);
            }
    
            if (++count < size) {  // Append comma only if it's not the last element
                json.append(",");
            }
            json.append("\n");
        }
    
        json.append("}");
        return json.toString();
    }
}