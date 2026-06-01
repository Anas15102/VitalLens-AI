"""
VitalLens API Server
Flask API to connect web interface to AI models
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import numpy as np
from PIL import Image
import io
import base64
import json
from pathlib import Path

# Add src to path for model imports
sys.path.append('src')

app = Flask(__name__)
CORS(app)  # Enable CORS for web interface

def extract_pdf_text(base64_content):
    """Extract text from PDF base64 content"""
    try:
        import PyPDF2
        
        # Remove data URL prefix if present
        if ',' in base64_content:
            base64_content = base64_content.split(',')[1]
        
        # Decode base64
        pdf_data = base64.b64decode(base64_content)
        
        # Create PDF reader
        pdf_file = io.BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except ImportError:
        print("PyPDF2 not installed. Install with: pip install PyPDF2")
        return None
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

# Serve static files (web interface)
@app.route('/')
def serve_index():
    return send_from_directory('web', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('web', filename)

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Check if API and models are working"""
    try:
        # Try to import models
        from prediction.image_models import brain_tumor_model, pneumonia_model
        
        status = {
            "status": "healthy",
            "brain_model": brain_tumor_model is not None,
            "pneumonia_model": pneumonia_model is not None,
            "message": "VitalLens API is running"
        }
        
        return jsonify(status)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error loading models: {str(e)}"
        }), 500

# Brain tumor analysis endpoint
@app.route('/api/analyze/brain', methods=['POST'])
def analyze_brain():
    """Analyze brain MRI scan for tumor detection"""
    try:
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Import prediction functions
        from prediction.image_models import predict_brain_tumor, get_brain_tumor_probabilities
        
        # Convert uploaded file to PIL Image
        image = Image.open(file.stream)
        
        # Get predictions
        probability, prediction = predict_brain_tumor(image)
        all_probabilities = get_brain_tumor_probabilities(image)
        
        # Determine result type for UI styling
        result_type = "success" if prediction == "No Tumor" else "warning"
        
        # Generate recommendations based on result
        recommendations = []
        if prediction == "No Tumor":
            recommendations = [
                "Continue regular checkups as recommended by your doctor",
                "Maintain a healthy lifestyle for brain health", 
                "Consult your doctor if you have any symptoms"
            ]
        else:
            recommendations = [
                "Schedule an appointment with a neurologist immediately",
                "Bring this analysis to show your doctor",
                "Don't panic - early detection helps with treatment",
                "Consider a second opinion if recommended",
                "Contact emergency services if severe symptoms (India: 102/108, US: 911)"
            ]
        
        response = {
            "success": True,
            "prediction": prediction,
            "confidence": round(probability, 1),
            "result_type": result_type,
            "all_probabilities": all_probabilities,
            "recommendations": recommendations,
            "model_info": {
                "accuracy": "95.82%",
                "architecture": "EfficientNet-B0",
                "input_size": "224x224"
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }), 500

