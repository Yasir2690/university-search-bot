import pickle
import nltk
import random
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

class CollegeChatbot:
    def __init__(self):
        print("🤖 Loading chatbot model...")
        with open('intent_model.pkl', 'rb') as f:
            self.classifier = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open('intents_data.pkl', 'rb') as f:
            self.intents = pickle.load(f)
        with open('label_encoder.pkl', 'rb') as f:
            self.label_encoder = pickle.load(f)
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        print("✅ Chatbot ready!")
    
    def preprocess(self, text):
        words = nltk.word_tokenize(text.lower())
        words = [self.lemmatizer.lemmatize(w) for w in words 
                if w.isalpha() and w not in self.stop_words]
        return ' '.join(words)
    
    def get_response(self, user_input):
        # Preprocess input
        processed = self.preprocess(user_input)
        
        # Convert to vector and predict
        input_vector = self.vectorizer.transform([processed])
        pred_encoded = self.classifier.predict(input_vector)[0]
        predicted_tag = self.label_encoder.inverse_transform([pred_encoded])[0]
        
        # Get confidence
        probabilities = self.classifier.predict_proba(input_vector)[0]
        confidence = max(probabilities)
        
        # Fallback for low confidence
        if confidence < 0.35:
            return "🤖 I'm not sure about that. Could you please rephrase? Try asking about:\n   • Admissions\n   • Fees\n   • Courses\n   • Placements\n   • Scholarships\n   • Facilities"
        
        # Get random response for predicted intent
        for intent in self.intents['intents']:
            if intent['tag'] == predicted_tag:
                response = random.choice(intent['responses'])
                
                # Show confidence level
                if confidence > 0.75:
                    response = f"🎯 {response}"
                elif confidence > 0.55:
                    response = f"📚 {response}"
                else:
                    response = f"🤔 {response}"
                
                # Add helpful follow-ups
                if predicted_tag == "admission_requirements" and confidence > 0.6:
                    response += "\n💡 Tip: Application deadline is May 30th."
                elif predicted_tag == "fee_structure" and confidence > 0.6:
                    response += "\n💡 Tip: First installment due by July 15th."
                elif predicted_tag == "courses_offered" and confidence > 0.6:
                    response += "\n💡 Tip: Popular choice is B.Tech CSE with AI specialization."
                    
                return response
        
        return "🤖 Let me connect you to an academic advisor for detailed information."

def chat():
    bot = CollegeChatbot()
    print("\n" + "="*55)
    print("🎓 COLLEGE HELP DESK CHATBOT (IMPROVED)")
    print("="*55)
    print("💡 Type 'quit' to exit")
    print("💡 Ask me about: admissions, fees, courses, placements, scholarships")
    print("-"*55)
    
    conversation_history = []
    
    while True:
        user_input = input("\n👤 You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("🤖 Bot: Thank you for chatting! Have a great day! 🎓")
            break
        
        if not user_input:
            print("🤖 Bot: Please type something!")
            continue
        
        response = bot.get_response(user_input)
        print(response)
        
        # Store conversation
        conversation_history.append((user_input, response))
        if len(conversation_history) > 10:
            conversation_history.pop(0)

if __name__ == "__main__":
    chat()