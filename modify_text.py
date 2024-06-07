import re

def remove_format(line, format_to_remove):
    cleaned_line = re.sub(format_to_remove, '', line)
    cleaned_line = re.sub(r'Difficult words:.*?\.', '', cleaned_line, flags=re.IGNORECASE)  
    return cleaned_line

def remove(input_text):
    unique_lines = set()
    unique_data = []

    for line in input_text:
        if len(line) > 15 and line not in unique_lines:
            unique_lines.add(line)
            unique_data.append(line)

    return unique_data

def merge_lines(text):
    merged_text = re.sub(r'(\d+\.)\s*\n\s*(\d+)', r'\1\2', text)
    return merged_text

with open("data.txt", 'r', encoding='utf-8') as text_file:
    lines = text_file.readlines()

    processed_lines = []
    for i in range(len(lines)):
        line = lines[i]

        cleaned_line = remove_format(line, r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}')  
        processed_lines.append(cleaned_line)

cleaned_data_unique = remove(processed_lines)
merged_text = merge_lines(''.join(cleaned_data_unique))

with open("data_update.txt", 'w', encoding='utf-8') as output_file:
    output_file.write(merged_text)
