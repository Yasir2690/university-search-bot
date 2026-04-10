import json
import re
import random
from datetime import datetime
import sqlite3
import os
import uuid
from collections import defaultdict
import time

class UltimateCollegeChatbot:
    def __init__(self):
        # Load intents
        with open('intents.json', 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        
        # User rate limiting
        self.user_requests = defaultdict(list)
        self.rate_limit = 10  # Max 10 requests per minute
        
        # Conversation history for summary
        self.conversation_history = []
        
        # Quick replies mapping
        self.quick_replies = {
            'admissions': ['Eligibility criteria', 'Application deadline', 'Required documents'],
            'fees': ['Fee structure', 'Scholarships', 'Payment options'],
            'courses': ['B.Tech courses', 'MBA program', 'BCA details'],
            'placements': ['Average package', 'Top recruiters', 'Placement process'],
            'hostel': ['Hostel fees', 'Hostel rules', 'Room types'],
            'sports': ['Sports facilities', 'Sports quota', 'Teams']
        }
        
        # Multi-language responses (basic)
        self.language = 'english'  # 'english' or 'hindi'
        self.language_responses = {
            'greeting': {
                'english': "Hello! How can I help you?",
                'hindi': "नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ?"
            },
            'goodbye': {
                'english': "Goodbye! Have a great day!",
                'hindi': "अलविदा! आपका दिन शुभ हो!"
            }
        }
        
        # Initialize database
        self.init_database()
        
        # Load user profile
        self.user_profile = {}
        self.load_user_profile()
        
        # Session tracking
        self.session_id = str(uuid.uuid4())[:8]
        self.start_time = datetime.now()
        
        # Keyword mapping
        self.keyword_map = {
            'greeting': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'goodbye': ['bye', 'goodbye', 'see you', 'thanks', 'thank you', 'exit', 'quit'],
            'admission_requirements': ['admission', 'apply', 'eligibility', 'requirements', 'criteria', 'percentage', 'marks'],
            'fee_structure': ['fee', 'fees', 'cost', 'price', 'tuition', 'payment'],
            'placement_record': ['placement', 'job', 'package', 'salary', 'recruiter', 'company'],
            'courses_offered': ['course', 'program', 'degree', 'btech', 'mba', 'bca', 'mca', 'bsc'],
            'scholarship': ['scholarship', 'financial aid', 'fee concession', 'merit', 'fund'],
            'campus_facilities': ['library', 'hostel', 'sports', 'canteen', 'lab', 'wifi', 'gym'],
            'exam_schedule': ['exam', 'test', 'mid term', 'final', 'semester', 'timetable'],
            'holidays': ['holiday', 'vacation', 'break', 'festival', 'diwali', 'holi'],
            'transport': ['bus', 'transport', 'commute', 'travel', 'metro'],
            'hostel': ['hostel', 'accommodation', 'room', 'mess', 'curfew'],
            'sports': ['sports', 'cricket', 'football', 'basketball', 'gym', 'tennis'],
            'faculty': ['faculty', 'teacher', 'professor', 'phd', 'instructor'],
            'alumni': ['alumni', 'graduate', 'passed out', 'old student'],
            'internship': ['internship', 'intern', 'stipend', 'training']
        }
    
    def init_database(self):
        """Initialize database"""
        self.conn = sqlite3.connect('chatbot_ultimate.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                intent TEXT,
                timestamp TEXT,
                response_time REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                rating INTEGER,
                comment TEXT,
                timestamp TEXT
            )
        ''')
        
        self.conn.commit()
    
    def load_user_profile(self):
        """Load user profile"""
        profile_file = 'user_profile_ultimate.json'
        if os.path.exists(profile_file):
            with open(profile_file, 'r') as f:
                self.user_profile = json.load(f)
        else:
            self.user_profile = {
                'name': None,
                'language': 'english',
                'total_queries': 0,
                'first_visit': str(datetime.now()),
                'last_visit': str(datetime.now()),
                'favorite_topics': []
            }
    
    def save_user_profile(self):
        """Save user profile"""
        with open('user_profile_ultimate.json', 'w') as f:
            json.dump(self.user_profile, f, indent=2)
    
    def check_rate_limit(self, user_id='default'):
        """Rate limiting to prevent spam"""
        now = time.time()
        # Clean old requests
        self.user_requests[user_id] = [t for t in self.user_requests[user_id] if now - t < 60]
        
        if len(self.user_requests[user_id]) >= self.rate_limit:
            return False
        self.user_requests[user_id].append(now)
        return True
    
    def show_typing_indicator(self):
        """Simulate typing indicator"""
        import sys
        print("🤖 Bot is typing", end="")
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="")
            sys.stdout.flush()
        print("\r", end="")
    
    def get_quick_replies(self, intent):
        """Get quick reply suggestions based on intent"""
        for category, replies in self.quick_replies.items():
            if category in intent or intent in category:
                return replies
        return ['More about admissions', 'Fee details', 'Course information']
    
    def match_intent(self, user_input):
        """Match intent using keywords"""
        user_lower = user_input.lower()
        scores = {}
        
        for intent, keywords in self.keyword_map.items():
            score = sum(2 if keyword in user_lower else 0 for keyword in keywords)
            scores[intent] = score
        
        max_score = max(scores.values())
        return max(scores, key=scores.get) if max_score > 0 else 'unknown'
    
    def change_language(self, user_input):
        """Change bot language"""
        if 'hindi' in user_input.lower() or 'हिंदी' in user_input:
            self.language = 'hindi'
            self.user_profile['language'] = 'hindi'
            self.save_user_profile()
            return "नमस्ते! अब मैं हिंदी में बात करूंगा।"
        elif 'english' in user_input.lower():
            self.language = 'english'
            self.user_profile['language'] = 'english'
            self.save_user_profile()
            return "Hello! I'll now speak in English."
        return None
    
    def export_chat_history(self):
        """Export conversation to file"""
        if not self.conversation_history:
            return "No conversation history to export."
        
        filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*50 + "\n")
            f.write("CHATBOT CONVERSATION EXPORT\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"User: {self.user_profile.get('name', 'Guest')}\n")
            f.write("="*50 + "\n\n")
            
            for i, (user_msg, bot_msg) in enumerate(self.conversation_history, 1):
                f.write(f"[{i}] User: {user_msg}\n")
                f.write(f"    Bot: {bot_msg}\n\n")
        
        return f"✅ Chat history exported to {filename}"
    
    def get_conversation_summary(self):
        """Generate summary of current conversation"""
        if not self.conversation_history:
            return "No conversation yet. Start asking questions!"
        
        # Count topics discussed
        topics = defaultdict(int)
        for user_msg, _ in self.conversation_history:
            intent = self.match_intent(user_msg)
            if intent != 'unknown':
                topics[intent] += 1
        
        if not topics:
            return "I couldn't identify specific topics in our conversation."
        
        summary = f"📊 **Conversation Summary**\n"
        summary += f"Total messages: {len(self.conversation_history)}\n"
        summary += f"Topics discussed:\n"
        
        for topic, count in sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]:
            summary += f"  • {topic.replace('_', ' ').title()}: {count} times\n"
        
        return summary
    
    def send_email_report(self, email_address):
        """Simulate sending email report"""
        # Note: For actual email, you'd need smtplib
        # This is a simulation
        if '@' in email_address and '.' in email_address:
            return f"📧 Report would be sent to {email_address} (Email feature ready for production)"
        return "Please provide a valid email address like: email name@example.com"
    
    def get_response(self, user_input):
        """Main response generator with all features"""
        
        # Check rate limit
        if not self.check_rate_limit():
            return "⏰ Too many messages! Please wait a moment before sending more."
        
        # Show typing effect
        self.show_typing_indicator()
        
        # Language change command
        if 'speak hindi' in user_input.lower() or 'hindi mein' in user_input.lower():
            return self.change_language(user_input)
        
        # Export command
        if 'export chat' in user_input.lower() or 'save chat' in user_input.lower():
            return self.export_chat_history()
        
        # Summary command
        if 'summary' in user_input.lower() or 'summarize' in user_input.lower():
            return self.get_conversation_summary()
        
        # Email command
        if 'email' in user_input.lower() and 'report' in user_input.lower():
            import re
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', user_input)
            if email_match:
                return self.send_email_report(email_match.group())
            return "Please provide your email address: email yourname@example.com"
        
        # Name change
        if 'my name is' in user_input.lower() or 'change name' in user_input.lower():
            import re
            name_match = re.search(r'(?:my name is|change name to|call me)\s+(\w+)', user_input.lower())
            if name_match:
                new_name = name_match.group(1).capitalize()
                self.user_profile['name'] = new_name
                self.save_user_profile()
                return f"✅ Nice to meet you, {new_name}! I'll remember your name."
        
        # Normal intent matching
        intent = self.match_intent(user_input)
        
        # Update profile
        self.user_profile['total_queries'] += 1
        self.user_profile['last_visit'] = str(datetime.now())
        if intent != 'unknown':
            if intent not in self.user_profile['favorite_topics']:
                self.user_profile['favorite_topics'].append(intent)
                self.user_profile['favorite_topics'] = self.user_profile['favorite_topics'][-5:]
        self.save_user_profile()
        
        # Get response from intents
        for intent_data in self.intents['intents']:
            if intent_data['tag'] == intent:
                response = random.choice(intent_data['responses'])
                
                # Add personalization
                if self.user_profile.get('name') and intent == 'greeting':
                    response = f"{response} Great to see you again, {self.user_profile['name']}!"
                
                # Add quick replies
                quick_reply_list = self.get_quick_replies(intent)
                quick_reply_text = "\n\n💡 **Quick replies:**\n" + " | ".join(quick_reply_list[:3])
                response += quick_reply_text
                
                # Store in history
                self.conversation_history.append((user_input, response))
                if len(self.conversation_history) > 50:
                    self.conversation_history.pop(0)
                
                # Save to database
                self.save_to_db(user_input, response, intent)
                
                return response
        
        # Unknown intent response with suggestions
        fallback = "🤔 I'm not sure about that. Here's what I can help with:\n\n"
        fallback += "• **Admissions** - eligibility, process, requirements\n"
        fallback += "• **Fees** - fee structure, scholarships\n"
        fallback += "• **Courses** - B.Tech, MBA, BCA, etc.\n"
        fallback += "• **Placements** - packages, recruiters\n"
        fallback += "• **Hostel & Sports** - facilities, rules\n\n"
        fallback += "💡 Try: 'change my name to Dhruv' or 'speak hindi'\n"
        fallback += "💡 Type 'summary' to see conversation summary\n"
        fallback += "💡 Type 'export chat' to save conversation"
        
        self.conversation_history.append((user_input, fallback))
        self.save_to_db(user_input, fallback, 'unknown')
        return fallback
    
    def save_to_db(self, user_msg, bot_resp, intent):
        """Save to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (session_id, user_message, bot_response, intent, timestamp, response_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.session_id, user_msg, bot_resp, intent, datetime.now().isoformat(), 0))
        self.conn.commit()
    
    def get_stats(self):
        """Get detailed statistics"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT intent, COUNT(*) FROM conversations WHERE intent != "unknown" GROUP BY intent ORDER BY COUNT(*) DESC LIMIT 5')
        top = cursor.fetchall()
        
        stats = f"""
╔{'='*50}╗
║                    STATISTICS DASHBOARD                    ║
╠{'='*50}╣
║ Session ID: {self.session_id}
║ Started at: {self.start_time.strftime('%H:%M:%S')}
║ Total queries: {total}
║ User name: {self.user_profile.get('name', 'Not set')}
║ Language: {self.language.upper()}
║ Total visits: {self.user_profile.get('total_queries', 0)}
╠{'='*50}╣
║ TOP 5 TOPICS:
"""
        for i, (intent, count) in enumerate(top, 1):
            stats += f"║ {i}. {intent.replace('_', ' ').title():<30} {count} times\n"
        
        stats += f"╚{'='*50}╝"
        return stats
    
    def chat(self):
        """Main chat loop"""
        print("\n" + "╔" + "="*58 + "╗")
        print("║" + " "*15 + "🤖 ULTIMATE COLLEGE CHATBOT" + " "*16 + "║")
        print("║" + " "*15 + "With 10+ Advanced Features" + " "*14 + "║")
        print("╚" + "="*58 + "╝")
        
        print("\n✨ **NEW FEATURES:**")
        print("  • 🌐 Multi-language (say 'speak hindi')")
        print("  • 💾 Export chat (say 'export chat')")
        print("  • 📊 Conversation summary (say 'summary')")
        print("  • 📧 Email reports (say 'email report to name@example.com')")
        print("  • 🔘 Quick reply suggestions")
        print("  • ⌨️ Typing indicator")
        print("  • ⏱️ Rate limiting")
        print("  • 👤 Name personalization")
        
        print("\n" + "-"*58)
        
        if not self.user_profile.get('name'):
            print("\n💡 Tip: Say 'my name is Dhruv' to personalize!")
        
        print("💡 Tip: Say 'stats' to see analytics")
        print("💡 Type 'quit' to exit")
        print("-"*58)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n🤖 Thank you for chatting! Have a great day! 🌟")
                if len(self.conversation_history) > 3:
                    print("\n💡 Tip: Say 'export chat' next time to save our conversation!")
                break
            
            if user_input.lower() == 'stats':
                print(self.get_stats())
                continue
            
            if not user_input:
                continue
            
            response = self.get_response(user_input)
            print(response)

if __name__ == "__main__":
    bot = UltimateCollegeChatbot()
    bot.chat()