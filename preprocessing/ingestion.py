import csv

def extract_college_data_to_csv(input_file, output_file):
    # Read input text file
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Split text into lines
    lines = text.split('\n')
    csv_data = []
    current_institute_id = None
    current_institute_name = None

    for line in lines:
        # Clean the line by removing extra whitespace and special characters
        line = line.replace('\xa0', ' ').replace('\t', ' ').strip()
        
        if line == '':
            continue

        # Check if the line starts with an Institute ID
        if line.startswith('E') and line[1:4].isdigit():
            parts = line.split(' ', 1)
            print(parts)  # Debugging line
            if len(parts) > 1:
                current_institute_id = parts[0]
                current_institute_name = parts[1]
            else:
                print(f"Warning: Unexpected line format for institute information: {line}")
                continue
        elif line.startswith('-'):
            # Skip lines with only hyphens
            continue
        else:
            # Process branch data
            branch_code = line[:2]
            cutoff_values = []
            elements = line[2:].split()
            
            # Skip branch name, get rest
            for element in elements:
                if element.isdigit() or element == '--':
                    cutoff_values.append(element if element.isdigit() else '')
            
            row = [current_institute_id, current_institute_name, branch_code] + cutoff_values
            csv_data.append(row)

    # Write the data to a CSV file
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['InstituteId', 'InstituteName', 'BranchCode', '1G', '1K', '1R', '2AG', '2AK', '2AR', '2BG', '2BK', '2BR', '3AG', '3AK', '3AR', '3BG', '3BK', '3BR', 'GM', 'GMK', 'GMR', 'SCG', 'SCK', 'SCR', 'STG', 'STK', 'STR']
        writer.writerow(header)
        writer.writerows(csv_data)

# Example usage
input_file = 'ingestion_data/input.txt'
output_file = 'test.csv'
extract_college_data_to_csv(input_file, output_file)

print(f"Data has been written to {output_file}")