# Chest X-ray analysis endpoint  
@app.route('/api/analyze/chest', methods=['POST'])
def analyze_chest():
    """Analyze chest X-ray for pneumonia/COVID detection"""
    try:
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Import prediction functions
        from prediction.image_models import predict_pneumonia, get_pneumonia_probabilities
        
        # Convert uploaded file to PIL Image
        image = Image.open(file.stream)
        
        # Get predictions
        probability, prediction = predict_pneumonia(image)
        all_probabilities = get_pneumonia_probabilities(image)
        
        # Determine result type and urgency for UI styling
        if prediction == "COVID-19":
            result_type = "emergency"
            urgency = "critical"
        elif prediction in ["Lung Opacity", "Viral Pneumonia"]:
            result_type = "warning" 
            urgency = "high"
        else:
            result_type = "success"
            urgency = "low"
        
        # Generate recommendations based on result
        recommendations = []
        if prediction == "COVID-19":
            recommendations = [
                "🚨 Isolate immediately - Stay away from others",
                "Contact healthcare provider right away", 
                "Monitor symptoms closely - fever, breathing difficulty",
                "Call emergency services if you have trouble breathing (India: 102/108, US: 911)",
                "Inform close contacts about potential exposure"
            ]
        elif prediction in ["Lung Opacity", "Viral Pneumonia"]:
            recommendations = [
                "Schedule medical consultation within 24-48 hours",
                "Monitor breathing and symptoms closely",
                "Rest and stay hydrated",
                "Avoid strenuous activities", 
                "Seek emergency care if breathing worsens (India: 102/108, US: 911)"
            ]
        else:
            recommendations = [
                "Normal chest X-ray - no signs of pneumonia or COVID-19",
                "Continue healthy habits - exercise and good nutrition",
                "Regular health checkups as recommended",
                "Consult your doctor if you develop respiratory symptoms"
            ]
        
        response = {
            "success": True,
            "prediction": prediction,
            "confidence": round(probability, 1),
            "result_type": result_type,
            "urgency": urgency,
            "all_probabilities": all_probabilities,
            "recommendations": recommendations,
            "model_info": {
                "accuracy": "93.76%", 
                "architecture": "ResNet18",
                "input_size": "224x224"
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }), 500

# AI Chat endpoint - NOW WITH REAL AI! 🤖
@app.route('/api/chat', methods=['POST'])
def ai_chat():
    """Handle AI chat conversations using local Phi-2 model"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        message = data.get('message', '')
        files = data.get('files', [])  # Base64 encoded files
        chat_history = data.get('history', [])
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Import Intelligent Medical AI
        try:
            from ai_chatbot import get_ai_response
            use_ai = True
            print("🤖 Using Intelligent Medical Knowledge System")
        except ImportError:
            print("⚠️ Medical AI not available, using fallback")
            use_ai = False
        
        # Prepare medical context from files
        medical_context = ""
        if files:
            medical_context = f"Patient uploaded {len(files)} medical document(s).\n\n"
            for file_data in files:
                filename = file_data.get('name', 'document')
                file_type = file_data.get('type', '')
                file_content = file_data.get('content', '')
                
                medical_context += f"**Document: {filename}**\n"
                
                # Extract text from PDF if available
                if file_type == 'application/pdf' and file_content:
                    try:
                        pdf_text = extract_pdf_text(file_content)
                        if pdf_text:
                            medical_context += f"Content: {pdf_text[:500]}...\n\n"  # First 500 chars
                        else:
                            medical_context += "PDF document (text extraction not available)\n\n"
                    except Exception as e:
                        print(f"Error extracting PDF text: {e}")
                        medical_context += "PDF document uploaded\n\n"
                else:
                    medical_context += f"File type: {file_type}\n\n"
        
        # Generate AI response using LOCAL MODEL
        if use_ai:
            ai_response = get_ai_response(
                user_message=message,
                chat_history=chat_history,
                medical_context=medical_context if medical_context else None
            )
        else:
            # Fallback response if AI not available
            ai_response = f"""I understand you're asking about: "{message}"

To enable full AI responses, please run:
```
python setup_local_ai.py
```

This will download a lightweight AI model (~2.7GB) that runs locally on your computer.

In the meantime, I can help you with:
- 🧠 Brain MRI analysis
- 🫁 Chest X-ray analysis  
- 📊 Basic health information

