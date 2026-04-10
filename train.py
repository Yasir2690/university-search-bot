import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
print("📥 Downloading NLTK data...")
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

class IntentTrainer:
    def __init__(self, intents_file='intents.json'):
        print(f"📂 Loading {intents_file}...")
        with open(intents_file, 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
        self.classifier = LogisticRegression(C=1.5, max_iter=1000)
        self.label_encoder = LabelEncoder()
        
    def preprocess(self, text):
        """Advanced text preprocessing"""
        # Convert to lowercase and tokenize
        words = nltk.word_tokenize(text.lower())
        
        # Remove stopwords and non-alphabetic, then lemmatize
        words = [self.lemmatizer.lemmatize(w) for w in words 
                if w.isalpha() and w not in self.stop_words]
        
        return ' '.join(words)
    
    def prepare_data(self):
        """Prepare patterns and tags for training"""
        patterns = []
        tags = []
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                processed = self.preprocess(pattern)
                patterns.append(processed)
                tags.append(intent['tag'])
        
        # Convert tags to numbers
        self.tags_encoded = self.label_encoder.fit_transform(tags)
        
        # Create TF-IDF features
        self.X = self.vectorizer.fit_transform(patterns)
        self.y = self.tags_encoded
        
        print(f"📊 Prepared {len(patterns)} training examples")
        print(f"🏷️  Found {len(self.label_encoder.classes_)} unique intents: {list(self.label_encoder.classes_)}")
        
    def train(self):
        """Train the classifier"""
        print("🔄 Preparing data...")
        self.prepare_data()
        
        print("🔄 Training model...")
        self.classifier.fit(self.X, self.y)
        
        # Calculate accuracy
        accuracy = self.classifier.score(self.X, self.y)
        
        # Save models
        print("💾 Saving models...")
        with open('intent_model.pkl', 'wb') as f:
            pickle.dump(self.classifier, f)
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        with open('intents_data.pkl', 'wb') as f:
            pickle.dump(self.intents, f)
        with open('label_encoder.pkl', 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        print("\n" + "="*50)
        print("✅ TRAINING COMPLETE!")
        print(f"📈 Model Accuracy: {accuracy:.2%}")
        print(f"💾 Files saved:")
        print("   - intent_model.pkl")
        print("   - vectorizer.pkl")
        print("   - intents_data.pkl")
        print("   - label_encoder.pkl")
        print("="*50)
        
        # Test the model
        self.test_model()
    
    def test_model(self):
        """Test the trained model with sample inputs"""
        print("\n🧪 Testing model with sample inputs:")
        test_inputs = [
            "hello",
            "hi there",
            "how much are fees?",
            "what is the fee structure",
            "what courses do you offer?",
            "which programs are available",
            "placement records",
            "average package",
            "bye",
            "goodbye"
        ]
        
        print("\n" + "-"*50)
        for test in test_inputs:
            processed = self.preprocess(test)
            vec = self.vectorizer.transform([processed])
            pred_encoded = self.classifier.predict(vec)[0]
            pred_tag = self.label_encoder.inverse_transform([pred_encoded])[0]
            
            # Get confidence scores for all classes
            probas = self.classifier.predict_proba(vec)[0]
            confidence = max(probas)
            
            # Get top 3 predictions
            top_3_idx = np.argsort(probas)[-3:][::-1]
            top_3 = [(self.label_encoder.inverse_transform([idx])[0], probas[idx]) for idx in top_3_idx]
            
            status = "✅" if confidence > 0.6 else "⚠️"
            print(f"{status} '{test}'")
            print(f"   → Predicted: {pred_tag} (confidence: {confidence:.2%})")
            print(f"   → Top alternatives: {', '.join([f'{t[0]}({t[1]:.1%})' for t in top_3[1:]])}")
            print()

if __name__ == "__main__":
    print("="*50)
    print("🤖 CHATBOT INTENT TRAINER (IMPROVED)")
    print("="*50)
    
    trainer = IntentTrainer()
    trainer.train()
    
    print("\n🎉 Training complete! Run 'python chatbot.py' to test your chatbot")