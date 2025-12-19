#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <accounts.csv>"
    exit 1
fi

input_file="$1"

if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' not found!"
    exit 1
fi

output_file="accounts_new.csv"

capitalize_name() {
    local name="$1"
    local result=""
    local IFS=' '
    
    for word in $name; do
        if [[ "$word" == *-* ]]; then
            local hyphen_result=""
            local old_ifs="$IFS"
            IFS='-'
            for part in $word; do
                capitalized=$(echo "${part:0:1}" | tr '[:lower:]' '[:upper:]')$(echo "${part:1}" | tr '[:upper:]' '[:lower:]')
                if [[ -z "$hyphen_result" ]]; then
                    hyphen_result="$capitalized"
                else
                    hyphen_result="$hyphen_result-$capitalized"
                fi
            done
            IFS="$old_ifs"
            word="$hyphen_result"
        else
            word=$(echo "${word:0:1}" | tr '[:lower:]' '[:upper:]')$(echo "${word:1}" | tr '[:upper:]' '[:lower:]')
        fi
        
        if [[ -z "$result" ]]; then
            result="$word"
        else
            result="$result $word"
        fi
    done
    
    echo "$result"
}

temp_count="/tmp/email_count_$$"
> "$temp_count"

while IFS= read -r line; do
    if [[ "$line" =~ ^id, ]] || [[ "$line" == "id,"* ]]; then
        continue
    fi
    
    if [[ -z "$line" ]]; then
        continue
    fi
    
    name=$(echo "$line" | cut -d',' -f3)
    
    if [[ -z "$name" ]]; then
        continue
    fi
    
    first_name=$(echo "$name" | awk '{print $1}')
    last_name=$(echo "$name" | awk '{print $NF}')
    
    first_letter=$(echo "${first_name:0:1}" | tr '[:upper:]' '[:lower:]')
    last_lower=$(echo "$last_name" | tr '[:upper:]' '[:lower:]')
    base_email="${first_letter}${last_lower}"
    
    echo "$base_email" >> "$temp_count"
done < "$input_file"

{
    while IFS= read -r line; do
        if [[ "$line" =~ ^id, ]] || [[ "$line" == "id,"* ]]; then
            echo "$line"
            continue
        fi
        
        if [[ -z "$line" ]]; then
            continue
        fi
        
        id=$(echo "$line" | cut -d',' -f1)
        location_id=$(echo "$line" | cut -d',' -f2)
        name=$(echo "$line" | cut -d',' -f3)
        
        rest=$(echo "$line" | cut -d',' -f4-)
        title=$(echo "$rest" | rev | cut -d',' -f3- | rev)
        
        formatted_name=$(capitalize_name "$name")
        
        first_name=$(echo "$name" | awk '{print $1}')
        last_name=$(echo "$name" | awk '{print $NF}')
        
        first_letter=$(echo "${first_name:0:1}" | tr '[:upper:]' '[:lower:]')
        last_lower=$(echo "$last_name" | tr '[:upper:]' '[:lower:]')
        base_email="${first_letter}${last_lower}"
        
        count=$(grep -c "^${base_email}$" "$temp_count")
        
        if [ "$count" -eq 1 ]; then
            new_email="${base_email}@abc.com"
        else
            new_email="${base_email}${location_id}@abc.com"
        fi
        
        department=$(echo "$line" | rev | cut -d',' -f1 | rev)
        
        echo "$id,$location_id,$formatted_name,$title,$new_email,$department"
    done < "$input_file"
} > "$output_file"

rm -f "$temp_count"

echo "Processing complete! Output saved to $output_file"
