#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <output.txt>"
    exit 1
fi

input_file="$1"

if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' not found!"
    exit 1
fi

output_file="output.json"

test_name=$(head -n 1 "$input_file" | sed -n 's/\[ \(.*\) \], .*/\1/p')

temp_json=$(mktemp)

echo '{' > "$temp_json"
echo ' "testName": "'"$test_name"'",' >> "$temp_json"
echo ' "tests": [' >> "$temp_json"

first_test=true
while IFS= read -r line; do
    if [[ "$line" =~ ^(not\ ok|ok)[[:space:]]+[0-9]+ ]]; then
        if [[ "$line" =~ ^ok[[:space:]] ]]; then
            status="true"
        else
            status="false"
        fi
        
        temp=$(echo "$line" | sed -E 's/^(not )?ok[[:space:]]+[0-9]+[[:space:]]+//')
        test_name_part=$(echo "$temp" | sed 's/,[[:space:]]*[0-9]*ms$//')
        duration=$(echo "$temp" | grep -oE '[0-9]+ms$')
        
        if [ "$first_test" = false ]; then
            echo ',' >> "$temp_json"
        fi
        first_test=false
        
        echo '   {' >> "$temp_json"
        echo '     "name": "'"$test_name_part"'",' >> "$temp_json"
        echo '     "status": '"$status"',' >> "$temp_json"
        echo '     "duration": "'"$duration"'"' >> "$temp_json"
        echo -n '   }' >> "$temp_json"
    fi
done < "$input_file"

last_line=$(tail -n 1 "$input_file")
success=$(echo "$last_line" | grep -oE '^[0-9]+')
failed=$(echo "$last_line" | grep -oE '[0-9]+ tests failed' | grep -oE '^[0-9]+')
rating=$(echo "$last_line" | grep -oE 'rated as [0-9]+(\.[0-9]+)?%' | grep -oE '[0-9]+(\.[0-9]+)?')
total_duration=$(echo "$last_line" | grep -oE 'spent [0-9]+ms' | grep -oE '[0-9]+ms')

echo '' >> "$temp_json"
echo ' ],' >> "$temp_json"
echo ' "summary": {' >> "$temp_json"
echo '   "success": '"$success"',' >> "$temp_json"
echo '   "failed": '"$failed"',' >> "$temp_json"
echo '   "rating": '"$rating"',' >> "$temp_json"
echo '   "duration": "'"$total_duration"'"' >> "$temp_json"
echo ' }' >> "$temp_json"
echo '}' >> "$temp_json"

mv "$temp_json" "$output_file"

echo "Conversion complete! Output saved to $output_file"
