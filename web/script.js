// VitalLens JavaScript - Multi-page Interactive functionality

// Global variables
let chatMessages = [];
let uploadedFiles = {
    brain: null,
    chest: null,
    chat: []
};

// Ensure uploadedFiles.chat is always an array
if (!Array.isArray(uploadedFiles.chat)) {
    uploadedFiles.chat = [];
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - VitalLens initializing...');
    initializeApp();
    checkAPIConnection();
});

// Check API connection on startup
function checkAPIConnection() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'healthy') {
                console.log('✅ VitalLens API connected successfully');
                showConnectionStatus('connected');
            } else {
                console.warn('⚠️ API health check failed:', data);
                showConnectionStatus('warning');
            }
        })
        .catch(error => {
            console.error('❌ API connection failed:', error);
            showConnectionStatus('disconnected');
        });
}

function showConnectionStatus(status) {
    // Create status indicator if it doesn't exist
    let statusIndicator = document.getElementById('api-status');
    if (!statusIndicator) {
        statusIndicator = document.createElement('div');
        statusIndicator.id = 'api-status';
        statusIndicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            z-index: 1000;
            transition: all 0.3s ease;
        `;
        document.body.appendChild(statusIndicator);
    }
    
    if (status === 'connected') {
        statusIndicator.innerHTML = '🟢 AI Models Connected';
        statusIndicator.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        statusIndicator.style.color = 'white';
        // Hide after 3 seconds
        setTimeout(() => {
            statusIndicator.style.opacity = '0';
        }, 3000);
    } else if (status === 'warning') {
        statusIndicator.innerHTML = '🟡 AI Models Loading...';
        statusIndicator.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
        statusIndicator.style.color = 'white';
    } else {
        statusIndicator.innerHTML = '🔴 AI Models Offline';
        statusIndicator.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
        statusIndicator.style.color = 'white';
    }
}

function initializeApp() {
    console.log('Initializing VitalLens app...');
    setupNavigation();
    
    // Detect current page and initialize appropriate functionality
    const currentPage = getCurrentPage();
    console.log('Current page detected:', currentPage);
    
    switch(currentPage) {
        case 'index':
            setupHomePage();
            break;
        case 'brain-analysis':
            setupBrainAnalysisPage();
            break;
        case 'chest-analysis':
            setupChestAnalysisPage();
            break;
        case 'ai-chat':
            console.log('Setting up AI chat page...');
            setupChatPage();
            break;
        case 'about':
            setupAboutPage();
            break;
        default:
            setupHomePage();
    }
    
    setupAnimations();
    setupScrollReveal();
}

// Detect current page based on URL
function getCurrentPage() {
    const path = window.location.pathname;
    const filename = path.split('/').pop().split('.')[0];
    return filename || 'index';
}

// Setup functions for each page
function setupHomePage() {
    // Home page specific functionality
    console.log('Home page initialized');
}

function setupBrainAnalysisPage() {
    setupImageUpload('brain');
}

function setupChestAnalysisPage() {
    setupImageUpload('chest');
}

function setupChatPage() {
    console.log('Setting up chat page functionality...');
    setupChat();
    setupChatFileUpload();
    setupVoiceChat();
}

function setupAboutPage() {
    // About page specific functionality
    console.log('About page initialized');
}

// Navigation functionality
function setupNavigation() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Smooth scrolling for navigation links (only for same-page anchors)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Close mobile menu if open
                if (mobileMenu) {
                    mobileMenu.classList.add('hidden');
                }
            }
        });
    });
}

// File upload functionality
function setupImageUpload(type) {
    const fileInput = document.getElementById(`${type}-file-input`);
    const uploadArea = document.getElementById(`${type}-upload-area`);
    const preview = document.getElementById(`${type}-preview`);
    const image = document.getElementById(`${type}-image`);
    const analyzeBtn = document.getElementById(`analyze-${type}-btn`);
    const placeholder = document.getElementById(`${type}-placeholder`);
    
    // Check if elements exist (they might not on all pages)
    if (!fileInput || !uploadArea) {
        return;
    }
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            uploadedFiles[type] = file;
            displayImagePreview(file, image, preview, uploadArea, placeholder);
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('border-indigo-500', 'bg-indigo-100');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('border-indigo-500', 'bg-indigo-100');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('border-indigo-500', 'bg-indigo-100');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            uploadedFiles[type] = file;
            fileInput.files = e.dataTransfer.files;
            displayImagePreview(file, image, preview, uploadArea, placeholder);
        }
    });
    
    // Analyze button
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function() {
            if (uploadedFiles[type]) {
                analyzeImage(type);
            }
        });
    }
}

function displayImagePreview(file, imageElement, previewElement, uploadArea, placeholder) {
    const reader = new FileReader();
    reader.onload = function(e) {
        if (imageElement) {
            imageElement.src = e.target.result;
        }
        if (previewElement) {
            previewElement.classList.remove('hidden');
        }
        if (uploadArea) {
            uploadArea.classList.add('hidden');
        }
        if (placeholder) {
            placeholder.classList.add('hidden');
        }
    };
    reader.readAsDataURL(file);
}

function analyzeImage(type) {
    showLoading();
    
    // Create FormData to send file to API
    const formData = new FormData();
    formData.append('image', uploadedFiles[type]);
    
    // Determine API endpoint
    const endpoint = type === 'brain' ? '/api/analyze/brain' : '/api/analyze/chest';
    
    // Send to real API
    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            showRealAnalysisResults(type, data);
        } else {
            showAnalysisError(type, data.error);
        }
    })
    .catch(error => {
        hideLoading();
        showAnalysisError(type, 'Network error: ' + error.message);
    });
}

function showRealAnalysisResults(type, data) {
    const resultsElement = document.getElementById(`${type}-results`);
    const confidenceElement = document.getElementById(`${type}-confidence`);
    const resultElement = document.getElementById(`${type}-result`);
    const placeholder = document.getElementById(`${type}-placeholder`);
    
    // Update confidence and result
    confidenceElement.textContent = `${data.confidence}%`;
    resultElement.textContent = data.prediction;
    
    // Update result card styling based on result type
    const resultCard = resultsElement.querySelector('div');
    if (data.result_type === 'success') {
        resultCard.className = 'bg-gradient-to-r from-green-900/80 to-green-800/80 rounded-2xl p-6 border border-green-500/50 backdrop-blur-sm';
        resultCard.querySelector('i').className = 'fas fa-check-circle text-green-400 mr-2';
    } else if (data.result_type === 'emergency') {
        resultCard.className = 'bg-gradient-to-r from-red-900/80 to-red-800/80 rounded-2xl p-6 border border-red-500/50 backdrop-blur-sm';
        resultCard.querySelector('i').className = 'fas fa-exclamation-triangle text-red-400 mr-2';
    } else {
        resultCard.className = 'bg-gradient-to-r from-yellow-900/80 to-yellow-800/80 rounded-2xl p-6 border border-yellow-500/50 backdrop-blur-sm';
        resultCard.querySelector('i').className = 'fas fa-exclamation-triangle text-yellow-400 mr-2';
    }
    
    // Update recommendations with better visibility
    const recommendationsContainer = document.getElementById(`${type}-recommendations`);
    if (recommendationsContainer && data.recommendations) {
        const recommendationsList = recommendationsContainer.querySelector('ul');
        recommendationsList.innerHTML = '';
        
        data.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.className = 'flex items-start';
            li.innerHTML = `
                <i class="fas fa-check text-green-400 mr-3 mt-1"></i>
                <span class="text-white font-medium">${rec}</span>
            `;
            recommendationsList.appendChild(li);
        });
    }
    
    // Display detailed probabilities
    displayProbabilityBars(type, data.all_probabilities);
    
    // Hide placeholder and show results
    if (placeholder) {
        placeholder.classList.add('hidden');
    }
    resultsElement.classList.remove('hidden');
    resultsElement.scrollIntoView({ behavior: 'smooth' });
}

function displayProbabilityBars(type, probabilities) {
    const probabilityContainer = document.getElementById(`${type}-probability-bars`);
    if (!probabilityContainer || !probabilities) return;
    
    probabilityContainer.innerHTML = '';
    
    // Sort probabilities by value (highest first)
    const sortedProbs = Object.entries(probabilities).sort((a, b) => b[1] - a[1]);
    
    sortedProbs.forEach(([className, probability]) => {
        const probDiv = document.createElement('div');
        probDiv.className = 'space-y-2';
        
        // Determine color based on probability
        let barColor = 'bg-gray-500';
        let textColor = 'text-gray-300';
        
        if (probability > 50) {
            barColor = 'bg-green-500';
            textColor = 'text-green-400';
        } else if (probability > 20) {
            barColor = 'bg-yellow-500';
            textColor = 'text-yellow-400';
        } else if (probability > 5) {
            barColor = 'bg-orange-500';
            textColor = 'text-orange-400';
        } else {
            barColor = 'bg-red-500';
            textColor = 'text-red-400';
        }
        
        probDiv.innerHTML = `
            <div class="flex justify-between items-center">
                <span class="text-white font-medium">${className}:</span>
                <span class="${textColor} font-bold">${probability.toFixed(1)}%</span>
            </div>
            <div class="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                <div class="${barColor} h-full rounded-full transition-all duration-1000 ease-out" 
                     style="width: ${Math.max(probability, 2)}%"></div>
            </div>
        `;
        
        probabilityContainer.appendChild(probDiv);
    });
}

function showAnalysisError(type, errorMessage) {
    const resultsElement = document.getElementById(`${type}-results`);
    const placeholder = document.getElementById(`${type}-placeholder`);
    
    // Show error message
    if (resultsElement) {
        resultsElement.innerHTML = `
            <div class="bg-gradient-to-r from-red-900/80 to-red-800/80 rounded-2xl p-6 border border-red-500/50 backdrop-blur-sm">
                <div class="text-center">
                    <i class="fas fa-exclamation-triangle text-red-400 text-4xl mb-4"></i>
                    <h3 class="text-xl font-semibold text-white mb-2">Analysis Error</h3>
                    <p class="text-red-200 font-medium">${errorMessage}</p>
                    <p class="text-red-300 text-sm mt-2">Please try uploading a different image or check your connection.</p>
                </div>
            </div>
        `;
        resultsElement.classList.remove('hidden');
        if (placeholder) {
            placeholder.classList.add('hidden');
        }
    }
}

// Chat functionality
function setupChat() {
    const sendBtn = document.getElementById('send-chat-btn');
    const clearBtn = document.getElementById('clear-chat-btn');
    const chatInput = document.getElementById('chat-input');
    
    console.log('Setting up chat:', { sendBtn, clearBtn, chatInput });
    
    // Check if chat elements exist (only on chat page)
    if (!sendBtn || !clearBtn || !chatInput) {
        console.log('Chat elements not found, skipping chat setup');
        return;
    }
    
    console.log('Adding event listeners to chat elements');
    
    sendBtn.addEventListener('click', function(e) {
        console.log('Send button clicked');
        e.preventDefault();
        sendMessage();
    });
    
    clearBtn.addEventListener('click', function(e) {
        console.log('Clear button clicked');
        e.preventDefault();
        clearChat();
    });
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            console.log('Enter key pressed in chat input');
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Initialize chat with welcome message
    initializeChat();
}

function setupChatFileUpload() {
    const fileInput = document.getElementById('chat-file-input');
    const filesPreview = document.getElementById('chat-files-preview');
    const filesList = document.getElementById('chat-files-list');
    
    console.log('Setting up chat file upload:', { fileInput, filesPreview, filesList });
    
    // Check if elements exist
    if (!fileInput || !filesPreview || !filesList) {
        console.log('Chat file upload elements not found, skipping setup');
        return;
    }
    
    // Initialize uploadedFiles.chat if not already an array
    if (!Array.isArray(uploadedFiles.chat)) {
        uploadedFiles.chat = [];
    }
    
    fileInput.addEventListener('change', function(e) {
        console.log('File input changed:', e.target.files);
        const files = Array.from(e.target.files);
        uploadedFiles.chat = files;
        displayChatFiles(files, filesList, filesPreview);
    });
}

function displayChatFiles(files, listElement, previewElement) {
    listElement.innerHTML = '';
    
    files.forEach((file, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'file-preview';
        fileDiv.innerHTML = `
            <div class="flex items-center space-x-2 p-2">
                <i class="fas fa-file text-indigo-600"></i>
                <span class="text-sm text-gray-700 truncate max-w-32">${file.name}</span>
                <button onclick="removeFile(${index})" class="remove-file">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        listElement.appendChild(fileDiv);
    });
    
    previewElement.classList.toggle('hidden', files.length === 0);
}

