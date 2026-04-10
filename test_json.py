import json

try:
    with open('intents.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    print("✅ JSON file is VALID!")
    print(f"📊 Number of intents: {len(data['intents'])}")
    print("\n📋 Your intents are:")
    for intent in data['intents']:
        print(f"  - {intent['tag']}: {len(intent['patterns'])} patterns, {len(intent['responses'])} responses")
        
except FileNotFoundError:
    print("❌ intents.json not found in current directory!")
except json.JSONDecodeError as e:
    print(f"❌ JSON has ERROR: {e}")
    print("Please check your JSON syntax (commas, brackets, quotes)")