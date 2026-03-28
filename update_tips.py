import json
import os
import random
from datetime import datetime
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_health_tips():
    seed = random.randint(1, 99999)
    prompt = (
        f"Generate 5 unique medical public health tips for the Libyan community. Seed: {seed}. "
        "Focus on: hygiene, water safety, and disease prevention. "
        "Return ONLY a JSON array with keys: 'title', 'content', 'type', 'source'."
    )
    try:
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    new_tips = generate_health_tips()
    if not new_tips: return
    file_path = 'athardata.json'
    timestamp = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    for tip in new_tips:
        tip['date'] = timestamp
        tip['id'] = f"tip-{random.randint(10000, 99999)}"
    archive = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                archive = json.load(f)
        except:
            archive = []
    full_data = new_tips + archive
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    print("✅ Done!")

if __name__ == "__main__":
    main()