function removeFile(index) {
    if (!uploadedFiles.chat || !Array.isArray(uploadedFiles.chat)) {
        uploadedFiles.chat = [];
        return;
    }
    
    uploadedFiles.chat.splice(index, 1);
    const fileInput = document.getElementById('chat-file-input');
    const filesPreview = document.getElementById('chat-files-preview');
    const filesList = document.getElementById('chat-files-list');
    
    if (filesList && filesPreview) {
        displayChatFiles(uploadedFiles.chat, filesList, filesPreview);
    }
    
    // Update file input
    if (fileInput) {
        const dt = new DataTransfer();
        uploadedFiles.chat.forEach(file => dt.items.add(file));
        fileInput.files = dt.files;
    }
}

function initializeChat() {
    // Check if chat messages container exists
    const chatContainer = document.getElementById('chat-messages');
    if (!chatContainer) {
        return;
    }
    
    chatMessages = [{
        role: 'ai',
        content: `Hello! I'm your AI Health Assistant. 👨‍⚕️

**How I can help:**
• Analyze medical documents (lab results, prescriptions, X-rays)
• Understand symptoms and provide recommendations  
• Find nearby doctors and specialists
• Explain medical terms and results

**Just type your message below and/or upload any medical documents.** I'll extract all the information I need from your documents and only ask follow-up questions if necessary.

What can I help you with today?`,
        timestamp: new Date()
    }];
    
    displayChatMessages();
}

