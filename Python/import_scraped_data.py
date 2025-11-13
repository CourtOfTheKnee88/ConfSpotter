import csv
import mysql.connector
from datetime import datetime
from connection import get_connection

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

# Import conference data from CSV into database
def import_conferences_from_csv(csv_file='conferences_normalized.csv'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        imported_count = 0
        skipped_count = 0
        
        print(f"Starting import from {csv_file}...")
        
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Extract and clean data
                    title = clean_text(row.get('name', ''), 255)
                    source = clean_text(row.get('source', ''))
                    link = clean_text(row.get('link', ''))
                    year = row.get('year', '').strip()
                    
                    # Skip if no title
                    if not title:
                        skipped_count += 1
                        continue
                    
                    # Handle dates - create reasonable defaults if missing
                    start_date = clean_date(row.get('start_date', ''))
                    end_date = clean_date(row.get('end_date', ''))
                    
                    # If we have a year but no specific dates, create a placeholder
                    if year and len(year) == 4 and not start_date:
                        try:
                            start_date = f"{year}-01-01 09:00:00"
                            if not end_date:
                                end_date = f"{year}-01-01 17:00:00"
                        except:
                            pass
                    
                    # Skip if we still don't have valid dates
                    if not start_date or not end_date:
                        print(f"Skipping '{title}' - missing valid dates")
                        skipped_count += 1
                        continue
                    
                    # Create description from available info
                    location = clean_text(row.get('location', ''))
                    description_parts = []
                    if source:
                        description_parts.append(f"Source: {source}")
                    if location:
                        description_parts.append(f"Location: {location}")
                    if link:
                        description_parts.append(f"Link: {link}")
                    
                    description = " | ".join(description_parts)
                    if len(description) > 500:
                        description = description[:497] + "..."
                    
                    # Insert into database
                    insert_query = """
                        INSERT IGNORE INTO Conferences (Title, Start_Date, End_Date, Descrip)
                        VALUES (%s, %s, %s, %s)
                    """
                    
                    cursor.execute(insert_query, (title, start_date, end_date, description))
                    
                    if cursor.rowcount > 0:
                        imported_count += 1
                        print(f"✓ Imported: {title}")
                    else:
                        print(f"- Skipped (duplicate): {title}")
                        skipped_count += 1
                        
                except Exception as e:
                    print(f"Error processing row: {e}")
                    print(f"Row data: {row}")
                    skipped_count += 1
                    continue
        
        conn.commit()
        print(f"\n=== Import Complete ===")
        print(f"Successfully imported: {imported_count} conferences")
        print(f"Skipped: {skipped_count} conferences")
        
        # Show current total
        cursor.execute("SELECT COUNT(*) FROM Conferences")
        total = cursor.fetchone()[0]
        print(f"Total conferences in database: {total}")
        
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close() 

if __name__ == "__main__":
    print("ConfSpotter - Import Scraped Conference Data")
    print("=" * 50)
    
    # Import the data
    import_conferences_from_csv()