What would you like to do?"""
        
        response = {
            "success": True,
            "message": ai_response,
            "ai_powered": use_ai,
            "timestamp": "now"
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Chat failed: {str(e)}"
        }), 500

# Speech recognition endpoint (server-side for cross-browser support)
@app.route('/api/speech/recognize', methods=['POST'])
def speech_recognize():
    """Server-side speech recognition for cross-browser support"""
    try:
        import speech_recognition as sr
        import io
        import base64
        from pydub import AudioSegment
        import tempfile
        import os
        
        # Get audio data from request
        data = request.get_json()
        if not data or 'audio' not in data:
            return jsonify({"error": "No audio data provided"}), 400
        
        # Decode base64 audio
        audio_base64 = data['audio']
        language = data.get('language', 'en-US')
        
        # Remove data URL prefix if present
        if ',' in audio_base64:
            audio_base64 = audio_base64.split(',')[1]
        
        audio_data = base64.b64decode(audio_base64)
        
        print(f"Received audio data: {len(audio_data)} bytes")
        
        # Create temporary files for conversion
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as webm_file:
            webm_file.write(audio_data)
            webm_path = webm_file.name
        
        wav_path = webm_path.replace('.webm', '.wav')
        
        try:
            # Convert WebM to WAV using pydub
            print(f"Converting audio from WebM to WAV...")
            audio = AudioSegment.from_file(webm_path, format="webm")
            
            # Export as WAV with proper settings for speech recognition
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(wav_path, format="wav")
            
            print(f"Audio converted successfully")
            
            # Create recognizer
            recognizer = sr.Recognizer()
            
            # Load the WAV file
            with sr.AudioFile(wav_path) as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)
            
            # Recognize speech using Google Speech Recognition
            try:
                # Map language codes
                lang_map = {
                    'en-US': 'en-US',
                    'hi-IN': 'hi-IN'
                }
                recognition_lang = lang_map.get(language, 'en-US')
                
                print(f"Recognizing speech in language: {recognition_lang}")
                text = recognizer.recognize_google(audio_data, language=recognition_lang)
                
                print(f"Recognition successful: {text}")
                
                return jsonify({
                    "success": True,
                    "text": text,
                    "language": language
                })
                
            except sr.UnknownValueError:
                print("Could not understand audio")
                return jsonify({
                    "success": False,
                    "error": "Could not understand audio. Please speak clearly and try again."
                }), 400
                
            except sr.RequestError as e:
                print(f"Speech recognition service error: {e}")
                return jsonify({
                    "success": False,
                    "error": f"Speech recognition service error: {str(e)}"
                }), 500
        
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(webm_path):
                    os.unlink(webm_path)
                if os.path.exists(wav_path):
                    os.unlink(wav_path)
            except Exception as e:
                print(f"Error cleaning up temp files: {e}")
        
    except Exception as e:
        print(f"Speech recognition error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"Speech recognition failed: {str(e)}"
        }), 500

# Model status endpoint
@app.route('/api/models/status')
def model_status():
    """Get detailed model status information"""
    try:
        from prediction.image_models import brain_tumor_model, pneumonia_model
        from prediction.image_models import brain_tumor_classes, pneumonia_classes
        
        status = {
            "brain_model": {
                "loaded": brain_tumor_model is not None,
                "classes": list(brain_tumor_classes.values()) if brain_tumor_model else [],
                "accuracy": "95.82%",
                "architecture": "EfficientNet-B0"
            },
            "pneumonia_model": {
                "loaded": pneumonia_model is not None,
                "classes": list(pneumonia_classes.values()) if pneumonia_model else [],
                "accuracy": "93.76%", 
                "architecture": "ResNet18"
            },
            "system_info": {
                "python_version": sys.version.split()[0],
                "api_status": "running"
            }
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            "error": f"Status check failed: {str(e)}"
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting VitalLens API Server...")
    print("📊 Web Interface: http://localhost:5001")
    print("🔗 API Endpoints:")
    print("   - Health Check: http://localhost:5001/api/health")
    print("   - Brain Analysis: POST http://localhost:5001/api/analyze/brain")
    print("   - Chest Analysis: POST http://localhost:5001/api/analyze/chest") 
    print("   - AI Chat: POST http://localhost:5001/api/chat")
    print("   - Model Status: http://localhost:5001/api/models/status")
    
    app.run(host='0.0.0.0', port=5001, debug=True)