function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    const files = uploadedFiles.chat || [];
    
    console.log('Send message called:', { message, filesCount: files.length });
    
    if (!message && files.length === 0) {
        console.log('No message or files to send');
        return;
    }
    
    // Add user message
    if (message) {
        chatMessages.push({
            role: 'user',
            content: message,
            timestamp: new Date()
        });
    }
    
    // Add file upload message
    if (files.length > 0) {
        const fileNames = files.map(f => f.name).join(', ');
        chatMessages.push({
            role: 'user',
            content: `📎 Uploaded files: ${fileNames}`,
            timestamp: new Date()
        });
    }
    
    // Clear input
    chatInput.value = '';
    uploadedFiles.chat = [];
    const filesPreview = document.getElementById('chat-files-preview');
    const fileInput = document.getElementById('chat-file-input');
    if (filesPreview) filesPreview.classList.add('hidden');
    if (fileInput) fileInput.value = '';
    
    displayChatMessages();
    
    // Show typing indicator
    showTypingIndicator();
    
    // Process files and extract content
    processFilesAndSend(message, files);
}

async function processFilesAndSend(message, files) {
    try {
        let filesData = [];
        
        // Extract content from files
        for (const file of files) {
            if (file.type === 'application/pdf') {
                // For PDFs, we'll send the file to server for processing
                const base64 = await fileToBase64(file);
                filesData.push({
                    name: file.name,
                    type: file.type,
                    size: file.size,
                    content: base64
                });
            } else if (file.type.startsWith('image/')) {
                // For images, convert to base64
                const base64 = await fileToBase64(file);
                filesData.push({
                    name: file.name,
                    type: file.type,
                    size: file.size,
                    content: base64
                });
            } else {
                // For other files, just send metadata
                filesData.push({
                    name: file.name,
                    type: file.type,
                    size: file.size
                });
            }
        }
        
        // Send to real AI API
        const requestData = {
            message: message,
            files: filesData,
            history: chatMessages
        };
        
        console.log('Sending request to API with file content');
        
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            console.log('API response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('API response data:', data);
            hideTypingIndicator();
            if (data.success) {
                chatMessages.push({
                    role: 'ai',
                    content: data.message,
                    timestamp: new Date()
                });
            } else {
                chatMessages.push({
                    role: 'ai',
                    content: `I apologize, but I encountered an error: ${data.error}. Please try again or contact support if the issue persists.`,
                    timestamp: new Date()
                });
            }
            displayChatMessages();
        })
        .catch(error => {
            console.error('API request failed:', error);
            hideTypingIndicator();
            chatMessages.push({
                role: 'ai',
                content: `I'm having trouble connecting to my AI systems right now. Please check your internet connection and try again. Error: ${error.message}`,
                timestamp: new Date()
            });
            displayChatMessages();
        });
        
    } catch (error) {
        console.error('Error processing files:', error);
        hideTypingIndicator();
        chatMessages.push({
            role: 'ai',
            content: `Error processing files: ${error.message}`,
            timestamp: new Date()
        });
        displayChatMessages();
    }
}

function generateAIResponse(userMessage, files) {
    let response = '';
    
    // Simulate different responses based on input
    if (files.length > 0) {
        response = `Thank you for sharing your information with me. I've analyzed everything and here's what I found:

**📋 Document Analysis:**
• ${files[0].name}: ${getFileType(files[0].name)}

**🔍 Key Medical Findings:**
• Document successfully analyzed
• Various health parameters detected
• Recommendations generated based on content

**🍎 Personalized recommendations:**
• Stay hydrated - drink 8 glasses of water daily
• Get 7-9 hours of quality sleep
• Practice stress management techniques

**🎯 Recommended next steps:**
• Continue regular health monitoring
• Follow the recommendations above
• Schedule routine checkup if due

**💬 Questions?** Feel free to ask about any of these findings, or upload additional documents for analysis. I'm here to help explain everything clearly! 😊`;
    } else if (userMessage.toLowerCase().includes('headache') || userMessage.toLowerCase().includes('dizzy')) {
        response = `I understand you're experiencing headaches and dizziness. Let me help you with this:

**🔍 Possible causes:**
• Dehydration
• Stress or tension
• Sleep deprivation
• Eye strain
• Blood pressure changes

**💡 Immediate recommendations:**
• Drink plenty of water
• Rest in a quiet, dark room
• Apply a cold compress to your forehead
• Practice deep breathing exercises

**⚠️ When to seek medical attention:**
• Severe or sudden onset headache
• Headache with fever, stiff neck, or rash
• Changes in vision or speech
• Headache after head injury

**🎯 Next steps:**
• Monitor your symptoms
• Keep a headache diary
• If symptoms persist or worsen, consult a healthcare provider

Would you like me to help you find nearby doctors or provide more specific advice?`;
    } else {
        response = `Thank you for reaching out! I'm here to help with your health concerns.

**How I can assist you:**
• Analyze medical documents and lab results
• Provide information about symptoms
• Suggest when to seek medical care
• Find healthcare providers in your area

**To provide the best help, please:**
• Describe your symptoms in detail
• Upload any relevant medical documents
• Let me know your age and location (for doctor recommendations)

**Common topics I can help with:**
• Symptom analysis and recommendations
• Lab result interpretation
• Medication questions
• Finding specialists

What specific health concern would you like to discuss today?`;
    }
    
    chatMessages.push({
        role: 'ai',
        content: response,
        timestamp: new Date()
    });
    
    displayChatMessages();
}

