"""
Debug script to inspect the actual JSON structure from the hadith source.
This helps us understand the exact field names and structure.
"""

import requests
import json

HADITH_JSON_URL = "https://uthumany.github.io/nawawi-40-hadiths/api/hadiths.json"

print("📥 Downloading hadith data...")
response = requests.get(HADITH_JSON_URL, timeout=10)
response.raise_for_status()

data = response.json()

print("\n🔍 JSON Structure Analysis:")
print("=" * 60)

# Show the overall structure
print(f"\nTop-level type: {type(data)}")

if isinstance(data, dict):
    print(f"Top-level keys: {list(data.keys())}")
    # Check if there's a hadiths array
    if 'hadiths' in data:
        print(f"Number of hadiths: {len(data['hadiths'])}")
        print("\nFirst hadith structure:")
        print(json.dumps(data['hadiths'][0], indent=2, ensure_ascii=False)[:500])
    else:
        # Show first entry of top-level dict
        first_key = list(data.keys())[0]
        print(f"\nFirst entry (key: {first_key}):")
        print(json.dumps(data[first_key], indent=2, ensure_ascii=False)[:500])

elif isinstance(data, list):
    print(f"Number of hadiths: {len(data)}")
    print("\nFirst hadith structure:")
    print(json.dumps(data[0], indent=2, ensure_ascii=False)[:500])

print("\n" + "=" * 60)
print("✅ Analysis complete. Use this to update seed_db.py field names.")
