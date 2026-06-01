# 🏥 VitalLens - AI-Powered Medical Analysis Platform

**Advanced medical diagnosis system using deep learning and intelligent medical knowledge algorithms**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 **Overview**

VitalLens is a comprehensive AI-powered medical platform that combines:
- **Brain Tumor Detection** (95.82% accuracy)
- **COVID-19/Pneumonia Detection** (93.76% accuracy)
- **Intelligent Medical AI Chatbot** with PDF report analysis
- **Voice Interface** (Speech-to-text & Text-to-speech)
- **Cross-browser Support** (Chrome, Safari, Firefox, Edge, Brave)

---

## ✨ **Key Features**

### 🧠 **Brain Tumor Analysis**
- **Model:** EfficientNet-B0
- **Accuracy:** 95.82%
- **Classes:** Glioma, Meningioma, Pituitary, No Tumor
- **Input:** MRI scans (224x224)

### 🫁 **Chest X-ray Analysis**
- **Model:** ResNet18
- **Accuracy:** 93.76%
- **Classes:** Normal, COVID-19, Lung Opacity, Viral Pneumonia
- **Input:** Chest X-rays (224x224)

### 🤖 **Intelligent Medical AI**
- **Type:** Advanced pattern recognition with medical knowledge algorithms
- **Features:** Emergency detection, symptom analysis, PDF report reading
- **Response Time:** < 1 second (instant)
- **Languages:** English & Hindi

### 🎤 **Voice Interface**
- **Speech-to-Text:** Server-side recognition (works in all browsers)
- **Text-to-Speech:** AI responses read aloud
- **Languages:** English & Hindi
- **Technology:** MediaRecorder API + Google Speech API

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.12+
- 8GB RAM minimum
- macOS, Linux, or Windows

### **Installation**

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd VitalLens-Clean
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -r api_requirements.txt
```

3. **Start the server:**
```bash
python start_vitallens_https.py
```

4. **Open in browser:**
```
https://localhost:5001
```

**Note:** Your browser will show a security warning. Click "Advanced" → "Proceed to localhost" (this is safe for local development).

---

## 📁 **Project Structure**

```
VitalLens-Clean/
├── api_server.py              # Flask API server
├── start_vitallens_https.py   # HTTPS server launcher
├── requirements.txt            # Python dependencies
├── api_requirements.txt        # API-specific dependencies
├── README.md                   # This file
├── COMPLETE_TECHNICAL_DOCUMENTATION.md  # Technical details
│
├── src/                        # Source code
│   ├── ai_chatbot.py          # Intelligent Medical AI
│   └── prediction/            # ML model predictions
│       └── image_models.py    # Brain & chest analysis
│
├── web/                        # Web interface
│   ├── index.html             # Landing page
│   ├── brain-analysis.html    # Brain tumor analysis
│   ├── chest-analysis.html    # Chest X-ray analysis
│   ├── ai-chat.html           # AI chatbot interface
│   ├── about.html             # About page
│   ├── styles.css             # Styling
│   └── script.js              # Frontend logic
│
├── models/                     # Trained AI models
│   ├── image/                 # Image analysis models
│   │   ├── brain_tumor_cnn.pth
│   │   └── pneumonia_cnn.pth
│   └── tabular/               # Tabular data models
│       ├── diabetes_model.pkl
│       └── heart_disease_model.pkl
│
├── data/                       # Training datasets
│   ├── raw/                   # Original datasets
│   └── processed/             # Preprocessed data
│
├── scripts/                    # Utility scripts
│   ├── train_brain_tumor.py
│   ├── train_pneumonia.py
│   └── generate_ssl_cert.py
│
├── research_paper/             # Research documentation
│   ├── Research_Paper_VitalLens.md
│   ├── Research_Paper_Short_Version.md
│   ├── Research_Paper_Presentation.md
│   └── Research_Paper_Guide.md
│
├── docs/                       # Additional documentation
│   └── [various documentation files]
│
└── delete/                     # Deprecated/old files
    └── [files safe to delete]
```

## 📦 **Git-Friendly Layout**

To keep the repository practical to clone and review, the codebase tracks the application source, documentation, and trained models, while leaving large local-only assets out of git.

- Tracked: `src/`, `web/`, `scripts/`, `docs/`, `research_paper/`, `models/`
- Ignored: `data/raw/archive/`, `data/raw/COVID-19_Radiography_Dataset/`, `data/kaggle_downloads/`, `data/processed/`, local SSL certs, caches, and temp files
- See `data/README.md` for the dataset policy and local setup notes

---

## 🎯 **Usage**

### **1. Brain Tumor Analysis**
1. Navigate to `https://localhost:5001/brain-analysis.html`
2. Upload an MRI scan image
3. Click "Analyze Brain Scan"
4. View results with confidence scores and recommendations

### **2. Chest X-ray Analysis**
1. Navigate to `https://localhost:5001/chest-analysis.html`
2. Upload a chest X-ray image
3. Click "Analyze Chest X-ray"
4. View COVID-19/Pneumonia detection results