function getFileType(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    if (ext === 'pdf') return 'Lab Report';
    if (['jpg', 'jpeg', 'png'].includes(ext)) return 'Medical Image';
    return 'Medical Document';
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full flex items-center justify-center">
            <i class="fas fa-robot text-white"></i>
        </div>
        <div>
            <div class="font-semibold text-indigo-600 text-sm">AI Doctor is typing</div>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function displayChatMessages() {
    const chatContainer = document.getElementById('chat-messages');
    
    // Check if chat container exists
    if (!chatContainer) {
        return;
    }
    
    // Clear existing messages except typing indicator
    const typingIndicator = document.getElementById('typing-indicator');
    chatContainer.innerHTML = '';
    if (typingIndicator) {
        chatContainer.appendChild(typingIndicator);
    }
    
    chatMessages.forEach(message => {
        const messageDiv = document.createElement('div');
        
        if (message.role === 'ai') {
            messageDiv.className = 'flex items-start space-x-3 mb-6 chat-message';
            
            // Format AI message content for better readability
            const formattedContent = formatAIMessage(message.content);
            
            messageDiv.innerHTML = `
                <div class="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-robot text-white text-lg"></i>
                </div>
                <div class="bg-gray-700/90 backdrop-blur-sm rounded-2xl p-6 max-w-4xl shadow-lg border border-gray-600">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center">
                            <i class="fas fa-user-md text-indigo-400 mr-2"></i>
                            <span class="font-semibold text-indigo-400 text-lg">AI Doctor</span>
                        </div>
                        <button onclick="readSpecificMessage('${message.timestamp}')" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-lg text-sm transition-colors flex items-center">
                            <i class="fas fa-volume-up mr-1"></i>
                            Read Aloud
                        </button>
                    </div>
                    <div class="text-gray-100 leading-relaxed">${formattedContent}</div>
                </div>
            `;
        } else if (message.role === 'system') {
            messageDiv.className = 'flex justify-center mb-4';
            messageDiv.innerHTML = `
                <div class="bg-yellow-900/60 border border-yellow-600/50 text-yellow-200 px-4 py-2 rounded-lg text-sm max-w-2xl text-center">
                    ${message.content}
                </div>
            `;
        } else {
            messageDiv.className = 'flex items-start space-x-3 mb-4 justify-end user-message';
            messageDiv.innerHTML = `
                <div class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-2xl p-4 max-w-2xl shadow-sm">
                    <div class="font-semibold mb-1">You</div>
                    <div class="whitespace-pre-line">${message.content}</div>
                </div>
                <div class="w-10 h-10 bg-gradient-to-r from-green-500 to-green-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-user text-white"></i>
                </div>
            `;
        }
        
        if (typingIndicator) {
            chatContainer.insertBefore(messageDiv, typingIndicator);
        } else {
            chatContainer.appendChild(messageDiv);
        }
    });
    
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function formatAIMessage(content) {
    // Enhanced formatting for AI messages
    let formatted = content;
    
    // Format emergency alerts with better styling
    formatted = formatted.replace(
        /🚨 \*\*URGENT MEDICAL EMERGENCY\*\*:(.*?)!/g,
        `<div class="bg-red-900/80 border-l-4 border-red-500 rounded-lg p-4 mb-6 shadow-lg animate-pulse">
            <div class="flex items-center mb-3">
                <i class="fas fa-exclamation-triangle text-red-400 text-2xl mr-3 animate-bounce"></i>
                <span class="text-red-300 font-bold text-xl">URGENT MEDICAL EMERGENCY</span>
            </div>
            <p class="text-red-100 font-medium text-lg">$1!</p>
        </div>`
    );
    
    // Format high priority warnings
    formatted = formatted.replace(
        /⚠️ \*\*High Priority\*\*:(.*?)(?=\n\n|\n\*\*|$)/gs,
        `<div class="bg-orange-900/80 border-l-4 border-orange-500 rounded-lg p-4 mb-6 shadow-lg">
            <div class="flex items-center mb-3">
                <i class="fas fa-exclamation-circle text-orange-400 text-xl mr-3"></i>
                <span class="text-orange-300 font-bold text-lg">High Priority</span>
            </div>
            <p class="text-orange-100 font-medium">$1</p>
        </div>`
    );
    
    // Format section headers with enhanced styling
    formatted = formatted.replace(
        /\*\*📋 (Document Analysis|I analyzed \d+ documents):\*\*/g,
        `<div class="bg-gradient-to-r from-blue-900/60 to-blue-800/60 border border-blue-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-blue-300 font-semibold text-lg mb-2">
                <i class="fas fa-file-medical text-blue-400 mr-3 text-xl"></i>
                Document Analysis
            </h3>
        </div>`
    );
    
    formatted = formatted.replace(
        /\*\*👤 Patient Information \(from documents\):\*\*/g,
        `<div class="bg-gradient-to-r from-cyan-900/60 to-cyan-800/60 border border-cyan-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-cyan-300 font-semibold text-lg mb-2">
                <i class="fas fa-user-circle text-cyan-400 mr-3 text-xl"></i>
                Patient Information
            </h3>
        </div>`
    );
    
    formatted = formatted.replace(
        /\*\*🔍 Key Medical Findings:\*\*/g,
        `<div class="bg-gradient-to-r from-green-900/60 to-green-800/60 border border-green-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-green-300 font-semibold text-lg mb-2">
                <i class="fas fa-search text-green-400 mr-3 text-xl"></i>
                Key Medical Findings
            </h3>
        </div>`
    );
    
    formatted = formatted.replace(
        /\*\*⚠️ Values requiring attention:\*\*/g,
        `<div class="bg-gradient-to-r from-red-900/60 to-red-800/60 border border-red-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-red-300 font-semibold text-lg mb-2">
                <i class="fas fa-exclamation-triangle text-red-400 mr-3 text-xl"></i>
                Values Requiring Attention
            </h3>
        </div>`
    );
    
    formatted = formatted.replace(
        /\*\*🍎 Personalized diet recommendations:\*\*/g,
        `<div class="bg-gradient-to-r from-orange-900/60 to-orange-800/60 border border-orange-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-orange-300 font-semibold text-lg mb-2">
                <i class="fas fa-apple-alt text-orange-400 mr-3 text-xl"></i>
                Diet Recommendations
            </h3>
        </div>`
    );
    
    formatted = formatted.replace(
        /\*\*💪 Exercise suggestions:\*\*/g,
        `<div class="bg-gradient-to-r from-purple-900/60 to-purple-800/60 border border-purple-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-purple-300 font-semibold text-lg mb-2">
                <i class="fas fa-dumbbell text-purple-400 mr-3 text-xl"></i>
                Exercise Recommendations
            </h3>
        </div>`
    );
    
    formatted = formatted.replace(
        /\*\*👨‍⚕️ Recommended specialists near (.*?):\*\*/g,
        `<div class="bg-gradient-to-r from-indigo-900/60 to-indigo-800/60 border border-indigo-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-indigo-300 font-semibold text-lg mb-2">
                <i class="fas fa-user-md text-indigo-400 mr-3 text-xl"></i>
                Recommended Specialists
            </h3>
        </div>`
    );
    
    formatted = formatted.replace(
        /\*\*🎯 Recommended next steps:\*\*/g,
        `<div class="bg-gradient-to-r from-yellow-900/60 to-yellow-800/60 border border-yellow-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-yellow-300 font-semibold text-lg mb-2">
                <i class="fas fa-bullseye text-yellow-400 mr-3 text-xl"></i>
                Next Steps
            </h3>
        </div>`
    );
    
    formatted = formatted.replace(
        /\*\*❓ To provide better recommendations, could you please share:\*\*/g,
        `<div class="bg-gradient-to-r from-gray-800/60 to-gray-700/60 border border-gray-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-gray-300 font-semibold text-lg mb-2">
                <i class="fas fa-question-circle text-gray-400 mr-3 text-xl"></i>
                Additional Information Needed
            </h3>
            <p class="text-gray-400 text-sm mb-2">To provide more personalized recommendations:</p>
        </div>`
    );
    
    // Format doctor information with enhanced cards
    formatted = formatted.replace(
        /• \*\*(Dr\. [^*]+)\*\* \(([^)]+)\) - ([^,]+), ([^,]+), ([^)]+)\)/g,
        `<div class="bg-gradient-to-r from-gray-800/80 to-gray-700/80 rounded-xl p-5 mb-4 border border-gray-600/50 shadow-lg hover:shadow-xl transition-all duration-300">
            <div class="flex items-center justify-between">
                <div class="flex-1">
                    <h4 class="text-white font-bold text-lg flex items-center">
                        <i class="fas fa-user-md text-indigo-400 mr-2"></i>
                        $1
                    </h4>
                    <p class="text-indigo-300 font-medium text-sm mt-1">$2</p>
                </div>
                <div class="text-right ml-4">
                    <div class="flex items-center justify-end mb-1">
                        <i class="fas fa-map-marker-alt text-green-400 mr-2"></i>
                        <span class="text-green-300 font-medium">$3</span>
                    </div>
                    <div class="flex items-center justify-end mb-1">
                        <i class="fas fa-star text-yellow-400 mr-2"></i>
                        <span class="text-yellow-300 font-medium">$4</span>
                    </div>
                    <div class="flex items-center justify-end">
                        <i class="fas fa-phone text-blue-400 mr-2"></i>
                        <span class="text-blue-300 font-medium text-sm">$5</span>
                    </div>
                </div>
            </div>
        </div>`
    );
    
    // Format bullet points with better icons and styling
    formatted = formatted.replace(/• ([^•\n]+)/g, function(match, text) {
        // Clean up long URLs in filenames
        text = text.replace(/https?:\/\/[^\s]+\.pdf\?[^\s]+/g, function(url) {
            // Extract just the filename part
            const filename = url.split('/').pop().split('?')[0];
            return filename.replace(/[^a-zA-Z0-9.-]/g, '_');
        });
        
        if (text.includes('Call emergency') || text.includes('CALL') || text.includes('emergency services')) {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-red-900/60 to-red-800/60 rounded-lg border border-red-500/30 shadow-lg">
                        <i class="fas fa-phone text-red-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-red-200 font-medium">${text}</span>
                    </div>`;
        } else if (text.includes('Schedule') || text.includes('appointment') || text.includes('urgent')) {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-blue-900/60 to-blue-800/60 rounded-lg border border-blue-500/30 shadow-lg">
                        <i class="fas fa-calendar-plus text-blue-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-blue-200 font-medium">${text}</span>
                    </div>`;
        } else if (text.includes('Reduce') || text.includes('Increase') || text.includes('Choose') || text.includes('Avoid')) {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-green-900/60 to-green-800/60 rounded-lg border border-green-500/30 shadow-lg">
                        <i class="fas fa-leaf text-green-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-green-200 font-medium">${text}</span>
                    </div>`;
        } else if (text.includes('minutes') || text.includes('training') || text.includes('walking') || text.includes('exercise')) {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-purple-900/60 to-purple-800/60 rounded-lg border border-purple-500/30 shadow-lg">
                        <i class="fas fa-running text-purple-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-purple-200 font-medium">${text}</span>
                    </div>`;
        } else if (text.includes('Age:') || text.includes('Location:') || text.includes('Medications:') || text.includes('Allergies:')) {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-cyan-900/60 to-cyan-800/60 rounded-lg border border-cyan-500/30 shadow-lg">
                        <i class="fas fa-user text-cyan-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-cyan-200 font-medium">${text}</span>
                    </div>`;
        } else if (text.includes('glucose') || text.includes('cholesterol') || text.includes('blood') || text.includes('mg/dL')) {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-red-900/60 to-red-800/60 rounded-lg border border-red-500/30 shadow-lg">
                        <i class="fas fa-tint text-red-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-red-200 font-medium">${text}</span>
                    </div>`;
        } else if (text.includes('detected') || text.includes('found') || text.includes('present')) {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-green-900/60 to-green-800/60 rounded-lg border border-green-500/30 shadow-lg">
                        <i class="fas fa-search-plus text-green-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-green-200 font-medium">${text}</span>
                    </div>`;
        } else if (text.includes('Continue') || text.includes('Monitor') || text.includes('Follow')) {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-yellow-900/60 to-yellow-800/60 rounded-lg border border-yellow-500/30 shadow-lg">
                        <i class="fas fa-tasks text-yellow-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-yellow-200 font-medium">${text}</span>
                    </div>`;
        } else {
            return `<div class="flex items-start mb-3 p-3 bg-gradient-to-r from-gray-800/60 to-gray-700/60 rounded-lg border border-gray-500/30 shadow-lg">
                        <i class="fas fa-check text-gray-400 mr-3 mt-1 text-lg"></i>
                        <span class="text-gray-200 font-medium">${text}</span>
                    </div>`;
        }
    });
    
    // Format questions section with better styling
    formatted = formatted.replace(
        /\*\*💬 Questions\?\*\*(.*?)(?=\n\n|\n\*\*|$)/gs,
        `<div class="bg-gradient-to-r from-indigo-900/60 to-indigo-800/60 border border-indigo-500/30 rounded-xl p-4 mb-4 shadow-lg">
            <h3 class="flex items-center text-indigo-300 font-semibold text-lg mb-2">
                <i class="fas fa-comments text-indigo-400 mr-3 text-xl"></i>
                Questions?
            </h3>
            <p class="text-indigo-200 font-medium">$1</p>
        </div>`
    );
    
    // Clean up extra asterisks and formatting
    formatted = formatted.replace(/\*\*/g, '');
    
    // Add proper spacing between sections
    formatted = formatted.replace(/(<\/div>)(\s*<div)/g, '$1<div class="mb-2"></div>$2');
    
    // Format document names to be cleaner (remove long URLs)
    formatted = formatted.replace(/Personal — [^:]+:/g, 'Personal Document:');
    
    return formatted;
}

