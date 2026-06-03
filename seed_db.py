"""
Data seeding script for Forty Hadith Annawawi.
Downloads hadith data from hadith-json repository and imports into the database.
"""

import os
import sys
import json
import requests
from datetime import datetime
from app import create_app, db
from app.models import Hadith

# Create app context
app = create_app(os.getenv('FLASK_ENV', 'development'))

# URLs to hadith data (primary and fallback)
HADITH_JSON_URLS = [
    "https://uthumany.github.io/nawawi-40-hadiths/api/hadiths.json",  # Primary source
    "https://raw.githubusercontent.com/uthumany/nawawi-40-hadiths/main/data/hadiths.json",  # Fallback
]

def download_hadith_json():
    """Download hadith JSON from repository with fallback URLs"""
    for url in HADITH_JSON_URLS:
        print(f"📥 Downloading hadith data from: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            print("✅ Downloaded successfully!")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Failed to download from {url}: {e}")
            continue
    
    print("❌ Error: Could not download hadith data from any source")
    return None

def parse_hadith_data(hadith_json):
    """
    Parse hadith JSON data and extract relevant fields.
    Returns a list of hadith dictionaries ready for database insertion.
    """
    print("\n🔍 Parsing hadith data...")
    hadiths = []
    
    if not hadith_json:
        print("❌ No data to parse")
        return hadiths
    
    # Check if it's a list or dict
    if isinstance(hadith_json, list):
        hadith_list = hadith_json
    elif isinstance(hadith_json, dict) and 'hadiths' in hadith_json:
        hadith_list = hadith_json['hadiths']
    elif isinstance(hadith_json, dict) and 'data' in hadith_json:
        hadith_list = hadith_json['data']
    elif isinstance(hadith_json, dict):
        # Try to find hadiths in the dict
        for key in ['items', 'content', 'hadiths', 'data']:
            if key in hadith_json and isinstance(hadith_json[key], list):
                hadith_list = hadith_json[key]
                break
        else:
            hadith_list = list(hadith_json.values())[0] if hadith_json else []
    else:
        print("❌ Unexpected JSON structure")
        return hadiths
    
    print(f"Found {len(hadith_list)} hadiths in JSON")
    
    for hadith in hadith_list:
        try:
            # Extract and normalize fields - try multiple possible field names
            hadith_number = (
                hadith.get('id') or 
                hadith.get('number') or 
                hadith.get('hadithNumber') or
                hadith.get('hadith_number') or
                hadith.get('no')
            )
            
            arabic_text = (
                hadith.get('ar_text') or 
                hadith.get('arabic') or 
                hadith.get('text_ar') or 
                hadith.get('arabicText') or
                hadith.get('text') or
                ""
            )
            
            english_text = (
                hadith.get('en_text') or 
                hadith.get('english') or 
                hadith.get('englishText') or
                hadith.get('translation') or
                hadith.get('text') or
                ""
            )
            
            narrator = (
                hadith.get('narrator') or 
                hadith.get('grading') or 
                hadith.get('source') or
                ""
            )
            
            # Skip if missing critical fields
            if not hadith_number or not english_text:
                continue
            
            hadith_obj = {
                'hadith_number': int(hadith_number),
                'arabic_text': arabic_text.strip() if arabic_text else "Arabic text not available",
                'english_text': english_text.strip(),
                'narrator': narrator.strip() if narrator else "Unknown",
                'book_reference': 'Book 15: Forty Hadith of al-Nawawi',
                'source_url': f'https://sunnah.com/nawawi/{hadith_number}'
            }
            
            hadiths.append(hadith_obj)
        except Exception as e:
            print(f"⚠️  Error parsing hadith {hadith.get('id', 'unknown')}: {e}")
            continue
    
    # Sort by hadith number
    hadiths.sort(key=lambda x: x['hadith_number'])
    print(f"✅ Parsed {len(hadiths)} valid hadiths")
    
    return hadiths

