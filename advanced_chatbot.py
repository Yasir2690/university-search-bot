import json
import re
import random

class AdvancedCollegeChatbot:
    def __init__(self):
        # Load intents with proper encoding
        with open('intents.json', 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        
        # Define keyword mappings for each intent
        self.keyword_map = {
            'greeting': ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'namaste'],
            'goodbye': ['bye', 'goodbye', 'see you', 'thanks', 'thank you', 'exit', 'quit'],
            'admission_requirements': ['admission', 'apply', 'eligibility', 'qualification', 'entrance', 'join', 'get in', 'requirements', 'criteria', 'percentage', 'marks', '12th', '10+2'],
            'fee_structure': ['fee', 'fees', 'cost', 'price', 'tuition', 'payment', 'semester fee', 'annual fee', 'expenses', 'afford'],
            'placement_record': ['placement', 'job', 'package', 'salary', 'recruiter', 'company', 'campus', 'employer', 'career', 'lpa', 'ctc'],
            'courses_offered': ['course', 'program', 'degree', 'btech', 'mtech', 'mba', 'bca', 'mca', 'bsc', 'phd', 'branch', 'specialization', 'computer science', 'mechanical', 'civil', 'electrical', 'couses', 'coarse'],
            'scholarship': ['scholarship', 'financial aid', 'fee concession', 'merit', 'fund', 'support', 'loan', 'assistance'],
            'campus_facilities': ['library', 'timing', 'hours', 'hostel', 'sports', 'canteen', 'lab', 'wifi', 'infrastructure', 'gym', 'medical', 'facility', 'book', 'reading', 'study'],
            'exam_schedule': ['exam', 'test', 'mid term', 'final', 'semester', 'timetable', 'schedule', 'dates', 'practical'],
            'holidays': ['holiday', 'vacation', 'break', 'closed', 'festival', 'diwali', 'holi', 'summer', 'winter'],
            'transport': ['bus', 'transport', 'commute', 'travel', 'reach college', 'bus stop', 'metro', 'vehicle'],
            'hostel': ['hostel', 'accommodation', 'room', 'mess', 'curfew', 'visitor', 'security deposit', 'rent', 'pg', 'hostel fee', 'hostel rule'],
            'sports': ['sports', 'cricket', 'football', 'basketball', 'volleyball', 'tennis', 'swimming', 'gym', 'badminton', 'table tennis', 'sports quota', 'ground', 'court', 'pool'],
            'faculty': ['faculty', 'teacher', 'professor', 'phd', 'instructor', 'lecturer', 'teaching staff', 'student teacher ratio', 'guest lecture'],
            'alumni': ['alumni', 'graduate', 'passed out', 'old student', 'alumni network', 'alumni association', 'alumni meet', 'famous alumni', 'success story'],
            'internship': ['internship', 'intern', 'stipend', 'industry training', 'summer training', 'winter training', 'internship opportunity', 'paid intern', 'company training']
        }
        
        # Store conversation context
        self.context = []
        
    def match_intent(self, user_input):
        """Match user input to intent using keywords"""
        user_input_lower = user_input.lower()
        
        # Score each intent based on keyword matches
        scores = {}
        for intent, keywords in self.keyword_map.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of each keyword
                occurrences = len(re.findall(r'\b' + re.escape(keyword) + r'\b', user_input_lower))
                score += occurrences
                
                # Also check for partial matches (e.g., "fees" matches "fee")
                if keyword in user_input_lower:
                    score += 0.5
            scores[intent] = score
        
        # Find intent with highest score
        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        
        # If score is 0, try to detect common questions
        if max_score == 0:
            if '?' in user_input:
                return 'general_query'
            return 'unknown'
        
        # Return best intent if score is high enough
        if max_score >= 1:
            return best_intent
        else:
            return 'unknown'
    
    def get_response(self, user_input):
        """Generate response based on matched intent"""
        intent = self.match_intent(user_input)
        
        # Find responses for the intent
        for intent_data in self.intents['intents']:
            if intent_data['tag'] == intent:
                response = random.choice(intent_data['responses'])
                
                # Add contextual responses
                if intent == 'admission_requirements':
                    response += "\n\nApplication deadline: May 30th, 2026"
                elif intent == 'fee_structure':
                    response += "\n\nScholarship applications open until June 15th"
                elif intent == 'placement_record':
                    response += "\n\nNext placement drive: August 2026"
                elif intent == 'courses_offered':
                    response += "\n\nPopular choice: B.Tech in AI & Data Science"
                elif intent == 'hostel':
                    response += "\n\nLimited seats! Apply before July 15th"
                elif intent == 'internship':
                    response += "\n\nInternship fair on March 20th, 2026"
                
                return f"Bot: {response}"
        
        # Handle unknown queries
        if intent == 'unknown':
            return """Bot: I'm not sure about that. Here's what I can help with:

- Admissions (eligibility, process, requirements)
- Fees (tuition, payment options, scholarships)
- Courses (B.Tech, MBA, BCA, MCA, BSc)
- Placements (packages, recruiters, records)
- Facilities (library, hostel, labs, sports)
- Exam schedules
- Holidays
- Transport
- Hostel (fees, rules, facilities)
- Sports (grounds, courts, quota)
- Faculty (qualifications, departments)
- Alumni (network, benefits, notable alumni)
- Internship (opportunities, stipend, recruiters)

Please rephrase your question."""
        
        elif intent == 'general_query':
            return "Bot: Good question! Is there something specific about admissions, fees, courses, hostel, sports, faculty, alumni, or internships I can help with?"
        
        return "Bot: Let me connect you to a human advisor for detailed assistance."
    
    def chat(self):
        """Start the chat interface"""
        print("\n" + "="*60)
        print("ADVANCED COLLEGE HELP DESK CHATBOT")
        print("="*60)
        print("Type 'quit' to exit")
        print("I can help you with:")
        print("  • Admissions & Eligibility")
        print("  • Fee Structure & Scholarships")
        print("  • Courses & Programs")
        print("  • Placement Records")
        print("  • Campus Facilities")
        print("  • Exam Schedule")
        print("  • Holidays")
        print("  • Transport")
        print("  • Hostel (NEW!)")
        print("  • Sports (NEW!)")
        print("  • Faculty (NEW!)")
        print("  • Alumni (NEW!)")
        print("  • Internship (NEW!)")
        print("-"*60)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\nBot: Thank you for chatting! Visit our website for more info. Have a great day!")
                break
            
            if not user_input:
                print("Bot: Please type your question.")
                continue
            
            # Get response
            response = self.get_response(user_input)
            print(response)
            
            # Store conversation context
            self.context.append((user_input, response))
            if len(self.context) > 10:
                self.context.pop(0)

# Run the chatbot
if __name__ == "__main__":
    bot = AdvancedCollegeChatbot()
    bot.chat()