function clearChat() {
    chatMessages = [];
    initializeChat();
}

// Helper function to convert file to base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Loading overlay
function showLoading() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('hidden');
    }
}

function hideLoading() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
    }
}

// Animation setup
function setupAnimations() {
    // Add entrance animations to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
    });
    
    // Add hover effects to interactive elements
    const interactiveElements = document.querySelectorAll('.btn-primary, .btn-secondary, .feature-card');
    interactiveElements.forEach(element => {
        element.classList.add('interactive');
    });
}

// Scroll animations
function setupScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);
    
    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        section.classList.add('reveal');
        observer.observe(section);
    });
}

// Animation setup
function setupAnimations() {
    // Add entrance animations to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
    });
    
    // Add hover effects to interactive elements
    const interactiveElements = document.querySelectorAll('.btn-primary, .btn-secondary, .feature-card');
    interactiveElements.forEach(element => {
        element.classList.add('interactive');
    });
}

// Utility functions
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('VitalLens Error:', e.error);
});

// Prevent default drag behaviors
document.addEventListener('dragover', function(e) {
    e.preventDefault();
});

document.addEventListener('drop', function(e) {
    e.preventDefault();
});

// Export functions for global access
window.scrollToSection = scrollToSection;
window.removeFile = removeFile;
window.removeBrainImage = removeBrainImage;
window.removeChestImage = removeChestImage;