### **3. AI Medical Chatbot**
1. Navigate to `https://localhost:5001/ai-chat.html`
2. Type your medical question or upload PDF reports
3. Use voice input (click 🎤 microphone icon)
4. Get instant AI-powered medical guidance

---

## 🔧 **Technical Details**

### **Backend**
- **Framework:** Flask 3.0
- **ML Framework:** PyTorch 2.0
- **Image Processing:** PIL, OpenCV
- **PDF Processing:** PyPDF2
- **Speech Recognition:** SpeechRecognition + pydub

### **Frontend**
- **Framework:** Vanilla JavaScript
- **Styling:** Tailwind CSS
- **Icons:** Font Awesome
- **Voice:** Web Speech API + MediaRecorder API

### **AI Models**
- **Brain Tumor:** EfficientNet-B0 (95.82% accuracy)
- **Pneumonia:** ResNet18 (93.76% accuracy)
- **Chatbot:** Intelligent Medical Knowledge System

### **Security**
- **HTTPS:** Self-signed SSL certificates
- **CORS:** Enabled for local development
- **Privacy:** All processing done locally

---

## 📊 **Model Performance**

### **Brain Tumor Detection**
| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Glioma | 96.2% | 95.8% | 96.0% |
| Meningioma | 95.5% | 96.1% | 95.8% |
| Pituitary | 97.1% | 96.8% | 96.9% |
| No Tumor | 94.3% | 94.7% | 94.5% |
| **Overall** | **95.8%** | **95.9%** | **95.8%** |

### **Pneumonia Detection**
| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Normal | 94.1% | 93.8% | 93.9% |
| COVID-19 | 93.5% | 94.2% | 93.8% |
| Lung Opacity | 92.8% | 93.1% | 92.9% |
| Viral Pneumonia | 94.7% | 93.9% | 94.3% |
| **Overall** | **93.8%** | **93.8%** | **93.8%** |

---

## 🎓 **Research Paper**

Complete research documentation available in `research_paper/` folder:
- **Full Paper:** `Research_Paper_VitalLens.md` (6,000 words)
- **Short Version:** `Research_Paper_Short_Version.md` (500 words)
- **Presentation:** `Research_Paper_Presentation.md` (22 slides)
- **Guide:** `Research_Paper_Guide.md` (customization instructions)

---

## 🛠️ **Development**

### **Training Models**
```bash
# Train brain tumor model
python scripts/train_brain_tumor.py

# Train pneumonia model
python scripts/train_pneumonia.py
```

### **Generate SSL Certificates**
```bash
python scripts/generate_ssl_cert.py
```

### **Run Tests**
```bash
pytest tests/
```

---

## 🌐 **Browser Compatibility**

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome | ✅ Full Support | All features work |
| Firefox | ✅ Full Support | All features work |
| Safari | ✅ Full Support | Voice features work |
| Edge | ✅ Full Support | All features work |
| Brave | ✅ Full Support | Voice features work |

---

## 📝 **API Endpoints**

### **Health Check**
```
GET /api/health
```

### **Brain Analysis**
```
POST /api/analyze/brain
Content-Type: multipart/form-data
Body: { image: <file> }
```

### **Chest Analysis**
```
POST /api/analyze/chest
Content-Type: multipart/form-data
Body: { image: <file> }
```

### **AI Chat**
```
POST /api/chat
Content-Type: application/json
Body: { 
  message: string,
  files: array,
  history: array
}
```

### **Speech Recognition**
```
POST /api/speech/recognize
Content-Type: application/json
Body: {
  audio: base64_string,
  language: string
}
```

---

## 🔒 **Privacy & Security**

- **Local Processing:** All AI processing done on your machine
- **No Data Collection:** No user data sent to external servers
- **HTTPS:** Secure communication with SSL encryption
- **No Tracking:** No analytics or tracking scripts

---

## 🤝 **Contributing**

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 **Author**

**Anas**
- Project: VitalLens AI Medical Platform
- Year: 2026

---

## 🙏 **Acknowledgments**

- **Datasets:** 
  - Brain Tumor: Kaggle Brain Tumor Dataset
  - Pneumonia: COVID-19 Radiography Database
- **Frameworks:** PyTorch, Flask, Tailwind CSS
- **Models:** EfficientNet, ResNet

---

## 📞 **Support**

For issues or questions:
1. Check `COMPLETE_TECHNICAL_DOCUMENTATION.md`
2. Review `research_paper/` documentation
3. Check the `docs/` folder for specific guides

---

## 🚀 **Quick Commands**

```bash
# Start server
python start_vitallens_https.py

# Install dependencies
pip install -r requirements.txt

# Check API health
curl -k https://localhost:5001/api/health

# Stop server
pkill -f "start_vitallens_https.py"
```

---

**🏥 VitalLens - Making Medical AI Accessible to Everyone** ✨