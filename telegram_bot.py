import json
import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load intents
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Simple keyword matching (reuse from your chatbot)
def get_response(user_input):
    user_lower = user_input.lower()
    
    # Simple response logic
    if any(word in user_lower for word in ['hi', 'hello', 'hey']):
        return "Hello! Welcome to College Help Bot! Ask me about admissions, fees, courses, placements, hostel, sports, etc."
    elif any(word in user_lower for word in ['fee', 'cost', 'price', 'tuition']):
        return "📚 Fee Structure:\n• Engineering: Rs 1.5L/year\n• MBA: Rs 2L/year\n• BSc: Rs 80k/year\n\nScholarships available!"
    elif any(word in user_lower for word in ['course', 'program', 'degree', 'btech']):
        return "🎓 Courses Offered:\n• B.Tech (CS, IT, Mechanical, Civil, Electrical)\n• MBA\n• BCA, MCA\n• BSc, MSc\n• PhD programs"
    elif any(word in user_lower for word in ['placement', 'job', 'package', 'recruiter']):
        return "💼 Placement Record:\n• 95% placement rate\n• Average package: Rs 8.5 LPA\n• Top recruiters: Google, Microsoft, Amazon, Deloitte"
    elif any(word in user_lower for word in ['hostel', 'accommodation', 'room']):
        return "🏠 Hostel Details:\n• Fees: Rs 60,000/year\n• In-time: 9 PM\n• Facilities: WiFi, Gym, Common Room, Mess"
    elif any(word in user_lower for word in ['sports', 'cricket', 'football', 'gym']):
        return "⚽ Sports Facilities:\n• Cricket ground\n• Football ground\n• Basketball court\n• Swimming pool\n• Modern gymnasium"
    elif any(word in user_lower for word in ['admission', 'apply', 'eligibility']):
        return "📝 Admission Requirements:\n• Minimum 60% in 12th\n• Entrance exam required\n• Application deadline: May 30th, 2026"
    elif any(word in user_lower for word in ['scholarship', 'financial', 'aid']):
        return "💰 Scholarships:\n• Merit-based: Up to 100%\n• Sports quota: 50% waiver\n• Need-based financial aid available"
    elif any(word in user_lower for word in ['exam', 'test', 'semester']):
        return "📅 Exam Schedule:\n• Mid-term: Sept 15-25\n• Finals: Dec 1-15\n• Practicals start 1 week before theory"
    elif any(word in user_lower for word in ['bye', 'goodbye', 'thanks', 'thank']):
        return "You're welcome! Feel free to ask anytime. Have a great day! 🎓"
    else:
        return "🤔 I can help with:\n• Admissions\n• Fees & Scholarships\n• Courses\n• Placements\n• Hostel & Sports\n• Exam schedules\n\nTry asking something specific!"

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /start is issued."""
    user = update.effective_user
    welcome_msg = f"""
🎓 *Welcome to College Help Bot, {user.first_name}!*

I'm your virtual college assistant. I can help you with:

📌 *Admissions* - Eligibility, process, deadlines
💰 *Fees* - Tuition, scholarships, payment options
📚 *Courses* - B.Tech, MBA, BCA, and more
💼 *Placements* - Packages, recruiters, preparation
🏠 *Hostel* - Fees, rules, facilities
⚽ *Sports* - Grounds, courts, gym, quota
📅 *Exams* - Schedule, dates, practicals

*Quick Commands:*
/help - Show this menu
/contact - Get college contact info
/website - Visit college website

Just type your question naturally!
    """
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /help is issued."""
    help_text = """
🤖 *College Help Bot - Help Guide*

*What I can do:*
• Answer questions about college admissions
• Provide fee structure and scholarship info
• List available courses and programs
• Share placement records and recruiters
• Explain hostel rules and facilities
• Describe sports facilities and quotas
• Give exam schedules and important dates

*How to use:*
Simply type your question naturally, like:
• "What are the admission requirements?"
• "How much are the fees for B.Tech?"
• "Tell me about placements"
• "Hostel facilities and rules"

*Commands:*
/start - Restart the bot
/help - Show this help
/contact - Get contact information
/website - Visit college website

*Pro tip:* Ask about multiple topics in one message!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send contact information."""
    contact_text = """
📞 *College Contact Information*

*Admissions Office:*
📱 +91-123-456-7890
📧 admissions@college.edu

*Placement Cell:*
📱 +91-123-456-7891
📧 placement@college.edu

*Hostel Office:*
📱 +91-123-456-7892
📧 hostel@college.edu

*Website:* www.college.edu
*Address:* College Road, City - 123456
    """
    await update.message.reply_text(contact_text, parse_mode='Markdown')

async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send website link."""
    await update.message.reply_text("🌐 Visit our official website: https://www.college.edu\n\nFor latest updates, admissions, and announcements!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages."""
    user_message = update.message.text
    response = get_response(user_message)
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token from @BotFather
    # To get a token: 
    # 1. Open Telegram and search for @BotFather
    # 2. Send /newbot and follow instructions
    # 3. Copy the token you receive
    
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # ← REPLACE THIS!
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️ Please get a bot token from @BotFather on Telegram first!")
        print("Steps:")
        print("1. Open Telegram")
        print("2. Search for @BotFather")
        print("3. Send /newbot")
        print("4. Choose a name (e.g., College Help Bot)")
        print("5. Choose a username (e.g., college_help_bot)")
        print("6. Copy the token and paste it above")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CommandHandler("website", website_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    print("🤖 Telegram bot is running...")
    print("Press Ctrl+C to stop")
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()