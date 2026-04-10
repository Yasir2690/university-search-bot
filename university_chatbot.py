import json
import re
import random
from difflib import get_close_matches

class UniversityChatbot:
    def __init__(self):
        # Create university database with aliases
        self.create_sample_data()
        print(f"✅ Loaded {len(self.universities)} universities with alias support")
    
    def create_sample_data(self):
        """Create comprehensive sample data with all required fields and aliases"""
        self.universities = [
            # ============ IITs (Indian Institutes of Technology) ============
            {
                "name": "IIT Bombay", 
                "aliases": ["iitb", "mumbai iit", "iit mumbai", "bombay iit"], 
                "location": "Mumbai, Maharashtra", 
                "category": "IIT", 
                "type": "Premier", 
                "nirf": 3, 
                "fees": {"btech": "₹2.2L", "hostel": "₹40k"}, 
                "placement": {"average": "₹23.5 LPA", "highest": "₹3.2 Cr", "rate": "98%", "top_recruiters": ["Google", "Microsoft", "Amazon"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Delhi", 
                "aliases": ["iitd", "delhi iit", "iit delhi"], 
                "location": "New Delhi", 
                "category": "IIT", 
                "type": "Premier", 
                "nirf": 2, 
                "fees": {"btech": "₹2.2L", "hostel": "₹42k"}, 
                "placement": {"average": "₹24 LPA", "highest": "₹2.8 Cr", "rate": "97%", "top_recruiters": ["Google", "Microsoft", "McKinsey"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Madras", 
                "aliases": ["iitm", "chennai iit", "iit chennai", "madras iit"], 
                "location": "Chennai, Tamil Nadu", 
                "category": "IIT", 
                "type": "Premier", 
                "nirf": 1, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹22 LPA", "highest": "₹2.5 Cr", "rate": "99%", "top_recruiters": ["Google", "Microsoft", "Amazon"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Kanpur", 
                "aliases": ["iitk", "kanpur iit"], 
                "location": "Kanpur, Uttar Pradesh", 
                "category": "IIT", 
                "type": "Premier", 
                "nirf": 4, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹21 LPA", "highest": "₹2.2 Cr", "rate": "96%", "top_recruiters": ["Google", "Amazon", "Microsoft"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Kharagpur", 
                "aliases": ["iitkgp", "kharagpur iit"], 
                "location": "Kharagpur, West Bengal", 
                "category": "IIT", 
                "type": "Premier", 
                "nirf": 5, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹20 LPA", "highest": "₹2.0 Cr", "rate": "95%", "top_recruiters": ["Microsoft", "Amazon", "Goldman Sachs"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Roorkee", 
                "aliases": ["iitr", "roorkee iit"], 
                "location": "Roorkee, Uttarakhand", 
                "category": "IIT", 
                "type": "Premier", 
                "nirf": 7, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹19 LPA", "highest": "₹1.8 Cr", "rate": "94%", "top_recruiters": ["Google", "Amazon", "Microsoft"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Guwahati", 
                "aliases": ["iitg", "guwahati iit"], 
                "location": "Guwahati, Assam", 
                "category": "IIT", 
                "type": "Premier", 
                "nirf": 8, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹18 LPA", "highest": "₹1.7 Cr", "rate": "93%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Hyderabad", 
                "aliases": ["iith", "hyderabad iit"], 
                "location": "Hyderabad, Telangana", 
                "category": "IIT", 
                "type": "Second Generation", 
                "nirf": 9, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹17 LPA", "highest": "₹1.5 Cr", "rate": "92%", "top_recruiters": ["Microsoft", "Amazon", "Google"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Indore", 
                "aliases": ["iiti", "indore iit"], 
                "location": "Indore, Madhya Pradesh", 
                "category": "IIT", 
                "type": "Second Generation", 
                "nirf": 10, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹16 LPA", "highest": "₹1.4 Cr", "rate": "91%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT BHU Varanasi", 
                "aliases": ["iit bhu", "bhu iit", "varanasi iit"], 
                "location": "Varanasi, Uttar Pradesh", 
                "category": "IIT", 
                "type": "Premier", 
                "nirf": 11, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹15.5 LPA", "highest": "₹1.3 Cr", "rate": "90%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Patna", 
                "aliases": ["iitp", "patna iit"], 
                "location": "Patna, Bihar", 
                "category": "IIT", 
                "type": "Second Generation", 
                "nirf": 12, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹14 LPA", "highest": "₹1.2 Cr", "rate": "89%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            {
                "name": "IIT Bhubaneswar", 
                "aliases": ["iit bbsr", "bhubaneswar iit"], 
                "location": "Bhubaneswar, Odisha", 
                "category": "IIT", 
                "type": "Second Generation", 
                "nirf": 13, 
                "fees": {"btech": "₹2.0L", "hostel": "₹38k"}, 
                "placement": {"average": "₹12.5 LPA", "highest": "₹95 LPA", "rate": "86%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Advanced", "deadline": "May 31", "process": "JEE Main -> JEE Advanced -> JoSAA Counseling"}
            },
            
            # ============ NITs (National Institutes of Technology) ============
            {
                "name": "NIT Trichy", 
                "aliases": ["nitt", "trichy nit", "nit tiruchirappalli"], 
                "location": "Tiruchirappalli, Tamil Nadu", 
                "category": "NIT", 
                "type": "Top NIT", 
                "nirf": 9, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹16.5 LPA", "highest": "₹52 LPA", "rate": "95%", "top_recruiters": ["Amazon", "Microsoft", "Deloitte"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Surathkal", 
                "aliases": ["nitk", "surathkal nit", "nit karnataka"], 
                "location": "Mangalore, Karnataka", 
                "category": "NIT", 
                "type": "Top NIT", 
                "nirf": 10, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹16 LPA", "highest": "₹50 LPA", "rate": "94%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Warangal", 
                "aliases": ["nitw", "warangal nit"], 
                "location": "Warangal, Telangana", 
                "category": "NIT", 
                "type": "Top NIT", 
                "nirf": 11, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹15.5 LPA", "highest": "₹48 LPA", "rate": "93%", "top_recruiters": ["Amazon", "Microsoft", "Deloitte"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Calicut", 
                "aliases": ["nitc", "calicut nit"], 
                "location": "Calicut, Kerala", 
                "category": "NIT", 
                "type": "Top NIT", 
                "nirf": 12, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹15 LPA", "highest": "₹45 LPA", "rate": "92%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Rourkela", 
                "aliases": ["nitrkl", "rourkela nit"], 
                "location": "Rourkela, Odisha", 
                "category": "NIT", 
                "type": "Top NIT", 
                "nirf": 13, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹14.5 LPA", "highest": "₹42 LPA", "rate": "91%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Durgapur", 
                "aliases": ["nitdgp", "durgapur nit"], 
                "location": "Durgapur, West Bengal", 
                "category": "NIT", 
                "type": "Good NIT", 
                "nirf": 14, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹14 LPA", "highest": "₹40 LPA", "rate": "90%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Hamirpur", 
                "aliases": ["nith", "hamirpur nit"], 
                "location": "Hamirpur, Himachal Pradesh", 
                "category": "NIT", 
                "type": "Good NIT", 
                "nirf": 15, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹13.5 LPA", "highest": "₹38 LPA", "rate": "89%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Patna", 
                "aliases": ["nitp", "patna nit"], 
                "location": "Patna, Bihar", 
                "category": "NIT", 
                "type": "Good NIT", 
                "nirf": 16, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹12.5 LPA", "highest": "₹35 LPA", "rate": "87%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Silchar", 
                "aliases": ["nits", "silchar nit"], 
                "location": "Silchar, Assam", 
                "category": "NIT", 
                "type": "Good NIT", 
                "nirf": 17, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹12 LPA", "highest": "₹34 LPA", "rate": "86%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Jalandhar", 
                "aliases": ["nitj", "jalandhar nit"], 
                "location": "Jalandhar, Punjab", 
                "category": "NIT", 
                "type": "Good NIT", 
                "nirf": 18, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹11.5 LPA", "highest": "₹32 LPA", "rate": "85%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            {
                "name": "NIT Goa", 
                "aliases": ["nit goa"], 
                "location": "Goa", 
                "category": "NIT", 
                "type": "Good NIT", 
                "nirf": 19, 
                "fees": {"btech": "₹1.5L", "hostel": "₹35k"}, 
                "placement": {"average": "₹11 LPA", "highest": "₹30 LPA", "rate": "84%", "top_recruiters": ["Amazon", "Microsoft", "Google"]}, 
                "admission": {"exam": "JEE Main", "deadline": "June 15", "process": "JEE Main -> JoSAA Counseling"}
            },
            
            # ============ IIITs (Indian Institutes of Information Technology) ============
            {
                "name": "IIIT Hyderabad", 
                "aliases": ["iiith", "hyderabad iiit"], 
                "location": "Hyderabad, Telangana", 
                "category": "IIIT", 
                "type": "Premier IIIT", 
                "fees": {"btech": "₹3.0L", "hostel": "₹50k"}, 
                "placement": {"average": "₹25 LPA", "highest": "₹56 LPA", "rate": "100%", "top_recruiters": ["Google", "Microsoft", "Amazon", "Facebook"]}, 
                "admission": {"exam": "JEE Main + UGEE", "deadline": "May 15", "process": "JEE Main -> UGEE -> Counseling"}
            },
            {
                "name": "IIIT Bangalore", 
                "aliases": ["iiitb", "bangalore iiit"], 
                "location": "Bangalore, Karnataka", 
                "category": "IIIT", 
                "type": "Good IIIT", 
                "fees": {"btech": "₹2.8L", "hostel": "₹45k"}, 
                "placement": {"average": "₹22 LPA", "highest": "₹48 LPA", "rate": "98%", "top_recruiters": ["Google", "Microsoft", "Amazon"]}, 
                "admission": {"exam": "JEE Main", "deadline": "May 15", "process": "JEE Main -> Counseling"}
            },
            {
                "name": "IIIT Delhi", 
                "aliases": ["iiitd", "delhi iiit"], 
                "location": "New Delhi", 
                "category": "IIIT", 
                "type": "Good IIIT", 
                "fees": {"btech": "₹2.8L", "hostel": "₹45k"}, 
                "placement": {"average": "₹21 LPA", "highest": "₹45 LPA", "rate": "97%", "top_recruiters": ["Google", "Microsoft", "Amazon"]}, 
                "admission": {"exam": "JEE Main", "deadline": "May 15", "process": "JEE Main -> Counseling"}
            },
            {
                "name": "IIIT Allahabad", 
                "aliases": ["iiita", "allahabad iiit"], 
                "location": "Allahabad, Uttar Pradesh", 
                "category": "IIIT", 
                "type": "Good IIIT", 
                "fees": {"btech": "₹2.5L", "hostel": "₹42k"}, 
                "placement": {"average": "₹18 LPA", "highest": "₹40 LPA", "rate": "95%", "top_recruiters": ["Google", "Microsoft", "Amazon"]}, 
                "admission": {"exam": "JEE Main", "deadline": "May 15", "process": "JEE Main -> Counseling"}
            },
            
            # ============ Premier Private Universities ============
            {
                "name": "BITS Pilani", 
                "aliases": ["bits", "bitsp", "pilani bits", "bits pilani"], 
                "location": "Pilani, Rajasthan", 
                "category": "Private", 
                "type": "Premier Private", 
                "fees": {"btech": "₹4.5L", "hostel": "₹65k"}, 
                "placement": {"average": "₹28 LPA", "highest": "₹60 LPA", "rate": "99%", "top_recruiters": ["Google", "Microsoft", "Amazon", "Goldman Sachs"]}, 
                "admission": {"exam": "BITSAT", "deadline": "May 20", "process": "BITSAT exam -> Counseling"}
            },
            {
                "name": "BITS Goa", 
                "aliases": ["bits goa", "goa bits"], 
                "location": "Goa", 
                "category": "Private", 
                "type": "Premier Private", 
                "fees": {"btech": "₹4.5L", "hostel": "₹65k"}, 
                "placement": {"average": "₹27 LPA", "highest": "₹58 LPA", "rate": "98%", "top_recruiters": ["Google", "Microsoft", "Amazon"]}, 
                "admission": {"exam": "BITSAT", "deadline": "May 20", "process": "BITSAT exam -> Counseling"}
            },
            {
                "name": "BITS Hyderabad", 
                "aliases": ["bits hyd", "hyderabad bits"], 
                "location": "Hyderabad, Telangana", 
                "category": "Private", 
                "type": "Premier Private", 
                "fees": {"btech": "₹4.5L", "hostel": "₹65k"}, 
                "placement": {"average": "₹26 LPA", "highest": "₹55 LPA", "rate": "97%", "top_recruiters": ["Google", "Microsoft", "Amazon"]}, 
                "admission": {"exam": "BITSAT", "deadline": "May 20", "process": "BITSAT exam -> Counseling"}
            },
            
            # ============ Top Private Universities ============
            {
                "name": "VIT Vellore", 
                "aliases": ["vit", "vellore vit", "vit vellore"], 
                "location": "Vellore, Tamil Nadu", 
                "category": "Private", 
                "type": "Top Private", 
                "fees": {"btech": "₹1.9L", "hostel": "₹50k"}, 
                "placement": {"average": "₹8.5 LPA", "highest": "₹51 LPA", "rate": "93%", "top_recruiters": ["Amazon", "Microsoft", "Deloitte", "Cognizant"]}, 
                "admission": {"exam": "VITEEE", "deadline": "April 30", "process": "VITEEE exam -> Counseling"}
            },
            {
                "name": "VIT Chennai", 
                "aliases": ["vit chennai", "chennai vit"], 
                "location": "Chennai, Tamil Nadu", 
                "category": "Private", 
                "type": "Top Private", 
                "fees": {"btech": "₹1.9L", "hostel": "₹50k"}, 
                "placement": {"average": "₹8.2 LPA", "highest": "₹49 LPA", "rate": "92%", "top_recruiters": ["Amazon", "Microsoft", "Deloitte"]}, 
                "admission": {"exam": "VITEEE", "deadline": "April 30", "process": "VITEEE exam -> Counseling"}
            },
            {
                "name": "SRM University Chennai", 
                "aliases": ["srm", "srm chennai", "srm university"], 
                "location": "Chennai, Tamil Nadu", 
                "category": "Private", 
                "type": "Top Private", 
                "fees": {"btech": "₹2.5L", "hostel": "₹65k"}, 
                "placement": {"average": "₹7.5 LPA", "highest": "₹48 LPA", "rate": "91%", "top_recruiters": ["Google", "Amazon", "Microsoft", "Dell"]}, 
                "admission": {"exam": "SRMJEEE", "deadline": "May 15", "process": "SRMJEEE exam -> Counseling"}
            },
            {
                "name": "Manipal University", 
                "aliases": ["manipal", "manipal university"], 
                "location": "Manipal, Karnataka", 
                "category": "Private", 
                "type": "Top Private", 
                "fees": {"btech": "₹3.5L", "hostel": "₹70k"}, 
                "placement": {"average": "₹9.5 LPA", "highest": "₹42 LPA", "rate": "94%", "top_recruiters": ["Google", "Microsoft", "Amazon", "Deloitte"]}, 
                "admission": {"exam": "MET", "deadline": "May 10", "process": "MET exam -> Counseling"}
            },
            {
                "name": "Thapar University", 
                "aliases": ["thapar", "thapar university"], 
                "location": "Patiala, Punjab", 
                "category": "Private", 
                "type": "Good Private", 
                "fees": {"btech": "₹3.2L", "hostel": "₹60k"}, 
                "placement": {"average": "₹10 LPA", "highest": "₹44 LPA", "rate": "95%", "top_recruiters": ["Microsoft", "Amazon", "Deloitte"]}, 
                "admission": {"exam": "JEE Main", "deadline": "May 30", "process": "JEE Main -> Counseling"}
            },
            {
                "name": "PES University Bangalore", 
                "aliases": ["pes", "pes bangalore", "pes university"], 
                "location": "Bangalore, Karnataka", 
                "category": "Private", 
                "type": "Good Private", 
                "fees": {"btech": "₹3.0L", "hostel": "₹70k"}, 
                "placement": {"average": "₹9.5 LPA", "highest": "₹43 LPA", "rate": "93%", "top_recruiters": ["Google", "Microsoft", "Amazon"]}, 
                "admission": {"exam": "PESSAT", "deadline": "May 25", "process": "PESSAT exam -> Counseling"}
            },
            
            # ============ Good Private Universities (Your Requested Ones) ============
            {
                "name": "Lovely Professional University (LPU)", 
                "aliases": ["lpu", "lovely", "lp", "lovely professional", "lovely professional university"], 
                "location": "Jalandhar, Punjab", 
                "category": "Private", 
                "type": "Good Private", 
                "fees": {"btech": "₹1.6L", "hostel": "₹50k"}, 
                "placement": {"average": "₹7.2 LPA", "highest": "₹64 LPA", "rate": "94%", "top_recruiters": ["Google", "Microsoft", "Amazon", "Deloitte"]}, 
                "admission": {"exam": "LPUNEST", "deadline": "July 15", "process": "LPUNEST exam -> Counseling"}
            },
            {
                "name": "Sharda University", 
                "aliases": ["sharda", "sharda university", "sharda univ"], 
                "location": "Greater Noida, Uttar Pradesh", 
                "category": "Private", 
                "type": "Good Private", 
                "fees": {"btech": "₹1.8L", "hostel": "₹55k"}, 
                "placement": {"average": "₹6.8 LPA", "highest": "₹42 LPA", "rate": "92%", "top_recruiters": ["Amazon", "Microsoft", "TCS", "Infosys"]}, 
                "admission": {"exam": "SUAT", "deadline": "June 30", "process": "SUAT exam -> Counseling"}
            },
            {
                "name": "Galgotias University", 
                "aliases": ["galgotias", "galgotia", "galgotias university"], 
                "location": "Greater Noida, Uttar Pradesh", 
                "category": "Private", 
                "type": "Good Private", 
                "fees": {"btech": "₹1.5L", "hostel": "₹50k"}, 
                "placement": {"average": "₹6.5 LPA", "highest": "₹38 LPA", "rate": "91%", "top_recruiters": ["Infosys", "TCS", "HCL", "Adobe"]}, 
                "admission": {"exam": "GEEE", "deadline": "July 31", "process": "GEEE exam -> Counseling"}
            },
            {
                "name": "Amity University Noida", 
                "aliases": ["amity", "amity noida", "amity university"], 
                "location": "Noida, Uttar Pradesh", 
                "category": "Private", 
                "type": "Good Private", 
                "fees": {"btech": "₹2.5L", "hostel": "₹75k"}, 
                "placement": {"average": "₹6.5 LPA", "highest": "₹35 LPA", "rate": "85%", "top_recruiters": ["Amazon", "Microsoft", "Google", "Deloitte"]}, 
                "admission": {"exam": "Amity JEE", "deadline": "June 30", "process": "Amity JEE -> Counseling"}
            },
            {
                "name": "Chandigarh University", 
                "aliases": ["chandigarh", "cu", "chandigarh university"], 
                "location": "Mohali, Punjab", 
                "category": "Private", 
                "type": "Good Private", 
                "fees": {"btech": "₹1.6L", "hostel": "₹55k"}, 
                "placement": {"average": "₹7 LPA", "highest": "₹38 LPA", "rate": "90%", "top_recruiters": ["Microsoft", "Amazon", "Google"]}, 
                "admission": {"exam": "CUCET", "deadline": "June 15", "process": "CUCET exam -> Counseling"}
            },
            {
                "name": "Chitkara University", 
                "aliases": ["chitkara", "chitkara university"], 
                "location": "Patiala, Punjab", 
                "category": "Private", 
                "type": "Good Private", 
                "fees": {"btech": "₹1.7L", "hostel": "₹52k"}, 
                "placement": {"average": "₹7 LPA", "highest": "₹40 LPA", "rate": "90%", "top_recruiters": ["Microsoft", "Amazon", "Deloitte"]}, 
                "admission": {"exam": "CUCET", "deadline": "June 15", "process": "CUCET exam -> Counseling"}
            },
            
            # ============ Central Universities ============
            {
                "name": "University of Delhi (DU)", 
                "aliases": ["du", "delhi university", "university of delhi"], 
                "location": "New Delhi", 
                "category": "Central", 
                "type": "Central University", 
                "fees": {"btech": "₹30k", "hostel": "₹20k"}, 
                "placement": {"average": "₹8 LPA", "highest": "₹35 LPA", "rate": "85%", "top_recruiters": ["Deloitte", "KPMG", "EY", "PwC"]}, 
                "admission": {"exam": "DU JAT", "deadline": "June 15", "process": "DU JAT -> Counseling"}
            },
            {
                "name": "JNU Delhi", 
                "aliases": ["jnu", "jawaharlal nehru university"], 
                "location": "New Delhi", 
                "category": "Central", 
                "type": "Central University", 
                "fees": {"btech": "₹25k", "hostel": "₹15k"}, 
                "placement": {"average": "₹9 LPA", "highest": "₹40 LPA", "rate": "88%", "top_recruiters": ["Deloitte", "KPMG", "McKinsey"]}, 
                "admission": {"exam": "JNUEE", "deadline": "May 30", "process": "JNUEE -> Counseling"}
            },
            {
                "name": "BHU Varanasi", 
                "aliases": ["bhu", "banaras hindu university"], 
                "location": "Varanasi, Uttar Pradesh", 
                "category": "Central", 
                "type": "Central University", 
                "fees": {"btech": "₹30k", "hostel": "₹16k"}, 
                "placement": {"average": "₹7.5 LPA", "highest": "₹34 LPA", "rate": "86%", "top_recruiters": ["TCS", "Infosys", "Wipro"]}, 
                "admission": {"exam": "BHU UET", "deadline": "June 5", "process": "BHU UET -> Counseling"}
            },
            {
                "name": "University of Hyderabad", 
                "aliases": ["uoh", "hyderabad university"], 
                "location": "Hyderabad, Telangana", 
                "category": "Central", 
                "type": "Central University", 
                "fees": {"btech": "₹28k", "hostel": "₹14k"}, 
                "placement": {"average": "₹8.5 LPA", "highest": "₹38 LPA", "rate": "87%", "top_recruiters": ["Deloitte", "KPMG", "Infosys"]}, 
                "admission": {"exam": "UOH Entrance", "deadline": "June 12", "process": "UOH Entrance -> Counseling"}
            },
            {
                "name": "AMU Aligarh", 
                "aliases": ["amu", "aligarh muslim university"], 
                "location": "Aligarh, Uttar Pradesh", 
                "category": "Central", 
                "type": "Central University", 
                "fees": {"btech": "₹35k", "hostel": "₹18k"}, 
                "placement": {"average": "₹7 LPA", "highest": "₹32 LPA", "rate": "84%", "top_recruiters": ["TCS", "Infosys", "Wipro"]}, 
                "admission": {"exam": "AMU Entrance", "deadline": "June 10", "process": "AMU Entrance -> Counseling"}
            },
            
            # ============ State Universities ============
            {
                "name": "Anna University Chennai", 
                "aliases": ["anna university", "anna univ"], 
                "location": "Chennai, Tamil Nadu", 
                "category": "State", 
                "type": "State University", 
                "fees": {"btech": "₹35k", "hostel": "₹18k"}, 
                "placement": {"average": "₹8 LPA", "highest": "₹38 LPA", "rate": "90%", "top_recruiters": ["TCS", "Infosys", "CTS", "Amazon"]}, 
                "admission": {"exam": "TNEA", "deadline": "May 30", "process": "TNEA Counseling"}
            },
            {
                "name": "University of Mumbai", 
                "aliases": ["mumbai university", "mu"], 
                "location": "Mumbai, Maharashtra", 
                "category": "State", 
                "type": "State University", 
                "fees": {"btech": "₹30k", "hostel": "₹15k"}, 
                "placement": {"average": "₹6.5 LPA", "highest": "₹30 LPA", "rate": "82%", "top_recruiters": ["TCS", "Infosys", "Capgemini"]}, 
                "admission": {"exam": "MU Entrance", "deadline": "June 18", "process": "MU Entrance -> Counseling"}
            },
            {
                "name": "Pune University (SPPU)", 
                "aliases": ["pune university", "sppu", "savitribai phule pune university"], 
                "location": "Pune, Maharashtra", 
                "category": "State", 
                "type": "State University", 
                "fees": {"btech": "₹26k", "hostel": "₹11k"}, 
                "placement": {"average": "₹6.8 LPA", "highest": "₹32 LPA", "rate": "83%", "top_recruiters": ["Infosys", "TCS", "IBM"]}, 
                "admission": {"exam": "MH-CET", "deadline": "June 14", "process": "MH-CET Counseling"}
            },
            {
                "name": "Bangalore University", 
                "aliases": ["bangalore univ", "bu"], 
                "location": "Bangalore, Karnataka", 
                "category": "State", 
                "type": "State University", 
                "fees": {"btech": "₹28k", "hostel": "₹12k"}, 
                "placement": {"average": "₹6 LPA", "highest": "₹28 LPA", "rate": "80%", "top_recruiters": ["Infosys", "TCS", "Wipro"]}, 
                "admission": {"exam": "BU Entrance", "deadline": "June 16", "process": "BU Entrance -> Counseling"}
            },
            {
                "name": "University of Calcutta", 
                "aliases": ["calcutta university", "cu"], 
                "location": "Kolkata, West Bengal", 
                "category": "State", 
                "type": "State University", 
                "fees": {"btech": "₹25k", "hostel": "₹12k"}, 
                "placement": {"average": "₹6 LPA", "highest": "₹28 LPA", "rate": "80%", "top_recruiters": ["TCS", "Infosys", "Wipro"]}, 
                "admission": {"exam": "CU Entrance", "deadline": "June 20", "process": "CU Entrance -> Counseling"}
            },
            
            # ============ Medical Colleges ============
            {
                "name": "AIIMS Delhi", 
                "aliases": ["aiims", "aiims delhi"], 
                "location": "New Delhi", 
                "category": "Medical", 
                "type": "Premier Medical", 
                "fees": {"mbbs": "₹1.6k", "hostel": "₹5k"}, 
                "placement": {"average": "NA", "highest": "NA", "rate": "100%", "top_recruiters": ["Hospitals", "Research Centers"]}, 
                "admission": {"exam": "NEET", "deadline": "May 30", "process": "NEET -> Counseling"}
            },
            {
                "name": "Christian Medical College Vellore", 
                "aliases": ["cmc vellore", "cmc"], 
                "location": "Vellore, Tamil Nadu", 
                "category": "Medical", 
                "type": "Top Medical", 
                "fees": {"mbbs": "₹50k", "hostel": "₹30k"}, 
                "placement": {"average": "NA", "highest": "NA", "rate": "99%", "top_recruiters": ["Hospitals", "Research Centers"]}, 
                "admission": {"exam": "NEET", "deadline": "May 30", "process": "NEET -> Counseling"}
            },
        ]
    
    def get_university_info(self, uni):
        """Get formatted information about a university"""
        info = f"""
{'='*60}
📚 **{uni.get('name', 'Unknown')}**
{'='*60}
📍 **Location:** {uni.get('location', 'N/A')}
🏷️ **Category:** {uni.get('category', 'N/A')} - {uni.get('type', 'N/A')}
⭐ **NIRF Ranking:** #{uni.get('nirf', 'Not Ranked')}

💰 **FEES STRUCTURE:**
"""
        fees = uni.get('fees', {})
        for course, fee in fees.items():
            info += f"   • {course.upper()}: {fee}\n"
        
        info += f"""
💼 **PLACEMENTS:**
   • Average Package: {uni.get('placement', {}).get('average', 'N/A')}
   • Highest Package: {uni.get('placement', {}).get('highest', 'N/A')}
   • Placement Rate: {uni.get('placement', {}).get('rate', 'N/A')}
   • Top Recruiters: {', '.join(uni.get('placement', {}).get('top_recruiters', ['Various companies'])[:5])}

📝 **ADMISSION:**
   • Entrance Exam: {uni.get('admission', {}).get('exam', 'N/A')}
   • Deadline: {uni.get('admission', {}).get('deadline', 'N/A')}
   • Process: {uni.get('admission', {}).get('process', 'Apply through official website')}
{'='*60}
"""
        return info
    
    def search_university(self, query):
        """Search for university by name, alias, location, or category"""
        query_lower = query.lower().strip()
        results = []
        
        # First, check exact aliases and names
        for uni in self.universities:
            name = uni.get('name', '').lower()
            aliases = [a.lower() for a in uni.get('aliases', [])]
            
            # Exact match on name or alias
            if query_lower == name or query_lower in aliases:
                return [uni]
        
        # Then search with scoring
        for uni in self.universities:
            score = 0
            name = uni.get('name', '').lower()
            location = uni.get('location', '').lower()
            category = uni.get('category', '').lower()
            uni_type = uni.get('type', '').lower()
            aliases = [a.lower() for a in uni.get('aliases', [])]
            
            # Check aliases
            for alias in aliases:
                if query_lower in alias or alias in query_lower:
                    score += 10
                    break
            
            # Name match
            if query_lower in name:
                score += 8
            elif any(word in name for word in query_lower.split()):
                score += 4
            
            # Location match
            if query_lower in location:
                score += 5
            
            # Category/Type match
            if query_lower in category or query_lower in uni_type:
                score += 3
            
            if score > 0:
                results.append((uni, score))
        
        # Remove duplicates and sort
        unique_results = {}
        for uni, score in results:
            uni_name = uni.get('name', '')
            if uni_name not in unique_results or score > unique_results[uni_name][1]:
                unique_results[uni_name] = (uni, score)
        
        results = list(unique_results.values())
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Fuzzy matching if no results
        if not results:
            names = [uni.get('name', '') for uni in self.universities]
            matches = get_close_matches(query, names, n=5, cutoff=0.6)
            results = [(next(uni for uni in self.universities if uni.get('name') == match), 5) for match in matches]
        
        return [r[0] for r in results[:5]]
    
    def chat(self):
        """Main chat interface"""
        print("\n" + "="*60)
        print("🎓 INDIAN UNIVERSITY SEARCH CHATBOT")
        print("="*60)
        print(f"📚 Database: {len(self.universities)} Universities")
        print("\n💡 What you can ask:")
        print("  • Search: 'Sharda University', 'LPU', 'IIT Bombay'")
        print("  • Aliases work: 'lpu', 'vit', 'bits', 'srm', 'du'")
        print("  • Location: 'Universities in Mumbai'")
        print("-"*60)
        
        while True:
            query = input("\n🔍 You: ").strip()
            
            if query.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thank you for using University Search! Goodbye!")
                break
            
            if not query:
                continue
            
            # Check for location-based search
            if 'in' in query.lower() and len(query.split()) > 2:
                words = query.split()
                try:
                    location_idx = words.index('in')
                    if location_idx + 1 < len(words):
                        location = words[location_idx + 1]
                        location_results = [u for u in self.universities if location.lower() in u.get('location', '').lower()]
                        if location_results:
                            print(f"\n📚 Universities in {location.upper()}:")
                            for i, uni in enumerate(location_results[:10], 1):
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
                    
                    print("\n💡 Type the exact name for more details!")
            else:
                print(f"\n❌ No universities found matching '{query}'")
                print("💡 Try: 'LPU', 'Sharda University', 'Galgotias', 'IIT Bombay', 'VIT'")

if __name__ == "__main__":
    bot = UniversityChatbot()
    bot.chat()