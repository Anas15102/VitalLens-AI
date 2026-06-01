# VitalLens 🏥 - AI Health Risk Assessment Platform

**Unified Multi-Modal Disease Prediction Platform with Modern Web Interface**

VitalLens is an AI-powered healthcare decision-support platform that predicts the risk of multiple diseases by analyzing **medical images** using state-of-the-art deep learning models. Now featuring both a modern web interface and Streamlit app with real AI model integration.

---

## 🚀 Quick Start

### Option 1: Web Interface with Real AI Models (Recommended)
```bash
# 1. Install API requirements
pip install -r api_requirements.txt

# 2. Start VitalLens with web interface
python start_vitallens.py
```

The web interface will automatically open at `http://localhost:5000` with full AI model integration!

### Option 2: Streamlit Interface
```bash
# 1. Install requirements
pip install -r requirements.txt

# 2. Run Streamlit app
streamlit run app.py
```

---

## 🌟 Features

### 🧠 **Brain Tumor Detection**
- **Accuracy**: 95.82% using EfficientNet-B0
- **Classes**: No Tumor, Glioma, Meningioma, Pituitary Tumor
- **Input**: MRI scans (JPG, PNG)
- **Output**: Confidence scores, detailed analysis, medical recommendations

### 🫁 **Chest X-Ray Analysis** 
- **Accuracy**: 93.76% using ResNet18
- **Classes**: Normal, COVID-19, Pneumonia, Lung Opacity
- **Input**: Chest X-rays (JPG, PNG)
- **Output**: Disease detection, emergency alerts, treatment guidance

### 🤖 **AI Health Assistant**
- **Document Analysis**: Upload lab reports, prescriptions, medical images
- **Symptom Assessment**: Describe symptoms for personalized recommendations
- **Smart Extraction**: AI automatically extracts patient info from documents
- **Doctor Recommendations**: Find nearby specialists based on analysis
- **Emergency Detection**: Automatic alerts for critical conditions

### 🌐 **Modern Web Interface**
- **Dark Theme**: Easy on the eyes with professional medical styling
- **Multi-Page**: Separate pages for each feature
- **Responsive**: Works on desktop, tablet, and mobile
- **Real-Time**: Live AI analysis with progress indicators
- **3D Animations**: Smooth hover effects and transitions

---

## 📁 Project Structure

```
VitalLens-Clean/
├── 🌐 Web Interface
│   ├── web/
│   │   ├── index.html          # Homepage
│   │   ├── brain-analysis.html # Brain scan analysis
│   │   ├── chest-analysis.html # Chest X-ray analysis  
│   │   ├── ai-chat.html        # AI health assistant
│   │   ├── about.html          # About page
│   │   ├── styles.css          # Dark theme styling
│   │   └── script.js           # API integration
│   └── api_server.py           # Flask API backend
│
├── 🧠 AI Models
│   ├── models/
│   │   └── image/
│   │       ├── brain_tumor_cnn.pth    # Brain tumor model
│   │       └── pneumonia_cnn.pth      # Pneumonia model
│   └── src/
│       └── prediction/
│           └── image_models.py        # Model inference
│
├── 📱 Streamlit App
│   ├── app.py                  # Main Streamlit application
│   └── requirements.txt        # Streamlit dependencies
│
└── 🚀 Startup & Config
    ├── start_vitallens.py      # Easy startup script
    ├── api_requirements.txt    # API dependencies
    └── README.md              # This file
```

---

## 🔗 API Endpoints

The Flask API provides these endpoints for the web interface:

### Health & Status
- `GET /api/health` - Check API and model status
- `GET /api/models/status` - Detailed model information

### AI Analysis  
- `POST /api/analyze/brain` - Brain tumor detection
- `POST /api/analyze/chest` - Chest X-ray analysis
- `POST /api/chat` - AI health assistant chat

### Web Interface
- `GET /` - Serve web interface
- `GET /<filename>` - Serve static files (CSS, JS, images)

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- 4GB+ RAM (for AI models)
- Modern web browser

### Step-by-Step Installation

1. **Clone or download the project**
   ```bash
   cd VitalLens-Clean
   ```

2. **Install API dependencies**
   ```bash
   pip install -r api_requirements.txt
   ```

3. **Verify model files exist**
   ```
   models/image/brain_tumor_cnn.pth
   models/image/pneumonia_cnn.pth
   ```

4. **Start VitalLens**
   ```bash
   python start_vitallens.py
   ```

5. **Open your browser**
   - Automatically opens to `http://localhost:5000`
   - Or manually navigate to the URL

---

## 🎯 Usage Guide

### Web Interface Usage

1. **Homepage**: Overview of all features with quick access buttons
2. **Brain Analysis**: 
   - Upload MRI scan → Get instant AI analysis → View recommendations
3. **Chest Analysis**: 
   - Upload X-ray → Detect pneumonia/COVID → Emergency alerts if needed
4. **AI Chat**: 
   - Type symptoms OR upload medical documents → Get comprehensive analysis

### API Integration

The web interface automatically connects to the Flask API. You can also use the API directly:

```python
import requests

# Brain analysis
with open('brain_scan.jpg', 'rb') as f:
    response = requests.post('http://localhost:5000/api/analyze/brain', 
                           files={'image': f})
    result = response.json()

# Chat with AI
response = requests.post('http://localhost:5000/api/chat',
                        json={'message': 'I have a headache for 3 days'})
ai_response = response.json()
```

---

## 📊 Model Performance

| Model | Accuracy | Architecture | Classes |
|-------|----------|--------------|---------|
| Brain Tumor | 95.82% | EfficientNet-B0 | No Tumor, Glioma, Meningioma, Pituitary |
| Pneumonia/COVID | 93.76% | ResNet18 | Normal, COVID-19, Pneumonia, Lung Opacity |

---

## 🔧 Troubleshooting

### Common Issues

**"Port 5000 already in use"**
```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9
# Or use different port in api_server.py
```

**"Models not loading"**
- Verify model files exist in `models/image/`
- Check PyTorch installation: `pip install torch torchvision`
- Ensure sufficient RAM (4GB+)

**"API connection failed"**
- Check if Flask server is running
- Verify no firewall blocking port 5000
- Try refreshing the web page

**"Module not found errors"**
```bash
# Install missing dependencies
pip install -r api_requirements.txt
# Or for Streamlit
pip install -r requirements.txt
```

---

## 🏥 Medical Disclaimer

**⚠️ IMPORTANT**: VitalLens is an AI-powered health information tool designed to assist and educate. It is **NOT** intended to replace professional medical advice, diagnosis, or treatment.

### What VitalLens Does:
✅ Provides AI-powered analysis of medical images  
✅ Offers health information and educational content  
✅ Suggests when to seek professional medical care  
✅ Helps understand medical terminology  

### What VitalLens Cannot Do:
❌ Replace professional medical diagnosis  
❌ Provide treatment recommendations  
❌ Handle medical emergencies  
❌ Guarantee 100% accuracy in all cases  

### Emergency Notice:
🚨 **If you're experiencing a medical emergency, call 911 immediately.**

Always consult with qualified healthcare professionals for medical decisions. Use VitalLens as a supplementary tool, not a replacement for medical care.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is part of the VitalLens AI Health Risk Assessment platform. All rights reserved.

---

**🚀 Ready to analyze your health data with AI? Run `python start_vitallens.py` and get started!**