// Functions to remove uploaded images
function removeBrainImage() {
    // Clear the uploaded file
    uploadedFiles.brain = null;
    
    // Reset file input
    const fileInput = document.getElementById('brain-file-input');
    if (fileInput) {
        fileInput.value = '';
    }
    
    // Hide preview and show upload area
    const preview = document.getElementById('brain-preview');
    const uploadArea = document.getElementById('brain-upload-area');
    const placeholder = document.getElementById('brain-placeholder');
    const results = document.getElementById('brain-results');
    
    if (preview) preview.classList.add('hidden');
    if (uploadArea) uploadArea.classList.remove('hidden');
    if (placeholder) placeholder.classList.remove('hidden');
    if (results) results.classList.add('hidden');
}

function removeChestImage() {
    // Clear the uploaded file
    uploadedFiles.chest = null;
    
    // Reset file input
    const fileInput = document.getElementById('chest-file-input');
    if (fileInput) {
        fileInput.value = '';
    }
    
    // Hide preview and show upload area
    const preview = document.getElementById('chest-preview');
    const uploadArea = document.getElementById('chest-upload-area');
    const placeholder = document.getElementById('chest-placeholder');
    const results = document.getElementById('chest-results');
    
    if (preview) preview.classList.add('hidden');
    if (uploadArea) uploadArea.classList.remove('hidden');
    if (placeholder) placeholder.classList.remove('hidden');
    if (results) results.classList.add('hidden');
}

// Voice Chat Functionality
let voiceRecognition = null;
let voiceSynthesis = null;
let isRecording = false;
let isSpeaking = false;
let currentLanguage = 'en-US';
let voiceRetryCount = 0;
let maxVoiceRetries = 2;
let mediaRecorder = null;
let audioChunks = [];
let useServerSideRecognition = true; // Use server-side by default for cross-browser support

function setupVoiceChat() {
    console.log('Setting up voice chat functionality...');
    
    // Check if elements exist (only on chat page)
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const voiceOutputBtn = document.getElementById('voice-output-btn');
    const languageSelect = document.getElementById('voice-language');
    const stopRecordingBtn = document.getElementById('stop-recording-btn');
    
    if (!voiceInputBtn || !voiceOutputBtn || !languageSelect) {
        console.log('Voice chat elements not found, skipping voice setup');
        return;
    }
    
    // Initialize speech recognition
    initializeSpeechRecognition();
    
    // Initialize speech synthesis
    initializeSpeechSynthesis();
    
    // Event listeners
    voiceInputBtn.addEventListener('click', toggleVoiceInput);
    voiceOutputBtn.addEventListener('click', readLastAIResponse);
    languageSelect.addEventListener('change', updateLanguage);
    if (stopRecordingBtn) {
        stopRecordingBtn.addEventListener('click', stopVoiceInput);
    }
    
    console.log('Voice chat setup complete');
}

function initializeSpeechRecognition() {
    // Check for browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.warn('Speech recognition not supported in this browser');
        showVoiceError(
            'Speech recognition is not supported in your browser.',
            'Please use Chrome, Edge, or Safari for voice features. Text input is always available!'
        );
        return;
    }
    
    // Create speech recognition instance
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    voiceRecognition = new SpeechRecognition();
    
    // Configure recognition
    voiceRecognition.continuous = false;  // Changed to false for better reliability
    voiceRecognition.interimResults = true;
    voiceRecognition.maxAlternatives = 1;
    voiceRecognition.lang = currentLanguage;
    
    console.log('Speech recognition initialized successfully');
    
    // Event handlers
    voiceRecognition.onstart = function() {
        console.log('Voice recognition started');
        isRecording = true;
        updateVoiceUI('recording');
    };
    
    voiceRecognition.onresult = function(event) {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Update chat input with transcript
        const chatInput = document.getElementById('chat-input');
        if (chatInput) {
            if (finalTranscript) {
                chatInput.value = finalTranscript;
            } else {
                chatInput.value = interimTranscript;
            }
        }
        
        // Update status
        if (interimTranscript) {
            updateVoiceStatus(`Listening: "${interimTranscript}"`);
        }
        
        // Auto-send if final transcript is complete
        if (finalTranscript.trim().length > 0) {
            console.log('Final transcript received:', finalTranscript);
            updateVoiceStatus('Processing...');
            
            // Stop recognition
            setTimeout(() => {
                stopVoiceInput();
                // Send message after a short delay
                setTimeout(() => {
                    if (finalTranscript.trim()) {
                        sendMessage();
                    }
                }, 500);
            }, 500);
        }
    };
    
    voiceRecognition.onerror = function(event) {
        console.error('Voice recognition error:', event.error);
        isRecording = false;
        updateVoiceUI('idle');
        
        let errorMessage = '';
        let solution = '';
        
        switch(event.error) {
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                solution = 'Speak louder and closer to your microphone.';
                break;
            case 'audio-capture':
                errorMessage = 'Microphone not accessible.';
                solution = 'Please check that your microphone is connected and working.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission denied.';
                solution = 'Please click the 🔒 icon in your browser address bar and allow microphone access.';
                break;
            case 'service-not-allowed':
                errorMessage = 'Voice recognition requires HTTPS or localhost.';
                solution = 'The site is running on HTTP which some browsers restrict. Solutions:\n\n' +
                          '1. Use Chrome/Edge (better localhost support)\n' +
                          '2. Access via: http://127.0.0.1:5001/ai-chat.html\n' +
                          '3. Or continue typing - voice is optional!';
                break;
            case 'network':
                errorMessage = 'Speech recognition service unavailable.';
                solution = 'The browser\'s speech recognition service (Google) may be temporarily unavailable. Solutions:\n\n' +
                          '1. Check your internet connection\n' +
                          '2. Try again in a few moments\n' +
                          '3. Restart your browser\n' +
                          '4. Use text input instead (works offline!)\n\n' +
                          'Note: Speech recognition requires internet as it uses Google\'s servers.';
                break;
            case 'aborted':
                // Don't show error for user-initiated stops
                console.log('Speech recognition aborted by user');
                return;
            default:
                errorMessage = 'Voice recognition error: ' + event.error;
                solution = 'Please try typing your message instead. Voice features require internet connection.';
        }
        
        showVoiceError(errorMessage, solution);
    };
    
    voiceRecognition.onend = function() {
        console.log('Voice recognition ended');
        isRecording = false;
        updateVoiceUI('idle');
    };
}

function initializeSpeechSynthesis() {
    // Check for browser support
    if (!('speechSynthesis' in window)) {
        console.warn('Speech synthesis not supported in this browser');
        showVoiceError('Text-to-speech is not supported in your browser.');
        return;
    }
    
    voiceSynthesis = window.speechSynthesis;
    console.log('Speech synthesis initialized');
}

function toggleVoiceInput() {
    if (!voiceRecognition) {
        showVoiceError('Voice recognition not available. Please check your browser compatibility.');
        return;
    }
    
    if (isRecording) {
        stopVoiceInput();
    } else {
        startVoiceInput();
    }
}

