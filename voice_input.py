import speech_recognition as sr
import pyttsx3
import json
import random

class VoiceChatbot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        
        # Load intents
        with open('intents.json', 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        
        # Set voice properties
        self.tts_engine.setProperty('rate', 150)  # Speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume
    
    def listen(self):
        """Listen for voice input"""
        with sr.Microphone() as source:
            print("\n🎤 Listening... (Speak now)")
            self.tts_engine.say("I'm listening")
            self.tts_engine.runAndWait()
            
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("👂 Recording...")
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("🔄 Processing...")
                text = self.recognizer.recognize_google(audio)
                print(f"👤 You said: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                print("⏰ No speech detected")
                return ""
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                return ""
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖 Bot: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def get_response(self, user_input):
        """Get response based on input"""
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                if pattern.lower() in user_input:
                    return random.choice(intent['responses'])
        return "I can help with admissions, fees, courses, placements, hostel, and sports. Please ask something specific!"
    
    def run(self):
        """Run voice chatbot"""
        print("\n" + "="*50)
        print("🎙️ VOICE CHATBOT")
        print("="*50)
        print("Commands:")
        print("  • Say 'quit' or 'exit' to stop")
        print("  • Say 'help' for assistance")
        print("-"*50)
        
        self.speak("Hello! I'm your college voice assistant. How can I help you?")
        
        while True:
            user_input = self.listen()
            
            if not user_input:
                continue
            
            if user_input in ['quit', 'exit', 'goodbye', 'bye']:
                self.speak("Thank you for chatting! Have a great day!")
                break
            
            if user_input == 'help':
                self.speak("I can answer questions about admissions, fees, courses, placements, hostel, sports, exams, and scholarships. What would you like to know?")
                continue
            
            response = self.get_response(user_input)
            self.speak(response)

if __name__ == "__main__":
    bot = VoiceChatbot()
    bot.run()