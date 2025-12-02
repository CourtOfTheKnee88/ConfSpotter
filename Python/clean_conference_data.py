# Written by Courtney Jackson
# Used AI assistance to help write in python, 
# I wrote the logic of how I wanted it to function, 
# and had AI help me with syntax and structure.
import csv
from datetime import datetime

# Converts data from CSV into the proper format for database insertion
def clean_date(date_str):
    if not date_str or date_str.strip() == '':
        return None
    
    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return None

# Cleans text fields for database insertion
def clean_text(text, max_length=None):
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    cleaned = ' '.join(text.split())
    
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length-3] + "..."
    
    return cleaned

# Clean and normalize conference data from CSV
def clean_conferences_csv(input_file='conferences.csv', output_file='conferences_normalized.csv'):
    try:
        cleaned_count = 0
        skipped_count = 0
        
        print(f"Starting cleaning from {input_file}...")
        
        # Read the input CSV and write to output CSV
        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.DictReader(infile)
            
            # Get the fieldnames from the original CSV
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                try:
                    # Create a cleaned row
                    cleaned_row = {}
                    
                    # Clean each field
                    cleaned_row['source'] = clean_text(row.get('source', ''))
                    cleaned_row['name'] = clean_text(row.get('name', ''), 255)
                    cleaned_row['link'] = clean_text(row.get('link', ''))
                    cleaned_row['year'] = row.get('year', '').strip()
                    cleaned_row['location'] = clean_text(row.get('location', ''))
                    
                    # Clean and normalize dates
                    start_date = row.get('start_date', '').strip()
                    end_date = row.get('end_date', '').strip()
                    
                    # Normalize date format if present
                    if start_date:
                        cleaned_start = clean_date(start_date)
                        if cleaned_start:
                            # Convert back to just date format (YYYY-MM-DD) for CSV
                            try:
                                date_obj = datetime.fromisoformat(cleaned_start)
                                cleaned_row['start_date'] = date_obj.strftime('%Y-%m-%d')
                            except:
                                cleaned_row['start_date'] = start_date
                        else:
                            cleaned_row['start_date'] = start_date
                    else:
                        cleaned_row['start_date'] = ''
                    
                    if end_date:
                        cleaned_end = clean_date(end_date)
                        if cleaned_end:
                            # Convert back to just date format (YYYY-MM-DD) for CSV
                            try:
                                date_obj = datetime.fromisoformat(cleaned_end)
                                cleaned_row['end_date'] = date_obj.strftime('%Y-%m-%d')
                            except:
                                cleaned_row['end_date'] = end_date
                        else:
                            cleaned_row['end_date'] = end_date
                    else:
                        cleaned_row['end_date'] = ''
                    
                    # Write the cleaned row
                    writer.writerow(cleaned_row)
                    cleaned_count += 1
                    
                    if cleaned_row['name']:
                        print(f"✓ Cleaned: {cleaned_row['name']}")
                    else:
                        print(f"✓ Cleaned row (no name)")
                        
                except Exception as e:
                    print(f"Error processing row: {e}")
                    print(f"Row data: {row}")
                    skipped_count += 1
                    continue
        
        print(f"\n=== Cleaning Complete ===")
        print(f"Successfully cleaned: {cleaned_count} conferences")
        print(f"Skipped: {skipped_count} conferences")
        print(f"Output saved to: {output_file}")
        
    except Exception as e:
        print(f"File processing error: {e}") 

if __name__ == "__main__":
    print("ConfSpotter - Clean Conference Data")
    
    # Clean the data
    clean_conferences_csv()
