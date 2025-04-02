import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Scanner;

public class FileAnalyzer {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter a file name: ");
        String fileName = input.nextLine().trim();
        System.out.println(formatAsJson(fileStats(fileName)));



    }


    static private Map<String,Object> fileStats(String fileName) {
        Map<Character, Integer> characterFrequency = new HashMap<>();
        Map<String, Integer> wordFrequency = new HashMap<>();
        int totalLines = 0;
        int totalChars = 0;
        int totalWords = 0;
        try (Scanner scanner = new Scanner(new File(fileName), StandardCharsets.UTF_8)) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                totalLines++;
                totalChars += line.length() + 1;

                for (char character : line.toCharArray()) {
                    characterFrequency.put(character, characterFrequency.getOrDefault(character, 0) + 1);
                }

                String[] words = line.split("\\s+");
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

        Character mostCommonChar = null;
        int maxCharCount = 0;
        for (Map.Entry<Character, Integer> entry : characterFrequency.entrySet()) {
            if (entry.getValue() > maxCharCount) {
                maxCharCount = entry.getValue();
                mostCommonChar = entry.getKey();
            }
        }

        String mostCommonWord = null;
        int maxWordCount = 0;
        for (Map.Entry<String, Integer> entry : wordFrequency.entrySet()) {
            if (entry.getValue() > maxWordCount) {
                maxWordCount = entry.getValue();
                mostCommonWord = entry.getKey();
            }
        }

        Map<String, Object> stats = new LinkedHashMap<>();
        stats.put("file_path", fileName);
        stats.put("total_characters", totalChars);
        stats.put("total_words", totalWords);
        stats.put("total_lines", totalLines);
        stats.put("most_common_character", mostCommonChar != null ? String.valueOf(mostCommonChar) : null);
        stats.put("most_common_word", mostCommonWord);

        return stats;
    }

    private static String formatAsJson(Map<String, Object> map) {
        StringBuilder json = new StringBuilder();
        json.append("{\n");
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            json.append("  \"")
                    .append(entry.getKey())
                    .append("\": ");

            Object value = entry.getValue();
            if (value instanceof String) {
                json.append("\"")
                        .append(value.toString().replace("\"", "\\\""))
                        .append("\"");
            } else if (value == null) {
                json.append("null");
            } else {
                json.append(value);
            }
            json.append(",");
            json.append("\n");
        }
        json.append("\b\b\n");
        json.append("}");
        System.out.println(json.toString());
        return json.toString();
    }

}
