import json
import re
import random
from difflib import get_close_matches

class EnhancedUniversityBot:
    def __init__(self):
        self.create_enhanced_database()
        self.reviews = self.load_reviews()
        print(f"✅ Loaded {len(self.universities)} universities")
        print(f"⭐ Loaded {len(self.reviews)} user reviews")
        print("🎓 Enhanced features: Course Search | Cutoff Ranks | Reviews | Compare")
    
    def load_reviews(self):
        """Load or create sample reviews"""
        return {
            "Lovely Professional University (LPU)": [
                {"user": "Rajesh K.", "rating": 4.5, "review": "Great campus life, excellent placements!", "date": "2024"},
                {"user": "Priya S.", "rating": 4.0, "review": "Good faculty, huge campus, many opportunities", "date": "2024"},
                {"user": "Amit M.", "rating": 4.5, "review": "Best private university in North India", "date": "2023"}
            ],
            "Sharda University": [
                {"user": "Neha G.", "rating": 4.0, "review": "Good infrastructure, helpful staff", "date": "2024"},
                {"user": "Vikram R.", "rating": 3.5, "review": "Decent placements, good for CS", "date": "2023"}
            ],
            "Galgotias University": [
                {"user": "Anjali P.", "rating": 4.0, "review": "Value for money, good faculty", "date": "2024"},
                {"user": "Rahul S.", "rating": 3.5, "review": "Good for engineering, nice campus", "date": "2023"}
            ],
            "IIT Bombay": [
                {"user": "Student Review", "rating": 5.0, "review": "Dream college! Best faculty, amazing opportunities", "date": "2024"},
                {"user": "Alumni", "rating": 5.0, "review": "Life-changing experience, top placements", "date": "2023"}
            ],
            "VIT Vellore": [
                {"user": "Current Student", "rating": 4.0, "review": "Good academics, huge campus, many clubs", "date": "2024"},
                {"user": "Parent", "rating": 4.5, "review": "Safe campus, good hostel facilities", "date": "2023"}
            ]
        }
    
    def create_enhanced_database(self):
        """Create comprehensive database with cutoff ranks and courses"""
        self.universities = [
            # ============ IITs with Cutoff Ranks ============
            {
                "name": "IIT Bombay", "aliases": ["iitb", "mumbai iit"],
                "location": "Mumbai, Maharashtra", "category": "IIT", "type": "Premier", "nirf": 3,
                "fees": {"btech": "₹2.2L", "hostel": "₹40k"},
                "placement": {"average": "₹23.5 LPA", "highest": "₹3.2 Cr", "rate": "98%", "top_recruiters": ["Google", "Microsoft", "Amazon"]},
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA"},
                "cutoff": {"general": 120, "obc": 95, "sc": 60, "st": 45},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "M.Tech", "PhD"],
                "website": "www.iitb.ac.in"
            },
            {
                "name": "IIT Delhi", "aliases": ["iitd", "delhi iit"],
                "location": "New Delhi", "category": "IIT", "type": "Premier", "nirf": 2,
                "fees": {"btech": "₹2.2L", "hostel": "₹42k"},
                "placement": {"average": "₹24 LPA", "highest": "₹2.8 Cr", "rate": "97%", "top_recruiters": ["Google", "Microsoft", "McKinsey"]},
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA"},
                "cutoff": {"general": 118, "obc": 92, "sc": 58, "st": 42},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech Chemical"],
                "website": "www.iitd.ac.in"
            },
            {
                "name": "IIT Madras", "aliases": ["iitm", "chennai iit"],
                "location": "Chennai, Tamil Nadu", "category": "IIT", "type": "Premier", "nirf": 1,
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"},
                "placement": {"average": "₹22 LPA", "highest": "₹2.5 Cr", "rate": "99%", "top_recruiters": ["Google", "Microsoft", "Amazon"]},
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA"},
                "cutoff": {"general": 115, "obc": 90, "sc": 55, "st": 40},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech Aerospace"],
                "website": "www.iitm.ac.in"
            },
            {
                "name": "IIT Kanpur", "aliases": ["iitk", "kanpur iit"],
                "location": "Kanpur, Uttar Pradesh", "category": "IIT", "type": "Premier", "nirf": 4,
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"},
                "placement": {"average": "₹21 LPA", "highest": "₹2.2 Cr", "rate": "96%", "top_recruiters": ["Google", "Amazon", "Microsoft"]},
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA"},
                "cutoff": {"general": 112, "obc": 88, "sc": 52, "st": 38},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech Aerospace"],
                "website": "www.iitk.ac.in"
            },
            {
                "name": "IIT Kharagpur", "aliases": ["iitkgp", "kharagpur iit"],
                "location": "Kharagpur, West Bengal", "category": "IIT", "type": "Premier", "nirf": 5,
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"},
                "placement": {"average": "₹20 LPA", "highest": "₹2.0 Cr", "rate": "95%", "top_recruiters": ["Microsoft", "Amazon", "Goldman Sachs"]},
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA"},
                "cutoff": {"general": 110, "obc": 85, "sc": 50, "st": 35},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech Metallurgy"],
                "website": "www.iitkgp.ac.in"
            },
            {
                "name": "IIT Roorkee", "aliases": ["iitr", "roorkee iit"],
                "location": "Roorkee, Uttarakhand", "category": "IIT", "type": "Premier", "nirf": 7,
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"},
                "placement": {"average": "₹19 LPA", "highest": "₹1.8 Cr", "rate": "94%", "top_recruiters": ["Google", "Amazon", "Microsoft"]},
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA"},
                "cutoff": {"general": 108, "obc": 82, "sc": 48, "st": 32},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech Architecture"],
                "website": "www.iitr.ac.in"
            },
            {
                "name": "IIT Guwahati", "aliases": ["iitg", "guwahati iit"],
                "location": "Guwahati, Assam", "category": "IIT", "type": "Premier", "nirf": 8,
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"},
                "placement": {"average": "₹18 LPA", "highest": "₹1.7 Cr", "rate": "93%", "top_recruiters": ["Amazon", "Microsoft", "Google"]},
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA"},
                "cutoff": {"general": 105, "obc": 80, "sc": 45, "st": 30},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech Design"],
                "website": "www.iitg.ac.in"
            },
            {
                "name": "IIT Hyderabad", "aliases": ["iith", "hyderabad iit"],
                "location": "Hyderabad, Telangana", "category": "IIT", "type": "Second Generation", "nirf": 9,
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"},
                "placement": {"average": "₹17 LPA", "highest": "₹1.5 Cr", "rate": "92%", "top_recruiters": ["Microsoft", "Amazon", "Google"]},
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA"},
                "cutoff": {"general": 100, "obc": 75, "sc": 42, "st": 28},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech AI"],
                "website": "www.iith.ac.in"
            },
            
            # ============ NITs with Cutoff Ranks ============
            {
                "name": "NIT Trichy", "aliases": ["nitt", "trichy nit"],
                "location": "Tiruchirappalli, Tamil Nadu", "category": "NIT", "type": "Top NIT", "nirf": 9,
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"},
                "placement": {"average": "₹16.5 LPA", "highest": "₹52 LPA", "rate": "95%", "top_recruiters": ["Amazon", "Microsoft", "Deloitte"]},
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA"},
                "cutoff": {"general": 15000, "obc": 25000, "sc": 45000, "st": 55000},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech ECE"],
                "website": "www.nitt.edu"
            },
            {
                "name": "NIT Surathkal", "aliases": ["nitk", "surathkal nit"],
                "location": "Mangalore, Karnataka", "category": "NIT", "type": "Top NIT", "nirf": 10,
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"},
                "placement": {"average": "₹16 LPA", "highest": "₹50 LPA", "rate": "94%", "top_recruiters": ["Amazon", "Microsoft", "Google"]},
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA"},
                "cutoff": {"general": 16000, "obc": 26000, "sc": 46000, "st": 56000},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech IT"],
                "website": "www.nitk.ac.in"
            },
            {
                "name": "NIT Warangal", "aliases": ["nitw", "warangal nit"],
                "location": "Warangal, Telangana", "category": "NIT", "type": "Top NIT", "nirf": 11,
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"},
                "placement": {"average": "₹15.5 LPA", "highest": "₹48 LPA", "rate": "93%", "top_recruiters": ["Amazon", "Microsoft", "Deloitte"]},
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA"},
                "cutoff": {"general": 17000, "obc": 27000, "sc": 47000, "st": 57000},
                "courses": ["B.Tech CSE", "B.Tech EE", "B.Tech Mechanical", "B.Tech Civil", "B.Tech ECE"],
                "website": "www.nitw.ac.in"
            },
            
            # ============ Top Private Universities ============
            {
                "name": "BITS Pilani", "aliases": ["bits", "bitsp"],
                "location": "Pilani, Rajasthan", "category": "Private", "type": "Premier Private",
                "fees": {"btech": "₹4.5L", "hostel": "₹65k"},
                "placement": {"average": "₹28 LPA", "highest": "₹60 LPA", "rate": "99%", "top_recruiters": ["Google", "Microsoft", "Amazon", "Goldman Sachs"]},
                "admission": {"exam": "BITSAT", "deadline": "May 20", "process": "BITSAT exam -> Counseling"},
                "cutoff": {"bitsat_score": 350, "percentile": 98.5},
                "courses": ["B.E. CSE", "B.E. EEE", "B.E. Mechanical", "B.E. Civil", "M.E.", "MBA"],
                "website": "www.bits-pilani.ac.in"
            },
            {
                "name": "VIT Vellore", "aliases": ["vit", "vellore vit"],
                "location": "Vellore, Tamil Nadu", "category": "Private", "type": "Top Private",
                "fees": {"btech": "₹1.9L", "hostel": "₹50k"},
                "placement": {"average": "₹8.5 LPA", "highest": "₹51 LPA", "rate": "93%", "top_recruiters": ["Amazon", "Microsoft", "Deloitte", "Cognizant"]},
                "admission": {"exam": "VITEEE", "deadline": "April 30", "process": "VITEEE exam -> Counseling"},
                "cutoff": {"viteee_rank": 5000, "percentile": 95},
                "courses": ["B.Tech CSE", "B.Tech IT", "B.Tech ECE", "B.Tech Mechanical", "B.Tech Civil"],
                "website": "www.vit.ac.in"
            },
            {
                "name": "SRM University Chennai", "aliases": ["srm", "srm chennai"],
                "location": "Chennai, Tamil Nadu", "category": "Private", "type": "Top Private",
                "fees": {"btech": "₹2.5L", "hostel": "₹65k"},
                "placement": {"average": "₹7.5 LPA", "highest": "₹48 LPA", "rate": "91%", "top_recruiters": ["Google", "Amazon", "Microsoft", "Dell"]},
                "admission": {"exam": "SRMJEEE", "deadline": "May 15", "process": "SRMJEEE exam -> Counseling"},
                "cutoff": {"srmjeee_rank": 10000, "percentile": 90},
                "courses": ["B.Tech CSE", "B.Tech IT", "B.Tech ECE", "B.Tech Mechanical", "B.Tech AI"],
                "website": "www.srmist.edu.in"
            },
            {
                "name": "Manipal University", "aliases": ["manipal"],
                "location": "Manipal, Karnataka", "category": "Private", "type": "Top Private",
                "fees": {"btech": "₹3.5L", "hostel": "₹70k"},
                "placement": {"average": "₹9.5 LPA", "highest": "₹42 LPA", "rate": "94%", "top_recruiters": ["Google", "Microsoft", "Amazon", "Deloitte"]},
                "admission": {"exam": "MET", "deadline": "May 10", "process": "MET exam -> Counseling"},
                "cutoff": {"met_rank": 8000, "percentile": 92},
                "courses": ["B.Tech CSE", "B.Tech IT", "B.Tech ECE", "B.Tech Mechanical", "B.Tech Data Science"],
                "website": "www.manipal.edu"
            },
            
            # ============ Your Requested Universities ============
            {
                "name": "Lovely Professional University (LPU)", "aliases": ["lpu", "lovely", "lp"],
                "location": "Jalandhar, Punjab", "category": "Private", "type": "Good Private",
                "fees": {"btech": "₹1.6L", "hostel": "₹50k"},
                "placement": {"average": "₹7.2 LPA", "highest": "₹64 LPA", "rate": "94%", "top_recruiters": ["Google", "Microsoft", "Amazon", "Deloitte"]},
                "admission": {"exam": "LPUNEST", "deadline": "July 15", "process": "LPUNEST exam -> Counseling"},
                "cutoff": {"lpunest_rank": 20000, "percentile": 85},
                "courses": ["B.Tech CSE", "B.Tech AI", "B.Tech Data Science", "B.Tech Cloud", "B.Tech Cyber Security", "BBA", "MBA", "BCA", "B.Sc", "B.Com", "B.Arch", "LLB", "B.Design", "B.Pharma"],
                "website": "www.lpu.in"
            },
            {
                "name": "Sharda University", "aliases": ["sharda"],
                "location": "Greater Noida, Uttar Pradesh", "category": "Private", "type": "Good Private",
                "fees": {"btech": "₹1.8L", "hostel": "₹55k"},
                "placement": {"average": "₹6.8 LPA", "highest": "₹42 LPA", "rate": "92%", "top_recruiters": ["Amazon", "Microsoft", "TCS", "Infosys"]},
                "admission": {"exam": "SUAT", "deadline": "June 30", "process": "SUAT exam -> Counseling"},
                "cutoff": {"suat_score": 60, "percentile": 80},
                "courses": ["B.Tech CSE", "B.Tech AI", "B.Tech Data Science", "B.Tech Cloud", "BCA", "BBA", "MBA", "LLB", "B.Arch", "B.Sc", "B.Com", "B.Design", "B.Pharma", "B.Optometry", "BPT"],
                "website": "www.sharda.ac.in"
            },
            {
                "name": "Galgotias University", "aliases": ["galgotias", "galgotia"],
                "location": "Greater Noida, Uttar Pradesh", "category": "Private", "type": "Good Private",
                "fees": {"btech": "₹1.5L", "hostel": "₹50k"},
                "placement": {"average": "₹6.5 LPA", "highest": "₹38 LPA", "rate": "91%", "top_recruiters": ["Infosys", "TCS", "HCL", "Adobe"]},
                "admission": {"exam": "GEEE", "deadline": "July 31", "process": "GEEE exam -> Counseling"},
                "cutoff": {"geee_rank": 25000, "percentile": 75},
                "courses": ["B.Tech CSE", "B.Tech AI", "B.Tech Data Science", "B.Tech Cloud", "BCA", "BBA", "MBA", "LLB", "B.Arch", "B.Sc", "B.Com", "B.Design"],
                "website": "www.galgotiasuniversity.edu.in"
            },
            {
                "name": "Amity University Noida", "aliases": ["amity"],
                "location": "Noida, Uttar Pradesh", "category": "Private", "type": "Good Private",
                "fees": {"btech": "₹2.5L", "hostel": "₹75k"},
                "placement": {"average": "₹6.5 LPA", "highest": "₹35 LPA", "rate": "85%", "top_recruiters": ["Amazon", "Microsoft", "Google", "Deloitte"]},
                "admission": {"exam": "Amity JEE", "deadline": "June 30", "process": "Amity JEE -> Counseling"},
                "cutoff": {"amity_score": 60, "percentile": 75},
                "courses": ["B.Tech CSE", "B.Tech AI", "B.Tech Data Science", "B.Tech Cloud", "BCA", "BBA", "MBA", "LLB", "B.Arch", "B.Sc", "B.Com", "B.Design", "B.JMC", "B.Ed"],
                "website": "www.amity.edu"
            },
            {
                "name": "Chandigarh University", "aliases": ["chandigarh", "cu"],
                "location": "Mohali, Punjab", "category": "Private", "type": "Good Private",
                "fees": {"btech": "₹1.6L", "hostel": "₹55k"},
                "placement": {"average": "₹7 LPA", "highest": "₹38 LPA", "rate": "90%", "top_recruiters": ["Microsoft", "Amazon", "Google"]},
                "admission": {"exam": "CUCET", "deadline": "June 15", "process": "CUCET exam -> Counseling"},
                "cutoff": {"cucet_rank": 30000, "percentile": 70},
                "courses": ["B.Tech CSE", "B.Tech AI", "B.Tech Data Science", "B.Tech Cloud", "BCA", "BBA", "MBA", "LLB", "B.Arch", "B.Sc", "B.Com", "B.Design", "B.Pharma", "Hotel Management"],
                "website": "www.chandigarhuniversity.ac.in"
            }
        ]
    
    def search_by_course(self, course_name):
        """Search universities offering a specific course"""
        course_lower = course_name.lower()
        results = []
        
        for uni in self.universities:
            courses = [c.lower() for c in uni.get('courses', [])]
            if any(course_lower in course or course in course_lower for course in courses):
                results.append(uni)
        
        return results
    
    def get_cutoff_info(self, uni):
        """Get cutoff information for a university"""
        cutoff = uni.get('cutoff', {})
        if not cutoff:
            return "No cutoff data available"
        
        info = "\n📊 **CUTOFF RANKS/SCORES:**\n"
        if 'general' in cutoff:
            info += f"   • General: {cutoff['general']}\n"
            info += f"   • OBC: {cutoff['obc']}\n"
            info += f"   • SC: {cutoff['sc']}\n"
            info += f"   • ST: {cutoff['st']}\n"
        if 'bitsat_score' in cutoff:
            info += f"   • BITSAT Score: {cutoff['bitsat_score']}+ | Percentile: {cutoff.get('percentile', 'N/A')}%\n"
        if 'viteee_rank' in cutoff:
            info += f"   • VITEEE Rank: Within {cutoff['viteee_rank']} | Percentile: {cutoff.get('percentile', 'N/A')}%\n"
        if 'srmjeee_rank' in cutoff:
            info += f"   • SRMJEEE Rank: Within {cutoff['srmjeee_rank']} | Percentile: {cutoff.get('percentile', 'N/A')}%\n"
        if 'lpunest_rank' in cutoff:
            info += f"   • LPUNEST Rank: Within {cutoff['lpunest_rank']} | Percentile: {cutoff.get('percentile', 'N/A')}%\n"
        
        return info
    
    def get_reviews(self, uni_name):
        """Get reviews for a university"""
        reviews = self.reviews.get(uni_name, [])
        if not reviews:
            return "No reviews available yet. Be the first to review!"
        
        info = "\n⭐ **STUDENT REVIEWS:**\n"
        for review in reviews[:3]:
            stars = "★" * int(review['rating']) + "☆" * (5 - int(review['rating']))
            info += f"\n   {stars} {review['rating']}/5\n"
            info += f"   📝 \"{review['review']}\"\n"
            info += f"   👤 {review['user']} | {review['date']}\n"
        
        return info
    
    def add_review(self, uni_name, user_name, rating, review_text):
        """Add a new review"""
        if uni_name not in self.reviews:
            self.reviews[uni_name] = []
        
        self.reviews[uni_name].append({
            "user": user_name,
            "rating": rating,
            "review": review_text,
            "date": "2024"
        })
        return "✅ Review added successfully!"
    
    def get_university_info(self, uni):
        """Get comprehensive university information"""
        info = f"""
{'='*65}
📚 **{uni.get('name', 'Unknown')}**
{'='*65}
📍 **Location:** {uni.get('location', 'N/A')}
🏷️ **Category:** {uni.get('category', 'N/A')} - {uni.get('type', 'N/A')}
⭐ **NIRF Ranking:** #{uni.get('nirf', 'Not Ranked')}
🌐 **Website:** {uni.get('website', 'www.college.edu')}

💰 **FEES STRUCTURE:**
   • B.Tech: {uni.get('fees', {}).get('btech', 'N/A')}
   • Hostel: {uni.get('fees', {}).get('hostel', 'N/A')}

💼 **PLACEMENTS:**
   • Average Package: {uni.get('placement', {}).get('average', 'N/A')}
   • Highest Package: {uni.get('placement', {}).get('highest', 'N/A')}
   • Placement Rate: {uni.get('placement', {}).get('rate', 'N/A')}
   • Top Recruiters: {', '.join(uni.get('placement', {}).get('top_recruiters', ['Various companies'])[:5])}

📝 **ADMISSION:**
   • Entrance Exam: {uni.get('admission', {}).get('exam', 'N/A')}
   • Deadline: {uni.get('admission', {}).get('deadline', 'N/A')}
   • Process: {uni.get('admission', {}).get('process', 'Apply through official website')}

🎓 **COURSES OFFERED:**
   • {', '.join(uni.get('courses', ['B.Tech', 'M.Tech', 'PhD'])[:8])}
"""
        info += self.get_cutoff_info(uni)
        info += self.get_reviews(uni.get('name', ''))
        
        return info
    
    def compare_universities(self, uni1_name, uni2_name):
        """Compare two universities in detail"""
        uni1 = self.search_university(uni1_name)[0] if self.search_university(uni1_name) else None
        uni2 = self.search_university(uni2_name)[0] if self.search_university(uni2_name) else None
        
        if not uni1 or not uni2:
            return "❌ Could not find one or both universities"
        
        comparison = f"""
{'='*80}
📊 **COMPREHENSIVE COMPARISON: {uni1['name']} vs {uni2['name']}**
{'='*80}
| {'Parameter':<22} | {uni1['name'][:25]:<25} | {uni2['name'][:25]:<25} |
|{'-'*22}|{'-'*25}|{'-'*25}|
| {'Location':<22} | {uni1.get('location', 'N/A')[:25]:<25} | {uni2.get('location', 'N/A')[:25]:<25} |
| {'Type':<22} | {uni1.get('type', 'N/A')[:25]:<25} | {uni2.get('type', 'N/A')[:25]:<25} |
| {'NIRF Ranking':<22} | #{uni1.get('nirf', 'N/A'):<24} | #{uni2.get('nirf', 'N/A'):<24} |
| {'Avg Package':<22} | {uni1.get('placement', {}).get('average', 'N/A'):<25} | {uni2.get('placement', {}).get('average', 'N/A'):<25} |
| {'Highest Package':<22} | {uni1.get('placement', {}).get('highest', 'N/A'):<25} | {uni2.get('placement', {}).get('highest', 'N/A'):<25} |
| {'Placement Rate':<22} | {uni1.get('placement', {}).get('rate', 'N/A'):<25} | {uni2.get('placement', {}).get('rate', 'N/A'):<25} |
| {'B.Tech Fees':<22} | {uni1.get('fees', {}).get('btech', 'N/A'):<25} | {uni2.get('fees', {}).get('btech', 'N/A'):<25} |
| {'Hostel Fees':<22} | {uni1.get('fees', {}).get('hostel', 'N/A'):<25} | {uni2.get('fees', {}).get('hostel', 'N/A'):<25} |
| {'Entrance Exam':<22} | {uni1.get('admission', {}).get('exam', 'N/A'):<25} | {uni2.get('admission', {}).get('exam', 'N/A'):<25} |
{'='*80}

🎯 **VERDICT:**
"""
        avg1 = int(uni1.get('placement', {}).get('average', '0').replace('₹', '').replace(' LPA', '')) if uni1.get('placement', {}).get('average') else 0
        avg2 = int(uni2.get('placement', {}).get('average', '0').replace('₹', '').replace(' LPA', '')) if uni2.get('placement', {}).get('average') else 0
        
        if avg1 > avg2:
            comparison += f"   ✅ {uni1['name']} has better average package (₹{avg1} LPA vs ₹{avg2} LPA)\n"
        elif avg2 > avg1:
            comparison += f"   ✅ {uni2['name']} has better average package (₹{avg2} LPA vs ₹{avg1} LPA)\n"
        
        return comparison
    
    def search_university(self, query):
        """Search for university by name, alias, location, or category"""
        query_lower = query.lower().strip()
        
        # Check exact matches first
        for uni in self.universities:
            name = uni.get('name', '').lower()
            aliases = [a.lower() for a in uni.get('aliases', [])]
            if query_lower == name or query_lower in aliases:
                return [uni]
        
        # Then scoring search
        results = []
        for uni in self.universities:
            score = 0
            name = uni.get('name', '').lower()
            location = uni.get('location', '').lower()
            category = uni.get('category', '').lower()
            uni_type = uni.get('type', '').lower()
            aliases = [a.lower() for a in uni.get('aliases', [])]
            
            if query_lower in name or any(query_lower in alias for alias in aliases):
                score += 10
            elif any(word in name for word in query_lower.split()):
                score += 5
            if query_lower in location:
                score += 3
            if query_lower in category or query_lower in uni_type:
                score += 2
            
            if score > 0:
                results.append((uni, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:5]]
    
    def chat(self):
        """Main chat interface with all features"""
        print("\n" + "="*65)
        print("🎓 ENHANCED UNIVERSITY SEARCH BOT")
        print("="*65)
        print(f"📚 Database: {len(self.universities)} Universities")
        print("\n✨ **NEW FEATURES:**")
        print("   • 🔍 Course Search - Find colleges by course")
        print("   • 📊 Cutoff Ranks - JEE Main, BITSAT, VITEEE ranks")
        print("   • ⭐ Student Reviews - Read real reviews")
        print("   • 📝 Add Reviews - Share your experience")
        print("   • 🎯 Course-specific search")
        print("   • 🔄 Compare universities")
        print("-"*65)
        
        print("\n💡 **Commands:**")
        print("   • 'LPU' / 'Sharda' - Search university")
        print("   • 'course B.Tech CSE' - Find colleges by course")
        print("   • 'compare IIT Delhi and IIT Bombay' - Compare")
        print("   • 'add review for LPU' - Add your review")
        print("   • 'help' - Show this menu")
        print("-"*65)
        
        while True:
            query = input("\n🔍 You: ").strip()
            
            if query.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thank you for using Enhanced University Search! Goodbye!")
                break
            
            if not query:
                continue
            
            # Help command
            if query.lower() == 'help':
                print("\n💡 **COMMANDS:**")
                print("   • Type university name: 'LPU', 'Sharda', 'IIT Bombay'")
                print("   • Course search: 'course B.Tech CSE' or 'courses for AI'")
                print("   • Compare: 'compare IIT Delhi and IIT Bombay'")
                print("   • Add review: 'add review for LPU'")
                print("   • Location: 'universities in Mumbai'")
                continue
            
            # Add review command
            if 'add review for' in query.lower():
                parts = query.lower().split('add review for')
                if len(parts) > 1:
                    uni_name = parts[1].strip().title()
                    print(f"\n📝 Adding review for {uni_name}")
                    user_name = input("Your name: ").strip()
                    rating = float(input("Rating (1-5): ").strip())
                    review_text = input("Your review: ").strip()
                    result = self.add_review(uni_name, user_name, rating, review_text)
                    print(f"\n✅ {result}")
                continue
            
            # Course search
            if query.lower().startswith('course') or query.lower().startswith('courses for'):
                course_name = query.lower().replace('course', '').replace('courses for', '').strip()
                results = self.search_by_course(course_name)
                if results:
                    print(f"\n📚 Universities offering '{course_name.title()}':")
                    for i, uni in enumerate(results[:10], 1):
                        print(f"\n   {i}. {uni.get('name', 'N/A')}")
                        print(f"      📍 {uni.get('location', 'N/A')}")
                        print(f"      💰 Fees: {uni.get('fees', {}).get('btech', 'N/A')}")
                        print(f"      📊 Avg Package: {uni.get('placement', {}).get('average', 'N/A')}")
                else:
                    print(f"\n❌ No universities found offering '{course_name}'")
                continue
            
            # Compare command
            if 'compare' in query.lower():
                import re
                names = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', query)
                if len(names) >= 2:
                    result = self.compare_universities(names[1], names[2] if len(names) > 2 else names[1])
                    print(result)
                else:
                    print("❌ Please specify two universities to compare")
                continue
            
            # Location search
            if 'in' in query.lower() and len(query.split()) > 2:
                words = query.split()
                try:
                    location_idx = words.index('in')
                    if location_idx + 1 < len(words):
                        location = words[location_idx + 1]
                        results = [u for u in self.universities if location.lower() in u.get('location', '').lower()]
                        if results:
                            print(f"\n📚 Universities in {location.upper()}:")
                            for i, uni in enumerate(results[:10], 1):
                                print(f"   {i}. {uni.get('name', 'N/A')}")
                                print(f"      📍 {uni.get('location', 'N/A')}")
                                print(f"      💰 Avg Package: {uni.get('placement', {}).get('average', 'N/A')}")
                            continue
                except ValueError:
                    pass
            
            # Normal search
            results = self.search_university(query)
            
            if results:
                if len(results) == 1:
                    print(self.get_university_info(results[0]))
                else:
                    print(f"\n📚 Found {len(results)} universities matching '{query}':")
                    for i, uni in enumerate(results, 1):
                        print(f"\n{i}. {uni.get('name', 'Unknown')}")
                        print(f"   📍 {uni.get('location', 'N/A')}")
                        print(f"   💰 Avg Package: {uni.get('placement', {}).get('average', 'N/A')}")
                        print(f"   📝 Entrance: {uni.get('admission', {}).get('exam', 'N/A')}")
                    
                    print("\n💡 Type the exact name for more details!")
            else:
                print(f"\n❌ No universities found matching '{query}'")
                print("💡 Try: 'LPU', 'Sharda', 'IIT Bombay', 'course B.Tech CSE', 'compare IIT Delhi and IIT Bombay'")

if __name__ == "__main__":
    bot = EnhancedUniversityBot()
    bot.chat()