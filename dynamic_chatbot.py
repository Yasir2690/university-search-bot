import json
import re
import random
from datetime import datetime
import sqlite3
import os
import uuid

class DynamicCollegeChatbot:
    def __init__(self):
        # Load intents
        with open('intents.json', 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        
        # Enhanced keyword mapping
        self.keyword_map = {
            'greeting': ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'namaste', 'howdy', 'sup'],
            'goodbye': ['bye', 'goodbye', 'see you', 'thanks', 'thank you', 'exit', 'quit', 'cya', 'take care'],
            'admission_requirements': ['admission', 'apply', 'eligibility', 'qualification', 'entrance', 'join', 'get in', 'requirements', 'criteria', 'percentage', 'marks', '12th', '10+2', 'cutoff'],
            'fee_structure': ['fee', 'fees', 'cost', 'price', 'tuition', 'payment', 'semester fee', 'annual fee', 'expenses', 'afford', 'money', 'rupees'],
            'placement_record': ['placement', 'job', 'package', 'salary', 'recruiter', 'company', 'campus', 'employer', 'career', 'lpa', 'ctc', 'hiring', 'recruitment'],
            'courses_offered': ['course', 'program', 'degree', 'btech', 'mtech', 'mba', 'bca', 'mca', 'bsc', 'phd', 'branch', 'specialization', 'computer science', 'mechanical', 'civil', 'electrical', 'couses', 'coarse'],
            'scholarship': ['scholarship', 'financial aid', 'fee concession', 'merit', 'fund', 'support', 'loan', 'assistance', 'waiver'],
            'campus_facilities': ['library', 'timing', 'hours', 'hostel', 'sports', 'canteen', 'lab', 'wifi', 'infrastructure', 'gym', 'medical', 'facility', 'book', 'reading', 'study', 'classroom'],
            'exam_schedule': ['exam', 'test', 'mid term', 'final', 'semester', 'timetable', 'schedule', 'dates', 'practical', 'theory', 'assessment'],
            'holidays': ['holiday', 'vacation', 'break', 'closed', 'festival', 'diwali', 'holi', 'summer', 'winter', 'leave', 'off day'],
            'transport': ['bus', 'transport', 'commute', 'travel', 'reach college', 'bus stop', 'metro', 'vehicle', 'conveyance', 'pickup'],
            'hostel': ['hostel', 'accommodation', 'room', 'mess', 'curfew', 'visitor', 'security deposit', 'rent', 'pg', 'hostel fee', 'hostel rule', 'dorm'],
            'sports': ['sports', 'cricket', 'football', 'basketball', 'volleyball', 'tennis', 'swimming', 'gym', 'badminton', 'table tennis', 'sports quota', 'ground', 'court', 'pool', 'athletics'],
            'faculty': ['faculty', 'teacher', 'professor', 'phd', 'instructor', 'lecturer', 'teaching staff', 'student teacher ratio', 'guest lecture', 'staff'],
            'alumni': ['alumni', 'graduate', 'passed out', 'old student', 'alumni network', 'alumni association', 'alumni meet', 'famous alumni', 'success story', 'ex-student'],
            'internship': ['internship', 'intern', 'stipend', 'industry training', 'summer training', 'winter training', 'internship opportunity', 'paid intern', 'company training', 'apprenticeship'],
            'change_name': ['change my name', 'my name is', 'call me', 'rename', 'set name', 'i am', 'change name to']
        }
        
        # Response variations
        self.response_variations = {
            'greeting': [
                "Hello! How can I help you with college info?",
                "Hi there! Ask me about admissions, fees, placements, or courses.",
                "Hey! Welcome to the college help desk! What brings you today?",
                "Greetings! I'm here to answer all your college questions!",
                "Namaste! How can I assist you with your college journey?"
            ]
        }
        
        # Fix: Suppress SQLite datetime warning
        self.init_database()
        
        # User profile
        self.user_profile = {}
        self.load_user_profile()
        
        # Conversation context
        self.context = []
        self.faq_counter = {}
    
    def init_database(self):
        """Initialize SQLite database without datetime warning"""
        self.conn = sqlite3.connect('chatbot_dynamic.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Use TEXT instead of DATETIME to avoid warning
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                intent TEXT,
                timestamp TEXT,
                session_id TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faq_stats (
                intent TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0,
                last_asked TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                rating INTEGER,
                feedback_text TEXT,
                timestamp TEXT
            )
        ''')
        
        self.conn.commit()
    
    def load_user_profile(self):
        """Load or create user profile"""
        profile_file = 'user_profile.json'
        if os.path.exists(profile_file):
            try:
                with open(profile_file, 'r') as f:
                    self.user_profile = json.load(f)
            except:
                self.user_profile = {}
        
        # Initialize default profile if needed
        if not self.user_profile:
            self.user_profile = {
                'name': None,
                'course_interest': None,
                'visit_count': 0,
                'last_visit': None,
                'favorite_topics': []
            }
    
    def save_user_profile(self):
        """Save user profile"""
        with open('user_profile.json', 'w') as f:
            json.dump(self.user_profile, f, indent=2)
    
    def change_user_name(self, user_input):
        """Extract and change user name from input"""
        import re
        
        # Patterns to extract name
        patterns = [
            r'change my name to (\w+)',
            r'my name is (\w+)',
            r'call me (\w+)',
            r'rename me to (\w+)',
            r'set name to (\w+)',
            r'i am (\w+)',
            r'change name to (\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                new_name = match.group(1).capitalize()
                old_name = self.user_profile.get('name', 'Unknown')
                self.user_profile['name'] = new_name
                self.save_user_profile()
                return f"✅ Done! I'll call you **{new_name}** from now on! Nice to meet you, {new_name}! 😊"
        
        return None
    
    def get_time_based_greeting(self):
        """Return greeting based on time of day"""
        hour = datetime.now().hour
        if hour < 12:
            return "🌅 Good morning! "
        elif hour < 17:
            return "☀️ Good afternoon! "
        else:
            return "🌙 Good evening! "
    
    def get_random_response(self, intent):
        """Get random response variation"""
        if intent in self.response_variations:
            return random.choice(self.response_variations[intent])
        return None
    
    def update_faq_stats(self, intent):
        """Track frequently asked questions"""
        cursor = self.conn.cursor()
        now_str = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO faq_stats (intent, count, last_asked)
            VALUES (?, 1, ?)
            ON CONFLICT(intent) DO UPDATE SET
                count = count + 1,
                last_asked = excluded.last_asked
        ''', (intent, now_str))
        self.conn.commit()
    
    def get_trending_topics(self):
        """Get most asked topics (excluding unknown)"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT intent, count FROM faq_stats 
            WHERE intent != 'unknown'
            ORDER BY count DESC LIMIT 3
        ''')
        return cursor.fetchall()
    
    def get_smart_suggestions(self, current_intent):
        """Provide intelligent question suggestions"""
        suggestions_map = {
            'admission_requirements': [
                "What is the last date to apply?",
                "How much are the fees?",
                "What scholarships are available?"
            ],
            'fee_structure': [
                "Is there hostel fees included?",
                "Can I get education loan?",
                "What is the refund policy?"
            ],
            'placement_record': [
                "Which companies visit for placements?",
                "What is the average package for CSE?",
                "Are internships mandatory?"
            ],
            'courses_offered': [
                "Which course has best placement?",
                "What is the duration of B.Tech?",
                "Can I do specialization in AI?"
            ],
            'hostel': [
                "Is there vegetarian mess?",
                "What are hostel timings?",
                "How to apply for hostel?"
            ],
            'sports': [
                "Is there sports quota?",
                "What sports facilities available?",
                "Are there sports scholarships?"
            ],
            'internship': [
                "When does internship start?",
                "Is internship paid?",
                "Which companies offer internships?"
            ],
            'scholarship': [
                "How to apply for scholarship?",
                "What is the scholarship amount?",
                "Who is eligible for scholarship?"
            ]
        }
        
        suggestions = suggestions_map.get(current_intent, [])
        if suggestions:
            random.shuffle(suggestions)
            return suggestions[:2]
        return []
    
    def get_live_fun_fact(self):
        """Return random fun facts"""
        fun_facts = [
            "📚 Our library has over 50,000 books and 10,000 e-journals!",
            "🏆 95% of our graduates get jobs within 6 months!",
            "🌍 We have students from 25 different countries!",
            "🎓 Our alumni network spans 30+ countries worldwide!",
            "💻 The campus has 24/7 high-speed WiFi everywhere!",
            "🏅 Our sports teams have won 50+ university championships!",
            "📊 Student-faculty ratio is an impressive 15:1!",
            "🔬 We have 25 research labs with latest equipment!"
        ]
        return random.choice(fun_facts)
    
    def get_important_dates(self):
        """Get current/upcoming important dates"""
        current_month = datetime.now().month
        if current_month in [1, 2, 3]:
            return "📅 Upcoming: Even semester exams in April-May"
        elif current_month in [4, 5, 6]:
            return "📅 Summer break starts May 15th! ☀️"
        elif current_month in [7, 8, 9]:
            return "📅 Admissions open! Apply before July 30th"
        elif current_month in [10, 11, 12]:
            return "📅 Placement season starts! Prepare your resume"
        return "📅 Check website for academic calendar"
    
    def match_intent(self, user_input):
        """Enhanced intent matching"""
        user_lower = user_input.lower()
        scores = {}
        
        for intent, keywords in self.keyword_map.items():
            score = 0
            for keyword in keywords:
                if keyword in user_lower:
                    if re.search(r'\b' + re.escape(keyword) + r'\b', user_lower):
                        score += 3
                    else:
                        score += 1
            scores[intent] = score
        
        max_score = max(scores.values())
        if max_score > 0:
            return max(scores, key=scores.get)
        return 'unknown'
    
    def get_response(self, user_input, session_id):
        """Generate dynamic response"""
        
        # Check for name change command FIRST
        if 'change my name' in user_input.lower() or 'my name is' in user_input.lower() or 'change name to' in user_input.lower() or 'call me' in user_input.lower():
            name_response = self.change_user_name(user_input)
            if name_response:
                return name_response
        
        intent = self.match_intent(user_input)
        
        # Update FAQ statistics
        self.update_faq_stats(intent)
        self.faq_counter[intent] = self.faq_counter.get(intent, 0) + 1
        
        # Find base response
        for intent_data in self.intents['intents']:
            if intent_data['tag'] == intent:
                base_response = random.choice(intent_data['responses'])
                
                # Add time-based context for greeting
                if intent == 'greeting':
                    base_response = self.get_time_based_greeting() + base_response
                    if self.user_profile.get('name'):
                        base_response = f"Welcome back, {self.user_profile['name']}! " + base_response
                    if random.random() < 0.2:
                        base_response += f"\n\n✨ Fun fact: {self.get_live_fun_fact()}"
                
                # Add deadline tips
                if intent == 'admission_requirements':
                    base_response += "\n\n⏰ Application deadline: May 30th, 2026"
                elif intent == 'fee_structure':
                    base_response += "\n\n💰 Early bird discount: 10% off if paid before June 15th"
                elif intent == 'placement_record':
                    base_response += "\n\n🏢 Next placement drive: August 2026"
                elif intent == 'hostel':
                    base_response += "\n\n🏠 Limited seats! Apply before July 15th"
                elif intent == 'internship':
                    base_response += "\n\n🎯 Internship fair on March 20th, 2026!"
                
                # Add smart suggestions
                suggestions = self.get_smart_suggestions(intent)
                if suggestions:
                    base_response += f"\n\n💡 You might also want to ask:\n• " + "\n• ".join(suggestions)
                
                self.save_conversation(session_id, user_input, base_response, intent)
                return f"🤖 {base_response}"
        
        # Handle unknown
        trending = self.get_trending_topics()
        fallback = f"🤖 I'm not sure about that. Here's what I can help with:\n\n"
        fallback += "• Admissions • Fees • Placements • Courses\n"
        fallback += "• Scholarships • Hostel • Sports • Faculty\n"
        fallback += "• Alumni • Internships • Exams • Transport\n\n"
        
        if trending:
            fallback += f"📈 Most asked: {', '.join([t[0].replace('_', ' ').title() for t in trending[:2]])}\n\n"
        
        fallback += f"💡 Try asking: 'What courses are offered?' or 'How much are fees?'\n\n"
        fallback += f"💡 Want to change your name? Say 'change my name to Dhruv'"
        
        self.save_conversation(session_id, user_input, fallback, 'unknown')
        return fallback
    
    def save_conversation(self, session_id, user_msg, bot_resp, intent):
        """Save conversation to database"""
        cursor = self.conn.cursor()
        now_str = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO conversations (user_id, user_message, bot_response, intent, timestamp, session_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('default', user_msg, bot_resp, intent, now_str, session_id))
        self.conn.commit()
    
    def get_detailed_stats(self):
        """Get comprehensive statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM conversations 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        today = cursor.fetchone()[0] if total > 0 else 0
        
        cursor.execute('''
            SELECT intent, COUNT(*) as count 
            FROM conversations 
            WHERE intent != 'unknown'
            GROUP BY intent 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        top_intents = cursor.fetchall()
        
        stats = f"""
📊 CHATBOT STATISTICS
{'='*40}
Total conversations: {total}
Today's chats: {today}

🔥 TOP ASKED TOPICS:
"""
        if top_intents:
            for i, (intent, count) in enumerate(top_intents, 1):
                stats += f"{i}. {intent.replace('_', ' ').title()}: {count} times\n"
        else:
            stats += "No data yet. Ask me some questions!\n"
        
        if self.user_profile.get('name'):
            stats += f"\n👤 Logged in as: {self.user_profile['name']}"
        
        return stats
    
    def chat(self):
        """Main chat loop"""
        session_id = str(uuid.uuid4())[:8]
        
        print("\n" + "="*60)
        print("🌟 DYNAMIC COLLEGE CHATBOT - ENHANCED EDITION")
        print("="*60)
        print("I can help you with 15+ college topics!")
        print("-"*60)
        print("💡 SPECIAL COMMANDS:")
        print("  • 'stats' - View chatbot statistics")
        print("  • 'trending' - See most asked topics")
        print("  • 'fact' - Get a fun college fact")
        print("  • 'date' - Check important dates")
        print("  • 'change my name to NAME' - Set your name")
        print("  • 'help' - Show this menu")
        print("  • 'quit' - Exit")
        print("-"*60)
        
        # Personalized greeting
        if not self.user_profile.get('name'):
            print("\n🤖 Hi! I'm your college assistant. What's your name?")
            print("   (You can also say 'change my name to Dhruv' anytime)")
        else:
            print(f"\n🤖 {self.get_time_based_greeting()}Welcome back, {self.user_profile['name']}! 👋")
            if random.random() < 0.3:
                print(f"🤖 ✨ Did you know? {self.get_live_fun_fact()}")
        
        while True:
            user_input = input("\n👤 You: ").strip().lower()
            
            # Handle special commands
            if user_input in ['quit', 'exit', 'bye', 'goodbye']:
                name = self.user_profile.get('name', 'friend')
                print(f"\n🤖 Thank you for chatting, {name}! Have a great day! 🌟")
                break
            
            if user_input == 'stats':
                print(f"\n🤖 {self.get_detailed_stats()}")
                continue
            
            if user_input == 'trending':
                trending = self.get_trending_topics()
                if trending:
                    print("\n🤖 🔥 Most asked topics:")
                    for intent, count in trending:
                        display_name = intent.replace('_', ' ').title()
                        print(f"  • {display_name}: {count} times")
                else:
                    print("\n🤖 No trending topics yet. Ask me some questions!")
                continue
            
            if user_input == 'fact':
                print(f"\n🤖 ✨ {self.get_live_fun_fact()}")
                continue
            
            if user_input == 'date':
                print(f"\n🤖 {self.get_important_dates()}")
                continue
            
            if user_input == 'help':
                print("\n🤖 💡 COMMANDS MENU:")
                print("  • 'stats' - View chatbot statistics")
                print("  • 'trending' - See most asked topics")
                print("  • 'fact' - Get a fun college fact")
                print("  • 'date' - Check important dates")
                print("  • 'change my name to Dhruv' - Change your name")
                print("  • 'quit' - Exit")
                print("\n📚 Ask about: admissions, fees, placements, courses, scholarships")
                print("  hostel, sports, faculty, alumni, internships, exams")
                continue
            
            if not user_input:
                print("🤖 Please type your question or type 'help' for options.")
                continue
            
            # Get dynamic response
            response = self.get_response(user_input, session_id)
            print(response)

# Run the chatbot
if __name__ == "__main__":
    bot = DynamicCollegeChatbot()
    bot.chat()