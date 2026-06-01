"""
Simple AI Chatbot using OpenAI API
This is much more reliable than local models and avoids dependency issues
"""

import os
import json
from typing import List, Dict, Optional

class SimpleAIChatbot:
    def __init__(self):
        self.api_key = None
        self.use_api = False
        
    def setup_api_key(self, api_key: str):
        """Setup OpenAI API key"""
        self.api_key = api_key
        self.use_api = True
        
    def generate_response(self, user_message: str, chat_history: List[Dict] = None, medical_context: str = None) -> str:
        """
        Generate AI response - tries API first, falls back to enhanced rule-based
        """
        if self.use_api and self.api_key:
            try:
                return self._generate_api_response(user_message, chat_history, medical_context)
            except Exception as e:
                print(f"API error: {e}")
                return self._generate_enhanced_response(user_message, medical_context)
        else:
            return self._generate_enhanced_response(user_message, medical_context)
    
    def _generate_api_response(self, user_message: str, chat_history: List[Dict], medical_context: str) -> str:
        """Generate response using OpenAI API"""
        try:
            import openai
            
            # Set API key
            openai.api_key = self.api_key
            
            # Create system prompt
            system_prompt = """You are a helpful medical AI assistant. You provide accurate, empathetic health information.

IMPORTANT RULES:
1. Always recommend seeing a doctor for serious symptoms
2. Never diagnose - only provide information and guidance
3. Be clear, concise, and easy to understand
4. Include emergency numbers for critical symptoms (India: 102/108, US: 911)
5. Keep responses under 300 words
6. Use bullet points for recommendations
7. Be empathetic and supportive

You can discuss symptoms, provide general health advice, explain medical terms, and guide users on when to seek care."""

            # Prepare messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add medical context if available
            if medical_context:
                messages.append({"role": "system", "content": f"Medical context: {medical_context}"})
            
            # Add chat history (last 3 messages)
            if chat_history:
                for msg in chat_history[-3:]:
                    role = "user" if msg.get('role') == 'user' else "assistant"
                    content = msg.get('content', '')
                    if content:
                        messages.append({"role": role, "content": content})
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Cheap and fast
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            return "Please install OpenAI package: pip install openai"
        except Exception as e:
            return f"API Error: {str(e)}"
    
    def _generate_enhanced_response(self, user_message: str, medical_context: str = None) -> str:
        """Enhanced rule-based response (much better than simple keyword matching)"""
        
        message_lower = user_message.lower()
        
        # Emergency symptoms
        emergency_keywords = [
            'chest pain', 'difficulty breathing', 'can\'t breathe', 'severe headache',
            'stroke', 'heart attack', 'unconscious', 'bleeding heavily', 'severe pain'
        ]
        
        if any(keyword in message_lower for keyword in emergency_keywords):
            return """🚨 **URGENT - SEEK IMMEDIATE MEDICAL ATTENTION**

Based on your symptoms, this could be a medical emergency.

**Call Emergency Services NOW:**
• India: 102 (Ambulance) or 108 (Emergency)
• US: 911
• UK: 999

**While waiting for help:**
• Stay calm and don't panic
• Sit or lie down in a comfortable position
• Don't drive yourself
• Have someone stay with you
• Bring any medications you're taking

**This is not a substitute for emergency medical care. Please seek immediate professional help.**"""

        # Common symptoms with intelligent responses
        symptom_responses = {
            'headache': self._headache_response(),
            'fever': self._fever_response(),
            'cough': self._cough_response(),
            'stomach': self._stomach_response(),
            'tired': self._fatigue_response(),
            'dizzy': self._dizziness_response(),
            'nausea': self._nausea_response(),
            'pain': self._pain_response()
        }
        
        # Check for symptoms
        for symptom, response_func in symptom_responses.items():
            if symptom in message_lower:
                return response_func()
        
        # General health questions
        if any(word in message_lower for word in ['what is', 'explain', 'tell me about']):
            return self._general_health_response(user_message)
        
        # Medication questions
        if any(word in message_lower for word in ['medication', 'medicine', 'drug', 'pill']):
            return self._medication_response()
        
        # Default response
        return self._default_response(user_message)
    
    def _headache_response(self) -> str:
        return """I understand you're experiencing a headache. Here's what might help:

**Common causes:**
• Tension or stress
• Dehydration
• Eye strain
• Lack of sleep
• Sinus congestion

**Immediate relief:**
• Rest in a quiet, dark room
• Apply cold compress to forehead
• Stay hydrated - drink water
• Gentle neck and shoulder massage
• Over-the-counter pain relievers (as directed)

**See a doctor if:**
• Sudden, severe headache
• Headache with fever, stiff neck, or rash
• Changes in vision or speech
• Headache after head injury
• Frequent or worsening headaches

**Emergency signs:** Sudden severe headache, confusion, or difficulty speaking
**Emergency numbers:** India 102/108, US 911

Would you like to tell me more about your headache (when it started, severity, other symptoms)?"""

    def _fever_response(self) -> str:
        return """Fever can be concerning. Here's what you should know:

**For adults - fever management:**
• Rest and stay hydrated
• Take acetaminophen or ibuprofen as directed
• Use cool compresses
• Wear light clothing
• Monitor temperature regularly

**See a doctor if:**
• Fever above 103°F (39.4°C)
• Fever lasts more than 3 days
• Severe symptoms (difficulty breathing, chest pain)
• Signs of dehydration

**Seek immediate care if:**
• Fever above 105°F (40.5°C)
• Difficulty breathing
• Severe headache with stiff neck
• Confusion or extreme drowsiness

**Emergency numbers:** India 102/108, US 911

What's your current temperature, and how long have you had the fever?"""

    def _cough_response(self) -> str:
        return """Coughs can have various causes. Here's guidance:

**Types and care:**
• **Dry cough:** Honey, warm liquids, humidifier
• **Productive cough:** Stay hydrated, don't suppress completely
• **Persistent cough:** May need medical evaluation

**Home remedies:**
• Honey (1-2 teaspoons)
• Warm salt water gargle
• Stay hydrated
• Use humidifier
• Avoid irritants (smoke, strong scents)

**See a doctor if:**
• Cough lasts more than 2-3 weeks
• Coughing up blood
• Fever with cough
• Difficulty breathing
• Chest pain

**Seek immediate care if:**
• Severe difficulty breathing
• Coughing up significant blood
• High fever with breathing problems

**Emergency numbers:** India 102/108, US 911

How long have you had the cough, and is it dry or producing mucus?"""

    def _stomach_response(self) -> str:
        return """Stomach issues can be uncomfortable. Here's what might help:

**For mild stomach upset:**
• Eat bland foods (rice, toast, bananas)
• Stay hydrated with small sips
• Avoid dairy, fatty, or spicy foods
• Rest and avoid stress
• Consider probiotics

**For nausea:**
• Ginger tea or ginger candies
• Small, frequent meals
• Avoid strong odors
• Fresh air

**See a doctor if:**
• Severe or persistent pain
• Vomiting that won't stop
• Signs of dehydration
• Blood in vomit or stool
• Fever with stomach pain

**Seek immediate care if:**
• Severe abdominal pain
• Vomiting blood
• Signs of severe dehydration
• Suspected food poisoning

**Emergency numbers:** India 102/108, US 911

Can you describe your stomach symptoms in more detail?"""

    def _fatigue_response(self) -> str:
        return """Fatigue can have many causes. Let's explore this:

**Common causes:**
• Lack of sleep
• Stress
• Poor nutrition
• Dehydration
• Lack of exercise
• Medical conditions

**Immediate steps:**
• Ensure 7-9 hours of sleep
• Stay hydrated
• Eat balanced meals
• Light exercise (even a short walk)
• Manage stress
• Limit caffeine late in day

**See a doctor if:**
• Extreme fatigue lasting weeks
• Fatigue with other symptoms (fever, weight loss)
• Difficulty performing daily activities
• Sudden onset of severe fatigue

**Consider medical evaluation for:**
• Persistent fatigue despite good sleep
• Fatigue with depression or anxiety
• Other concerning symptoms

How long have you been feeling tired, and have you noticed any other symptoms?"""

    def _dizziness_response(self) -> str:
        return """Dizziness can be concerning. Here's what to do:

**Immediate safety:**
• Sit or lie down immediately
• Avoid sudden movements
• Stay hydrated
• Don't drive

**Common causes:**
• Dehydration
• Low blood sugar
• Inner ear problems
• Blood pressure changes
• Medications

**When to see a doctor:**
• Frequent dizziness episodes
• Dizziness with hearing loss
• Severe or persistent dizziness
• Dizziness with other symptoms

**Seek immediate care if:**
• Dizziness with chest pain
• Difficulty speaking or confusion
• Severe headache with dizziness
• Loss of consciousness

**Emergency numbers:** India 102/108, US 911

Are you experiencing any other symptoms along with the dizziness?"""

    def _nausea_response(self) -> str:
        return """Nausea can be very uncomfortable. Here's how to manage it:

**Immediate relief:**
• Sip clear fluids slowly
• Try ginger (tea, candies, or fresh)
• Eat small amounts of bland food
• Get fresh air
• Rest in a comfortable position

**Helpful foods:**
• Crackers or toast
• Rice
• Bananas
• Clear broths

**Avoid:**
• Strong smells
• Fatty or spicy foods
• Large meals
• Lying flat immediately after eating

**See a doctor if:**
• Persistent vomiting
• Signs of dehydration
• Severe abdominal pain
• Blood in vomit
• High fever

**Emergency numbers:** India 102/108, US 911

How long have you been feeling nauseous, and have you been able to keep fluids down?"""

    def _pain_response(self) -> str:
        return """Pain management depends on the type and location. Here's general guidance:

**For mild to moderate pain:**
• Rest the affected area
• Apply ice for acute injuries (first 24-48 hours)
• Apply heat for muscle tension
• Over-the-counter pain relievers as directed
• Gentle stretching or movement (if appropriate)

**When to see a doctor:**
• Severe or persistent pain
• Pain that interferes with daily activities
• Pain with swelling, redness, or warmth
• Pain after an injury
• Pain with other concerning symptoms

**Seek immediate care if:**
• Severe, sudden pain
• Pain with difficulty breathing
• Pain with signs of infection
• Pain after significant trauma

**Emergency numbers:** India 102/108, US 911

Can you tell me more about your pain - where is it located and how severe is it on a scale of 1-10?"""

    def _general_health_response(self, question: str) -> str:
        return f"""I'd be happy to help explain health topics, but I want to make sure I give you accurate information.

For the question: "{question}"

**I recommend:**
• Consulting reliable medical sources (Mayo Clinic, WebMD, NHS)
• Speaking with your healthcare provider
• Getting information from medical professionals

**I can help with:**
• General symptom guidance
• When to seek medical care
• Basic health and wellness tips
• Understanding when something might be urgent

**What I can't do:**
• Provide specific medical diagnoses
• Replace professional medical advice
• Interpret test results
• Recommend specific treatments

Would you like me to help you understand when to seek care for specific symptoms, or do you have other health concerns I can guide you on?"""

    def _medication_response(self) -> str:
        return """For medication questions, safety is my top priority:

**Important reminders:**
• Always follow your doctor's instructions
• Read medication labels carefully
• Don't share prescription medications
• Keep medications in original containers
• Check expiration dates

**For medication concerns:**
• Contact your prescribing doctor
• Call your pharmacist for questions
• Use medication interaction checkers
• Keep an updated medication list

**Seek immediate help if:**
• Allergic reaction (rash, difficulty breathing)
• Severe side effects
• Accidental overdose
• Medication poisoning

**Emergency numbers:** India 102/108, US 911

**I cannot provide specific medication advice.** Please consult your healthcare provider or pharmacist for medication-related questions.

Is there a specific concern about your medications that I can help you understand when to seek professional guidance?"""

    def _default_response(self, user_message: str) -> str:
        return f"""Thank you for reaching out about your health concern.

I'm here to provide general health guidance and help you understand when to seek medical care.

**How I can help:**
• Provide information about common symptoms
• Guide you on when to see a doctor
• Offer general wellness tips
• Help you understand urgent vs. non-urgent situations
• Explain when to call emergency services

**For your specific concern:** "{user_message}"

I'd recommend:
• Being more specific about your symptoms
• Consulting with a healthcare provider for personalized advice
• Seeking immediate care if you're experiencing severe symptoms

**Emergency signs that need immediate attention:**
• Difficulty breathing
• Chest pain
• Severe bleeding
• Loss of consciousness
• Severe allergic reactions

**Emergency numbers:** India 102/108, US 911

Could you tell me more about what specific symptoms or health concerns you're experiencing? This will help me provide better guidance."""

# Global instance
chatbot = SimpleAIChatbot()

def get_ai_response(user_message: str, chat_history: List[Dict] = None, medical_context: str = None) -> str:
    """
    Main function to get AI response
    """
    return chatbot.generate_response(user_message, chat_history, medical_context)

def setup_openai_key(api_key: str):
    """Setup OpenAI API key for enhanced responses"""
    chatbot.setup_api_key(api_key)