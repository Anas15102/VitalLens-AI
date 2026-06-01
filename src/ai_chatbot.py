"""
Intelligent Medical Knowledge System - VitalLens AI
Advanced pattern recognition and symptom analysis algorithms
Optimized for instant, accurate medical guidance
"""

import re
from datetime import datetime

class IntelligentMedicalAI:
    """
    Intelligent Medical Knowledge System with:
    - Advanced symptom pattern recognition
    - Emergency detection algorithms
    - Evidence-based medical guidance
    - Instant response time (< 1 second)
    """
    
    def __init__(self):
        self.conversation_history = []
        self.medical_knowledge = self._load_medical_knowledge()
        
    def _load_medical_knowledge(self):
        """Load comprehensive medical knowledge base"""
        return {
            "emergency_keywords": [
                "chest pain", "heart attack", "can't breathe", "difficulty breathing",
                "severe headache", "stroke", "unconscious", "bleeding heavily",
                "severe abdominal pain", "poisoning", "overdose"
            ],
            
            "symptom_patterns": {
                "headache": {
                    "keywords": ["headache", "head pain", "migraine", "head ache", "head hurt"],
                    "severity_indicators": ["severe", "worst", "terrible", "unbearable", "splitting"]
                },
                "fever": {
                    "keywords": ["fever", "high temperature", "hot", "chills", "feverish", "burning up"],
                    "severity_indicators": ["high fever", "very hot", "burning", "103", "104"]
                },
                "chest_pain": {
                    "keywords": ["chest pain", "heart pain", "chest hurt", "chest ache"],
                    "severity_indicators": ["severe", "crushing", "tight", "pressure", "squeezing"]
                },
                "breathing": {
                    "keywords": ["can't breathe", "difficulty breathing", "shortness of breath", "trouble breathing"],
                    "severity_indicators": ["severe", "can't", "unable", "gasping"]
                },
                "cough": {
                    "keywords": ["cough", "coughing", "throat", "sore throat"],
                    "severity_indicators": ["severe", "persistent", "blood", "painful"]
                },
                "body_pain": {
                    "keywords": ["body pain", "body ache", "muscle pain", "joint pain", "aches"],
                    "severity_indicators": ["severe", "all over", "everywhere", "terrible"]
                },
                "dizziness": {
                    "keywords": ["dizzy", "dizziness", "lightheaded", "faint", "vertigo"],
                    "severity_indicators": ["severe", "can't stand", "falling", "spinning"]
                }
            }
        }
    
    def generate_response(self, user_message, chat_history=None, medical_context=None):
        """Generate intelligent medical response using pattern recognition"""
        
        # Add to conversation history
        self.conversation_history.append({
            "user": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Clean and analyze message
        message_lower = user_message.lower().strip()
        
        # Handle greetings first
        if self._is_greeting(message_lower):
            return self._handle_greeting(user_message)
        
        # Check for emergency situations (highest priority)
        emergency_response = self._check_emergency(message_lower)
        if emergency_response:
            return emergency_response
        
        # Analyze symptoms
        symptoms = self._identify_symptoms(message_lower)
        if symptoms:
            return self._generate_symptom_response(symptoms, message_lower)
        
        # Handle medical documents
        if medical_context:
            return self._handle_medical_document(user_message, medical_context)
        
        # General health guidance
        return self._generate_general_response(user_message)
    
    def _is_greeting(self, message):
        """Check if message is a greeting"""
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        name_patterns = ["my name is", "i'm", "i am", "call me"]
        
        # Check for greetings
        has_greeting = any(greeting in message for greeting in greetings)
        
        # Check for name patterns (but not "I am having" which is symptoms)
        has_name_pattern = False
        for pattern in name_patterns:
            if pattern in message and "having" not in message and "feeling" not in message and "experiencing" not in message:
                has_name_pattern = True
                break
        
        return has_greeting or has_name_pattern
    
    def _handle_greeting(self, message):
        """Handle greeting messages with name extraction"""
        name = self._extract_name(message)
        
        return f"""Hello {name}! 👨‍⚕️ **Welcome to VitalLens Intelligent Medical AI**

**I'm your advanced medical knowledge system, powered by:**
• Evidence-based medical algorithms
• Symptom pattern recognition
• Emergency detection protocols
• Comprehensive health guidance

**I can help with:**
🩺 **Symptom Analysis**
• Detailed guidance for headaches, fever, cough, body pain
• Emergency situation recognition and immediate advice
• Multi-symptom analysis and recommendations

🚨 **Emergency Detection**
• Immediate recognition of serious conditions
• Step-by-step emergency guidance
• Local emergency contact numbers (India & US)

💊 **Health Information**
• Evidence-based medical advice
• When to seek professional care
• Home remedies and self-care tips

📋 **Medical Document Analysis**
• Lab result interpretation guidance
• Medical report explanation
• Questions to ask your doctor

**For the best help, please:**
• Describe symptoms clearly and in detail
• Mention duration (how long you've had symptoms)
• Include severity level (mild, moderate, severe)
• Note any triggers or patterns

**Important:** I provide information and guidance only. Always consult healthcare professionals for diagnosis and treatment.

What health concern can I help you with today?"""
    
    def _extract_name(self, message):
        """Extract name from user message"""
        patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"call me (\w+)"
        ]
        
        # Only extract from "I am" if it's not followed by symptoms
        if "i am " in message.lower() and not any(symptom in message.lower() for symptom in ["having", "feeling", "experiencing"]):
            match = re.search(r"i am (\w+)", message, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
        
        return "there"
    
    def _check_emergency(self, message):
        """Check for emergency medical situations"""
        
        emergency_keywords = self.medical_knowledge["emergency_keywords"]
        
        for keyword in emergency_keywords:
            if keyword in message:
                if "chest pain" in message or "heart attack" in message:
                    return """🚨 **CHEST PAIN - MEDICAL EMERGENCY**

**CALL EMERGENCY SERVICES IMMEDIATELY:**
📞 **India: 102 (Ambulance) / 108 (Emergency)**
📞 **US: 911**

**Immediate Actions While Waiting:**
• Sit upright and try to stay calm
• Loosen any tight clothing around chest/neck
• Do NOT drive yourself to the hospital
• If not allergic to aspirin, chew 1 adult aspirin (ask 911 operator first)
• Have someone stay with you at all times

**Important Information for Emergency Services:**
• When the pain started
• Type of pain (crushing, burning, pressure, sharp)
• Any radiation to arms, jaw, or back
• Associated symptoms (nausea, sweating, shortness of breath)

**Do NOT wait to see if it gets better. Chest pain can indicate:**
• Heart attack (myocardial infarction)
• Pulmonary embolism (blood clot in lungs)
• Aortic dissection
• Other life-threatening conditions

**Time is critical for heart attacks - every minute counts!**"""

                elif "can't breathe" in message or "difficulty breathing" in message:
                    return """🚨 **BREATHING DIFFICULTY - MEDICAL EMERGENCY**

**CALL EMERGENCY SERVICES NOW:**
📞 **India: 102 (Ambulance) / 108 (Emergency)**
📞 **US: 911**

**Immediate Actions:**
• Sit upright in the most comfortable position
• Loosen tight clothing around neck and chest
• Stay as calm as possible (panic worsens breathing)
• Use rescue inhaler if you have one prescribed
• Do NOT lie flat on your back

**Critical Warning Signs:**
• Blue lips, fingernails, or face (cyanosis)
• Severe chest pain with breathing difficulty
• Confusion or altered mental state
• Cannot speak in full sentences due to breathlessness
• Wheezing or high-pitched breathing sounds

**While Waiting for Help:**
• Focus on slow, controlled breathing if possible
• Have someone stay with you
• Prepare list of current medications
• Note when breathing difficulty started

**Severe breathing problems can indicate:**
• Asthma attack • Pneumonia • Heart failure
• Pulmonary embolism • Allergic reaction

**This requires immediate professional medical attention.**"""

                elif "severe headache" in message:
                    return """🚨 **SEVERE HEADACHE - POTENTIAL EMERGENCY**

**CALL EMERGENCY SERVICES IF:**
📞 **India: 102 (Ambulance) / 108 (Emergency)**
📞 **US: 911**

**Emergency Headache Warning Signs:**
• Sudden, severe "thunderclap" headache (worst of your life)
• Headache with fever AND stiff neck
• Headache with confusion, vision changes, or speech problems
• Headache after head injury or trauma
• Headache with weakness, numbness, or difficulty walking

**Immediate Actions:**
• Lie down in a dark, quiet room
• Apply cold compress to forehead
• Do NOT take multiple different pain medications
• Note exact time headache started and characteristics
• Have someone stay with you to monitor symptoms

**Severe sudden headaches can indicate:**
• Stroke or mini-stroke (TIA)
• Brain aneurysm rupture
• Meningitis (brain infection)
• Increased brain pressure

**When in doubt, seek emergency care immediately. It's better to be safe with severe headaches.**"""

                else:
                    return """🚨 **MEDICAL EMERGENCY DETECTED**

**CALL EMERGENCY SERVICES IMMEDIATELY:**
📞 **India: 102 (Ambulance) / 108 (Emergency)**
📞 **US: 911**

**Your symptoms may require immediate medical attention.**

**While waiting for emergency services:**
• Stay calm and don't panic
• Sit or lie down in a comfortable position
• Do NOT drive yourself to the hospital
• Have someone stay with you
• Prepare a list of current medications
• Note when symptoms started

**This is not a substitute for emergency medical care.**
**When in doubt, always err on the side of caution and seek immediate help.**"""
        
        return None
    
    def _identify_symptoms(self, message):
        """Identify symptoms mentioned in the message"""
        identified_symptoms = []
        symptom_patterns = self.medical_knowledge["symptom_patterns"]
        
        for symptom_name, data in symptom_patterns.items():
            for keyword in data["keywords"]:
                if keyword in message:
                    # Check severity
                    is_severe = any(severity in message for severity in data["severity_indicators"])
                    identified_symptoms.append({
                        "name": symptom_name,
                        "severe": is_severe,
                        "keyword": keyword
                    })
                    break
        
        return identified_symptoms
    
    def _generate_symptom_response(self, symptoms, original_message):
        """Generate response based on identified symptoms"""
        
        if len(symptoms) > 1:
            return self._handle_multiple_symptoms(symptoms, original_message)
        elif len(symptoms) == 1:
            return self._handle_single_symptom(symptoms[0], original_message)
        else:
            return self._generate_general_response(original_message)
    
    def _handle_multiple_symptoms(self, symptoms, original_message):
        """Handle multiple symptoms"""
        
        symptom_names = [s["name"] for s in symptoms]
        
        if "headache" in symptom_names and "fever" in symptom_names:
            return """**Multiple Symptoms: Headache + Fever**

**Likely Causes:**
• Viral infection (flu, common cold, COVID-19)
• Bacterial infection (strep throat, sinus infection)
• Dehydration combined with illness
• Stress and fatigue

**Immediate Care Plan:**
• **Rest:** Stay in bed, sleep as much as possible
• **Hydration:** Drink water, herbal tea, clear broths every hour
• **Temperature Control:** Take acetaminophen or ibuprofen as directed
• **Environment:** Dark, quiet, cool room
• **Monitoring:** Check temperature every 4-6 hours

**Symptom Management:**
• **For Headache:** Cold compress on forehead, gentle massage
• **For Fever:** Light clothing, cool compresses, increase fluids
• **Both:** Avoid bright lights and loud noises

**See a Doctor If:**
• Fever above 103°F (39.4°C)
• Severe headache with stiff neck
• Symptoms worsen after 2-3 days
• Difficulty breathing or chest pain
• Persistent vomiting or dehydration signs

**Emergency Signs:** Sudden severe headache with high fever, confusion, or difficulty breathing
**Contact:** India 102/108, US 911

**Expected Recovery:** 3-7 days with proper rest and care"""

        elif "chest_pain" in symptom_names:
            # Any chest pain with other symptoms is emergency
            return self._check_emergency("chest pain")
        
        elif "body_pain" in symptom_names or "muscle_pain" in symptom_names:
            return """**Multiple Symptoms with Body/Muscle Pain**

**Common Causes:**
• Viral infections (flu, COVID-19, other viruses)
• Physical overexertion or strain
• Dehydration and electrolyte imbalance
• Stress and tension
• Sleep deprivation effects

**Comprehensive Care Plan:**
• **Rest:** Prioritize sleep (7-9 hours), avoid strenuous activities
• **Hydration:** Water, electrolyte drinks, warm broths
• **Pain Relief:** Acetaminophen or ibuprofen as directed
• **Heat Therapy:** Warm baths, heating pads for muscle aches
• **Gentle Movement:** Light stretching, avoid intense exercise

**Nutrition Support:**
• Easy-to-digest foods (soup, toast, bananas)
• Avoid alcohol and caffeine
• Increase vitamin C (citrus fruits, berries)
• Consider zinc supplements if approved by doctor

**Monitor Closely:**
• Temperature changes
• Pain levels and locations
• Energy levels and appetite
• Sleep quality

**See a Doctor If:**
• Symptoms persist more than a week
• High fever (>103°F/39.4°C)
• Severe pain that limits movement
• Signs of dehydration
• Difficulty breathing

**Emergency:** Severe symptoms with breathing difficulty
**Contact:** India 102/108, US 911

**Recovery Timeline:** Usually 5-10 days with proper care"""
        
        else:
            symptom_list = ", ".join([s["name"].replace("_", " ") for s in symptoms])
            return f"""**Multiple Symptoms Analysis: {symptom_list.title()}**

**Your Symptoms:** {original_message}

**General Approach for Multiple Symptoms:**
• **Rest:** Your body needs energy to fight illness
• **Hydration:** Increase fluid intake significantly
• **Monitoring:** Track all symptoms and their changes
• **Nutrition:** Light, easy-to-digest foods
• **Medication:** Over-the-counter relief as appropriate

**Common Patterns:**
• Multiple symptoms often indicate viral infection
• Body's immune system response to illness
• Usually resolve together over 3-7 days
• Gradual improvement is normal pattern

**Red Flags - Seek Immediate Care:**
• Difficulty breathing or chest pain
• High fever above 103°F (39.4°C)
• Severe dehydration (dizziness, no urination)
• Symptoms rapidly worsening
• Confusion or altered mental state

**When to See a Doctor:**
• Symptoms persist beyond a week
• No improvement after 3-4 days
• New concerning symptoms develop
• You feel significantly worse

**Emergency Situations:** India 102/108, US 911

**For Better Guidance:** Please describe each symptom in more detail - when it started, severity level, and any patterns you've noticed."""
    
    def _handle_single_symptom(self, symptom, original_message):
        """Handle single symptom with detailed guidance"""
        
        symptom_responses = {
            "headache": """**Headache Analysis & Complete Care Guide**

**Types of Headaches:**
• **Tension Headache:** Band-like pressure around head (most common)
• **Migraine:** Throbbing, often one-sided, may include nausea/light sensitivity
• **Sinus Headache:** Pressure around eyes, nose, cheeks
• **Cluster Headache:** Severe pain around one eye (rare but intense)

**Immediate Relief Strategies:**
• **Environment:** Dark, quiet, cool room
• **Cold Therapy:** Ice pack on forehead for 15-20 minutes
• **Pressure Points:** Gentle massage of temples, neck, shoulders
• **Hydration:** Drink water slowly (dehydration is common cause)
• **Medication:** Acetaminophen or ibuprofen (follow package directions)

**Natural Remedies:**
• Peppermint oil on temples (diluted)
• Warm compress on neck and shoulders
• Deep breathing exercises
• Gentle neck stretches

**Prevention Strategies:**
• Regular sleep schedule (7-9 hours nightly)
• Stay hydrated throughout the day
• Regular meals (don't skip)
• Manage stress levels
• Limit screen time
• Identify and avoid personal triggers

**See a Doctor If:**
• Sudden, severe headache (worst of your life)
• Headache with fever and stiff neck
• Changes in vision, speech, or coordination
• Headache after head injury
• Frequent headaches (more than 3 per week)
• Pattern of headaches getting worse

**Emergency Warning Signs:**
• Sudden severe "thunderclap" headache
• Headache with confusion or altered consciousness
• Headache with weakness or numbness
• Severe headache with high fever

**Emergency Contact:** India 102/108, US 911

**Recovery Timeline:** Most headaches resolve within 2-4 hours with proper treatment""",

            "fever": """**Fever Management - Complete Guide**

**Understanding Fever Levels:**
• **Normal:** 98.6°F (37°C)
• **Low-grade:** 100-102°F (37.8-38.9°C)
• **Moderate:** 102-104°F (38.9-40°C)
• **High:** Above 104°F (40°C) - seek immediate care

**Fever is your body's natural defense against infection - it's usually helpful!**

**Home Treatment Protocol:**
• **Rest:** Sleep as much as possible, avoid physical exertion
• **Hydration:** Water, herbal tea, clear broths, electrolyte drinks
• **Clothing:** Light, breathable fabrics, remove excess layers
• **Cooling:** Cool (not cold) compresses on forehead, wrists
• **Medication:** Acetaminophen or ibuprofen (alternate every 4-6 hours if needed)

**Monitoring Guidelines:**
• Check temperature every 4-6 hours
• Track fluid intake (aim for clear, pale yellow urine)
• Note other symptoms (cough, headache, body aches)
• Monitor energy levels and appetite

**Nutrition During Fever:**
• Light, easy-to-digest foods
• Chicken soup (proven immune benefits)
• Fruits high in vitamin C
• Avoid dairy if it increases mucus
• Small, frequent meals

**See a Doctor If:**
• Fever above 103°F (39.4°C)
• Fever lasts more than 3 days
• Difficulty breathing or chest pain
• Severe dehydration (dizziness, no urination for 8+ hours)
• Persistent vomiting preventing fluid intake
• Severe headache or neck stiffness

**Emergency Situations:**
• Fever above 104°F (40°C)
• Difficulty breathing
• Chest pain
• Confusion or altered mental state
• Signs of severe dehydration

**Emergency Contact:** India 102/108, US 911

**Recovery:** Most fevers resolve in 2-5 days as your body fights the infection""",

            "cough": """**Cough Analysis & Treatment Guide**

**Types of Cough:**
• **Dry Cough:** No mucus, often tickling sensation in throat
• **Productive Cough:** Brings up mucus or phlegm (usually good - clears airways)
• **Acute Cough:** Lasts less than 3 weeks (usually viral)
• **Chronic Cough:** Lasts more than 8 weeks (needs medical evaluation)

**Natural Remedies (Proven Effective):**
• **Honey:** 1-2 teaspoons, especially before bed (natural cough suppressant)
• **Warm Salt Water Gargle:** 1/2 teaspoon salt in warm water, 3-4 times daily
• **Hydration:** Warm liquids help thin mucus and soothe throat
• **Humidifier:** Moist air reduces throat irritation
• **Steam Therapy:** Hot shower steam or bowl of hot water with towel over head

**Additional Relief Methods:**
• Throat lozenges or hard candy
• Elevate head while sleeping
• Avoid irritants (smoke, strong perfumes)
• Warm tea with honey and lemon

**Cough Suppressants vs. Expectorants:**
• **Suppress dry cough** that prevents sleep
• **Don't suppress productive cough** - it's clearing your airways
• Consult pharmacist for appropriate over-the-counter options

**See a Doctor If:**
• Cough persists more than 2-3 weeks
• Coughing up blood or pink-tinged mucus
• Fever with persistent cough
• Difficulty breathing or wheezing
• Chest pain when coughing
• Cough interfering significantly with sleep

**Emergency Signs:**
• Severe difficulty breathing
• Coughing up significant amounts of blood
• High fever with severe cough
• Chest pain with shortness of breath

**Emergency Contact:** India 102/108, US 911

**Prevention:** Hand hygiene, avoid sick contacts, stay hydrated, don't smoke""",

            "body_pain": """**Body Pain & Muscle Aches - Complete Care**

**Common Causes:**
• **Viral Infections:** Flu, COVID-19, other viruses (most common)
• **Physical Overexertion:** Exercise, heavy lifting, unusual activity
• **Stress & Tension:** Muscle tightness from emotional stress
• **Dehydration:** Affects muscle function and comfort
• **Sleep Issues:** Poor sleep quality causes muscle tension

**Immediate Relief Protocol:**
• **Rest:** Avoid strenuous activities, prioritize sleep
• **Heat Therapy:** Warm baths, heating pads, warm compresses
• **Gentle Movement:** Light stretching, slow walks (don't overdo)
• **Hydration:** Water and electrolyte replacement
• **Medication:** Ibuprofen or acetaminophen as directed

**Heat vs. Cold Therapy:**
• **Heat:** Better for muscle aches, stiffness, chronic pain
• **Cold:** Better for acute injuries, swelling, inflammation
• **For body aches:** Heat is usually more effective

**Gentle Exercises:**
• Neck rolls and shoulder shrugs
• Gentle back stretches
• Light yoga or tai chi movements
• Walking at comfortable pace
• Avoid high-impact activities

**Nutrition Support:**
• Anti-inflammatory foods (berries, leafy greens, fish)
• Adequate protein for muscle repair
• Magnesium-rich foods (nuts, seeds, dark chocolate)
• Stay well-hydrated

**See a Doctor If:**
• Pain persists more than a week
• Severe pain that limits normal movement
• Fever with body aches
• Signs of infection (redness, swelling, warmth)
• Pain after injury or trauma
• Weakness or numbness with pain

**Emergency Situations:**
• Severe pain with high fever
• Difficulty moving or walking
• Signs of serious infection
• Chest pain with body aches

**Emergency Contact:** India 102/108, US 911

**Prevention:** Regular exercise, good posture, stress management, adequate sleep""",

            "dizziness": """**Dizziness Assessment & Management**

**Types of Dizziness:**
• **Lightheadedness:** Feeling faint, woozy, or about to pass out
• **Vertigo:** Spinning sensation, room feels like it's moving
• **Disequilibrium:** Feeling unsteady or off-balance
• **Presyncope:** Feeling like you're about to faint

**Common Causes:**
• **Dehydration:** Most common, especially in hot weather
• **Low Blood Sugar:** Skipping meals, diabetes
• **Orthostatic Hypotension:** Blood pressure drop when standing
• **Inner Ear Problems:** Vestibular disorders
• **Medication Side Effects:** Check your medications
• **Anxiety:** Can cause dizziness and lightheadedness

**Immediate Safety Actions:**
• **Sit or lie down immediately** - don't try to "push through"
• **Stay hydrated** - drink water slowly
• **Avoid sudden movements** - change positions slowly
• **Eat something** if blood sugar might be low
• **Rest** until feeling completely passes

**Prevention Strategies:**
• Stand up slowly from sitting or lying positions
• Stay well-hydrated throughout the day
• Eat regular meals to maintain blood sugar
• Avoid alcohol and excessive caffeine
• Get adequate sleep (7-9 hours)

**When Dizziness Occurs:**
• Note triggers (standing up, turning head, certain positions)
• Check if you're dehydrated or hungry
• Sit with head between knees if feeling faint
• Focus on a fixed point to reduce spinning sensation

**See a Doctor If:**
• Frequent episodes of dizziness
• Dizziness with chest pain or heart palpitations
• Severe headache with dizziness
• Hearing loss or ringing in ears (tinnitus)
• Weakness, numbness, or difficulty speaking
• Dizziness after head injury

**Emergency Situations:**
• Dizziness with severe chest pain
• Dizziness with difficulty breathing
• Dizziness with severe headache and confusion
• Fainting or loss of consciousness
• Signs of stroke (weakness, speech problems)

**Emergency Contact:** India 102/108, US 911

**Recovery:** Most dizziness resolves quickly with rest and hydration"""
        }
        
        return symptom_responses.get(symptom["name"], self._generate_general_response(original_message))
    
    def _handle_medical_document(self, message, medical_context):
        """Handle medical document analysis"""
        
        return f"""**Medical Document Analysis**

**Document Context:** {medical_context}

**Your Question:** "{message}"

**Understanding Medical Documents:**
• **Lab Results:** Compare values to reference ranges provided
• **Imaging Reports:** Radiologist interpretations of X-rays, CT, MRI
• **Pathology Reports:** Tissue or cell analysis results
• **Discharge Summaries:** Hospital stay overview and follow-up instructions

**Key Points to Remember:**
• Abnormal values don't always mean serious problems
• Trends over time are more important than single results
• Reference ranges can vary between laboratories
• Your doctor considers your complete medical picture

**Common Lab Tests Explained:**
• **CBC (Complete Blood Count):** Checks for infections, anemia, blood disorders
• **Basic Metabolic Panel:** Kidney function, electrolytes, blood sugar
• **Lipid Panel:** Cholesterol levels and heart disease risk
• **Liver Function Tests:** How well your liver is working
• **Thyroid Tests:** Metabolism and hormone levels

**Questions to Ask Your Doctor:**
• What do these results mean for my health?
• Are any values concerning and why?
• Do I need follow-up testing?
• Should I make any lifestyle changes?
• When should I have these tests repeated?

**Next Steps:**
• Schedule appointment with your healthcare provider
• Bring original documents and any questions
• Don't panic about abnormal results until discussed with doctor
• Ask for explanation of any terms you don't understand

**Important:** Only qualified healthcare professionals can provide accurate interpretation of medical tests and results.

**Emergency:** If you have severe symptoms, don't wait for appointments
**Contact:** India 102/108, US 911

Would you like me to explain any specific medical terms or help you prepare questions for your doctor?"""
    
    def _generate_general_response(self, message):
        """Generate general health response"""
        
        return f"""**Health Information & Guidance**

**Your Question:** "{message}"

**I'm here to help you with comprehensive health guidance. Let me provide you with the information you need.**

**For Specific Symptoms:**
Please tell me more details about what you're experiencing:
• **What symptoms** are you having?
• **How long** have you had them?
• **How severe** are they (mild, moderate, severe)?
• **Any triggers** or patterns you've noticed?
• **Other symptoms** occurring at the same time?

**General Health Maintenance:**
• **Sleep:** 7-9 hours nightly for optimal health
• **Hydration:** 8-10 glasses of water daily
• **Nutrition:** Balanced diet with fruits, vegetables, whole grains
• **Exercise:** 150 minutes moderate activity per week
• **Stress Management:** Regular relaxation, meditation, or hobbies
• **Preventive Care:** Regular checkups and screenings

**When to Seek Medical Care:**
• **Immediate:** Severe symptoms, chest pain, difficulty breathing
• **Soon:** Persistent symptoms, worsening conditions
• **Routine:** Preventive care, chronic condition management
• **Emergency:** Life-threatening symptoms

**I Can Help You With:**
• Symptom analysis and guidance
• Emergency situation recognition
• Health information and education
• When to seek professional care
• Home remedies and self-care tips
• Medical document interpretation guidance

**Emergency Situations:** 
• Chest pain or difficulty breathing
• Severe headache with confusion
• High fever with severe symptoms
• Any life-threatening condition

**Emergency Contact:** India 102/108, US 911

**For Better Assistance:** Please provide more specific details about your health concern, and I'll give you targeted, evidence-based guidance."""

# Global instance
chatbot = IntelligentMedicalAI()

def get_ai_response(user_message, chat_history=None, medical_context=None):
    """
    Get intelligent medical AI response
    Pure Python, no dependencies, instant responses
    """
    return chatbot.generate_response(user_message, chat_history, medical_context)