def seed_database(hadiths):
    """Insert hadith data into the database"""
    with app.app_context():
        print("\n💾 Seeding database with hadith data...")
        
        # Check if hadiths already exist
        existing_count = Hadith.query.count()
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} hadiths!")
            confirm = input("Do you want to replace them? (yes/no): ")
            if confirm.lower() != 'yes':
                print("❌ Operation cancelled.")
                return False
            
            # Delete existing hadiths
            Hadith.query.delete()
            db.session.commit()
            print("✅ Old data cleared")
        
        # Insert new hadiths
        try:
            for hadith_data in hadiths:
                hadith = Hadith(
                    hadith_number=hadith_data['hadith_number'],
                    arabic_text=hadith_data['arabic_text'],
                    english_text=hadith_data['english_text'],
                    narrator=hadith_data['narrator'],
                    book_reference=hadith_data['book_reference'],
                    source_url=hadith_data['source_url']
                )
                db.session.add(hadith)
            
            db.session.commit()
            print(f"✅ Successfully inserted {len(hadiths)} hadiths into database!")
            return True
        except Exception as e:
            print(f"❌ Error inserting hadiths: {e}")
            db.session.rollback()
            return False

def verify_seeding():
    """Verify that hadiths were seeded correctly"""
    with app.app_context():
        print("\n🔍 Verifying seeded data...")
        
        total_count = Hadith.query.count()
        print(f"Total hadiths in database: {total_count}")
        
        if total_count == 0:
            print("❌ No hadiths found in database!")
            return False
        
        if total_count != 40:
            print(f"⚠️  Expected 40 hadiths, but found {total_count}")
        
        # Spot-check some hadiths
        print("\n📋 Spot-checking hadiths:")
        for hadith_num in [1, 20, 40]:
            hadith = Hadith.query.filter_by(hadith_number=hadith_num).first()
            if hadith:
                print(f"\n  Hadith #{hadith.hadith_number}:")
                print(f"    Narrator: {hadith.narrator}")
                print(f"    English: {hadith.english_text[:100]}...")
                if hadith.arabic_text and hadith.arabic_text != "Arabic text not available":
                    print(f"    Arabic: {hadith.arabic_text[:100]}...")
            else:
                print(f"  ❌ Hadith #{hadith_num} not found!")
        
        print("\n✅ Verification complete!")
        return True

def main():
    """Main function with CLI options"""
    if len(sys.argv) < 2:
        print("Hadith Data Seeding Script")
        print("=" * 50)
        print("\nUsage: python seed_db.py [command]")
        print("\nCommands:")
        print("  download    - Download hadith JSON from repository")
        print("  seed        - Download and seed database with all 40 hadiths")
        print("  verify      - Verify seeded data")
        print("  reset-seed  - Clear database and reseed")
        print("\nExamples:")
        print("  python seed_db.py seed")
        print("  python seed_db.py verify")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'download':
        hadith_data = download_hadith_json()
        if hadith_data:
            parsed = parse_hadith_data(hadith_data)
            print("\n📊 First 3 hadiths preview:")
            for h in parsed[:3]:
                print(f"\n  Hadith #{h['hadith_number']}:")
                print(f"    Narrator: {h['narrator']}")
                print(f"    English: {h['english_text'][:100]}...")
    
    elif command == 'seed':
        hadith_data = download_hadith_json()
        if hadith_data:
            parsed = parse_hadith_data(hadith_data)
            if seed_database(parsed):
                verify_seeding()
    
    elif command == 'verify':
        verify_seeding()
    
    elif command == 'reset-seed':
        with app.app_context():
            print("⚠️  This will delete all hadiths from the database!")
            confirm = input("Are you sure? Type 'yes' to confirm: ")
            if confirm.lower() == 'yes':
                Hadith.query.delete()
                db.session.commit()
                print("✅ All hadiths deleted.")
                
                hadith_data = download_hadith_json()
                if hadith_data:
                    parsed = parse_hadith_data(hadith_data)
                    if seed_database(parsed):
                        verify_seeding()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python seed_db.py' for usage information")

if __name__ == '__main__':
    main()