function startVoiceInput() {
    // Use server-side recognition for cross-browser support
    if (useServerSideRecognition) {
        startServerSideRecording();
        return;
    }
    
    // Fallback to browser-based recognition (Chrome/Edge only)
    if (!voiceRecognition) {
        showVoiceError('Voice recognition not initialized.', 'Please refresh the page and try again.');
        return;
    }
    
    // Check if already recording
    if (isRecording) {
        console.log('Already recording, ignoring start request');
        return;
    }
    
    // Request microphone permission and start recording
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            console.log('Microphone access granted');
            
            // Stop the stream (we just needed permission)
            stream.getTracks().forEach(track => track.stop());
            
            // Start recognition
            try {
                voiceRecognition.lang = currentLanguage;
                voiceRecognition.start();
                voiceRetryCount = 0; // Reset retry count on successful start
                console.log('Voice recognition started successfully');
            } catch (error) {
                console.error('Error starting voice recognition:', error);
                
                // If already started, stop and restart
                if (error.message && error.message.includes('already started')) {
                    console.log('Recognition already started, stopping first...');
                    voiceRecognition.stop();
                    setTimeout(() => {
                        try {
                            voiceRecognition.start();
                        } catch (e) {
                            console.error('Retry failed:', e);
                            showVoiceError('Failed to start voice recognition.', 'Please try again or use text input.');
                        }
                    }, 500);
                } else {
                    showVoiceError('Failed to start voice recognition.', 'Please try again or use text input.');
                }
            }
        })
        .catch(function(error) {
            console.error('Microphone permission error:', error);
            showVoiceError(
                'Microphone access denied.',
                'Please allow microphone permissions in your browser settings and try again.'
            );
        });
}

function startServerSideRecording() {
    console.log('Starting server-side voice recording...');
    
    // Request microphone access
    navigator.mediaDevices.getUserMedia({ 
        audio: {
            channelCount: 1,
            sampleRate: 16000,
            echoCancellation: true,
            noiseSuppression: true
        } 
    })
        .then(function(stream) {
            console.log('Microphone access granted for server-side recording');
            
            // Create MediaRecorder with best available format
            let options = { mimeType: 'audio/webm;codecs=opus' };
            
            // Try different formats based on browser support
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                console.log('opus not supported, trying vorbis...');
                options = { mimeType: 'audio/webm;codecs=vorbis' };
            }
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                console.log('vorbis not supported, trying default webm...');
                options = { mimeType: 'audio/webm' };
            }
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                console.log('webm not supported, using default...');
                options = {};
            }
            
            console.log('Using MediaRecorder with:', options);
            
            try {
                mediaRecorder = new MediaRecorder(stream, options);
            } catch (e) {
                console.error('MediaRecorder creation error:', e);
                // Fallback without options
                mediaRecorder = new MediaRecorder(stream);
            }
            
            audioChunks = [];
            
            mediaRecorder.ondataavailable = function(event) {
                if (event.data.size > 0) {
                    console.log('Audio chunk received:', event.data.size, 'bytes');
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = function() {
                console.log('Recording stopped, processing audio...');
                console.log('Total chunks:', audioChunks.length);
                processRecordedAudio(stream);
            };
            
            mediaRecorder.onerror = function(event) {
                console.error('MediaRecorder error:', event.error);
                stream.getTracks().forEach(track => track.stop());
                isRecording = false;
                updateVoiceUI('idle');
                showVoiceError('Recording error occurred.', 'Please try again.');
            };
            
            // Start recording
            mediaRecorder.start();
            isRecording = true;
            updateVoiceUI('recording');
            updateVoiceStatus('Recording... Speak now!');
            
            console.log('Server-side recording started successfully');
            
            // Auto-stop after 10 seconds (safety measure)
            setTimeout(() => {
                if (isRecording && mediaRecorder && mediaRecorder.state === 'recording') {
                    console.log('Auto-stopping recording after 10 seconds');
                    stopVoiceInput();
                }
            }, 10000);
            
        })
        .catch(function(error) {
            console.error('Microphone permission error:', error);
            showVoiceError(
                'Microphone access denied.',
                'Please allow microphone permissions in your browser settings and try again.'
            );
        });
}

function processRecordedAudio(stream) {
    // Stop all tracks
    stream.getTracks().forEach(track => track.stop());
    
    // Create audio blob
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    
    console.log('Audio blob created, size:', audioBlob.size);
    
    // Convert to base64 and send to server
    const reader = new FileReader();
    reader.onloadend = function() {
        const base64Audio = reader.result;
        sendAudioToServer(base64Audio);
    };
    reader.readAsDataURL(audioBlob);
}

function sendAudioToServer(audioData) {
    console.log('Sending audio to server for recognition...');
    updateVoiceStatus('Processing speech...');
    
    fetch('/api/speech/recognize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            audio: audioData,
            language: currentLanguage
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
        isRecording = false;
        updateVoiceUI('idle');
        
        if (data.success && data.text) {
            // Update chat input with recognized text
            const chatInput = document.getElementById('chat-input');
            if (chatInput) {
                chatInput.value = data.text;
            }
            
            // Show success message
            showVoiceSuccess(`Recognized: "${data.text}"`);
            
            // Auto-send message
            setTimeout(() => {
                sendMessage();
            }, 500);
        } else {
            showVoiceError(
                data.error || 'Could not recognize speech.',
                'Please speak clearly and try again, or use text input.'
            );
        }
    })
    .catch(error => {
        console.error('Server recognition error:', error);
        isRecording = false;
        updateVoiceUI('idle');
        showVoiceError(
            'Failed to process speech.',
            'Please check your connection and try again, or use text input.'
        );
    });
}

function stopVoiceInput() {
    if (useServerSideRecognition && mediaRecorder && isRecording) {
        console.log('Stopping server-side recording...');
        mediaRecorder.stop();
        // The onstop event will handle the rest
    } else if (voiceRecognition && isRecording) {
        voiceRecognition.stop();
    }
}

function readLastAIResponse() {
    if (!voiceSynthesis) {
        showVoiceError('Text-to-speech not available in your browser.');
        return;
    }
    
    // Stop any current speech
    voiceSynthesis.cancel();
    
    // Find the last AI message
    const lastAIMessage = [...chatMessages].reverse().find(msg => msg.role === 'ai');
    
    if (!lastAIMessage) {
        showVoiceError('No AI response to read aloud.');
        return;
    }
    
    // Clean the text for speech (remove markdown and HTML)
    let textToSpeak = cleanTextForSpeech(lastAIMessage.content);
    
    // Create speech utterance
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    
    // Configure voice settings
    utterance.lang = currentLanguage;
    utterance.rate = 0.9; // Slightly slower for medical content
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    
    // Find appropriate voice for the language
    const voices = voiceSynthesis.getVoices();
    const preferredVoice = voices.find(voice => 
        voice.lang.startsWith(currentLanguage.split('-')[0]) && 
        (voice.name.includes('Female') || voice.name.includes('Google'))
    ) || voices.find(voice => voice.lang.startsWith(currentLanguage.split('-')[0]));
    
    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }
    
    // Event handlers
    utterance.onstart = function() {
        isSpeaking = true;
        updateVoiceUI('speaking');
        console.log('Started speaking');
    };
    
    utterance.onend = function() {
        isSpeaking = false;
        updateVoiceUI('idle');
        console.log('Finished speaking');
    };
    
    utterance.onerror = function(event) {
        isSpeaking = false;
        updateVoiceUI('idle');
        console.error('Speech synthesis error:', event.error);
        showVoiceError('Error reading text aloud: ' + event.error);
    };
    
    // Start speaking
    voiceSynthesis.speak(utterance);
}

function cleanTextForSpeech(text) {
    // Remove markdown formatting
    let cleaned = text
        .replace(/\*\*([^*]+)\*\*/g, '$1') // Bold
        .replace(/\*([^*]+)\*/g, '$1')     // Italic
        .replace(/#{1,6}\s/g, '')          // Headers
        .replace(/```[^`]*```/g, '')       // Code blocks
        .replace(/`([^`]+)`/g, '$1')       // Inline code
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Links
        .replace(/!\[([^\]]*)\]\([^)]+\)/g, '$1') // Images
        
        // Remove HTML tags
        .replace(/<[^>]*>/g, '')
        
        // Clean up special characters and emojis
        .replace(/[📋🔍🍎💪👨‍⚕️🎯❓💬🚨⚠️]/g, '')
        
        // Replace bullet points
        .replace(/•/g, '. ')
        
        // Clean up extra whitespace
        .replace(/\s+/g, ' ')
        .trim();
    
    // Add pauses for better speech flow
    cleaned = cleaned
        .replace(/\. /g, '. ... ') // Pause after sentences
        .replace(/: /g, ': ... ')  // Pause after colons
        .replace(/\n/g, ' ... ');  // Pause for line breaks
    
    return cleaned;
}

function updateLanguage() {
    const languageSelect = document.getElementById('voice-language');
    if (languageSelect) {
        currentLanguage = languageSelect.value;
        console.log('Language updated to:', currentLanguage);
        
        // Update recognition language if active
        if (voiceRecognition) {
            voiceRecognition.lang = currentLanguage;
        }
        
        // Show language change confirmation
        const langName = currentLanguage === 'en-US' ? 'English' : 'हिंदी (Hindi)';
        showVoiceSuccess(`Language changed to ${langName}`);
    }
}

function updateVoiceUI(state) {
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const voiceInputText = document.getElementById('voice-input-text');
    const voiceOutputBtn = document.getElementById('voice-output-btn');
    const voiceOutputText = document.getElementById('voice-output-text');
    const voiceStatus = document.getElementById('voice-status');
    
    // Reset classes
    if (voiceInputBtn) {
        voiceInputBtn.classList.remove('voice-btn-recording', 'voice-btn-speaking');
    }
    if (voiceOutputBtn) {
        voiceOutputBtn.classList.remove('voice-btn-speaking');
    }
    
    switch(state) {
        case 'recording':
            if (voiceInputBtn && voiceInputText) {
                voiceInputBtn.classList.add('voice-btn-recording');
                voiceInputText.innerHTML = '<i class="fas fa-stop mr-2"></i>Stop';
            }
            if (voiceStatus) {
                voiceStatus.classList.remove('hidden');
                voiceStatus.classList.add('voice-status-listening');
            }
            updateVoiceStatus('Listening... Speak now!');
            break;
            
        case 'speaking':
            if (voiceOutputBtn && voiceOutputText) {
                voiceOutputBtn.classList.add('voice-btn-speaking');
                voiceOutputText.innerHTML = '<i class="fas fa-stop mr-2"></i>Stop Reading';
            }
            break;
            
        case 'idle':
        default:
            if (voiceInputBtn && voiceInputText) {
                voiceInputText.innerHTML = '<i class="fas fa-microphone mr-2"></i>Speak';
            }
            if (voiceOutputBtn && voiceOutputText) {
                voiceOutputText.innerHTML = '<i class="fas fa-volume-up mr-2"></i>Read Aloud';
            }
            if (voiceStatus) {
                voiceStatus.classList.add('hidden');
                voiceStatus.classList.remove('voice-status-listening', 'voice-status-processing');
            }
            break;
    }
}

function updateVoiceStatus(message) {
    const voiceStatusText = document.getElementById('voice-status-text');
    if (voiceStatusText) {
        voiceStatusText.textContent = message;
    }
}

function showVoiceError(message, solution) {
    console.error('Voice error:', message);
    
    // Create detailed error message
    let fullMessage = `🎤 ${message}`;
    if (solution) {
        fullMessage += `\n\n💡 Solution: ${solution}`;
    }
    
    // Add error message to chat
    if (chatMessages) {
        chatMessages.push({
            role: 'system',
            content: fullMessage,
            timestamp: new Date()
        });
        displayChatMessages();
    }
    
    // Show temporary notification
    showVoiceNotification(message, 'error');
}

function showVoiceSuccess(message) {
    console.log('Voice success:', message);
    showVoiceNotification(message, 'success');
}

function showVoiceNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-20 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
    
    if (type === 'error') {
        notification.className += ' bg-red-600 text-white';
    } else {
        notification.className += ' bg-green-600 text-white';
    }
    
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} mr-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Animate out and remove
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Load voices when they become available
if ('speechSynthesis' in window) {
    speechSynthesis.onvoiceschanged = function() {
        console.log('Voices loaded:', speechSynthesis.getVoices().length);
    };
}

// Export voice functions for global access
window.toggleVoiceInput = toggleVoiceInput;
window.readLastAIResponse = readLastAIResponse;
window.stopVoiceInput = stopVoiceInput;
// Function to read a specific message by timestamp
function readSpecificMessage(timestamp) {
    if (!voiceSynthesis) {
        showVoiceError('Text-to-speech not available in your browser.');
        return;
    }
    
    // Find the message by timestamp
    const message = chatMessages.find(msg => msg.timestamp.toString() === timestamp);
    
    if (!message) {
        showVoiceError('Message not found.');
        return;
    }
    
    // Stop any current speech
    voiceSynthesis.cancel();
    
    // Clean the text for speech
    let textToSpeak = cleanTextForSpeech(message.content);
    
    // Create speech utterance
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    
    // Configure voice settings
    utterance.lang = currentLanguage;
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    
    // Find appropriate voice
    const voices = voiceSynthesis.getVoices();
    const preferredVoice = voices.find(voice => 
        voice.lang.startsWith(currentLanguage.split('-')[0]) && 
        (voice.name.includes('Female') || voice.name.includes('Google'))
    ) || voices.find(voice => voice.lang.startsWith(currentLanguage.split('-')[0]));
    
    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }
    
    // Event handlers
    utterance.onstart = function() {
        console.log('Started reading specific message');
    };
    
    utterance.onend = function() {
        console.log('Finished reading specific message');
    };
    
    utterance.onerror = function(event) {
        console.error('Speech synthesis error:', event.error);
        showVoiceError('Error reading message: ' + event.error);
    };
    
    // Start speaking
    voiceSynthesis.speak(utterance);
}

// Export for global access
window.readSpecificMessage = readSpecificMessage;