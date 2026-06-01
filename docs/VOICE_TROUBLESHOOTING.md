# Voice Feature Troubleshooting Guide 🎤

## "service-not-allowed" Error - Quick Fix

### **Problem:**
The error "service-not-allowed" occurs because Web Speech API requires secure context (HTTPS) or proper localhost configuration.

### **✅ Solution 1: Use 127.0.0.1 Instead of localhost**

Instead of accessing:
```
http://localhost:5001/ai-chat.html
```

Use this URL:
```
http://127.0.0.1:5001/ai-chat.html
```

**Why this works:** Some browsers treat `127.0.0.1` differently than `localhost` for security permissions.

---

### **✅ Solution 2: Use Chrome or Edge (Recommended)**

**Best Browsers for Voice Features:**
1. **Google Chrome** ✅ (Best support)
2. **Microsoft Edge** ✅ (Best support)
3. **Safari** ⚠️ (Limited support)
4. **Firefox** ❌ (Poor speech recognition support)

**To switch browsers:**
1. Open Chrome or Edge
2. Go to: `http://127.0.0.1:5001/ai-chat.html`
3. Allow microphone permission when prompted

---

### **✅ Solution 3: Check Browser Permissions**

**Chrome/Edge:**
1. Click the 🔒 or ⓘ icon in the address bar
2. Find "Microphone" setting
3. Change to "Allow"
4. Refresh the page

**Safari:**
1. Go to Safari → Settings → Websites
2. Click "Microphone"
3. Find your site and set to "Allow"
4. Refresh the page

---

### **✅ Solution 4: Enable HTTPS (Advanced)**

If you need HTTPS for production, you can generate SSL certificates:

```bash
# Install mkcert (one-time setup)
brew install mkcert  # macOS
# or
choco install mkcert  # Windows

# Generate certificates
mkcert -install
mkcert localhost 127.0.0.1

# Update Flask to use HTTPS
# In api_server.py, change:
app.run(host='0.0.0.0', port=5001, 
        ssl_context=('localhost+1.pem', 'localhost+1-key.pem'))
```

Then access via: `https://localhost:5001/ai-chat.html`

---

## **Alternative: Text Input Always Works! ✍️**

**Remember:** Voice is an optional accessibility feature. You can always:
- ✅ Type your symptoms in the text box
- ✅ Upload medical documents
- ✅ Use "Read Aloud" for AI responses (text-to-speech works without microphone)

The AI works perfectly with text input - voice is just an added convenience!

---

## **Quick Test: Is Voice Working?**

### **Test 1: Check Browser Support**
Open browser console (F12) and type:
```javascript
'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
```
- **true** = Browser supports voice ✅
- **false** = Browser doesn't support voice ❌

### **Test 2: Check Microphone Access**
```javascript
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(() => console.log('✅ Microphone access granted'))
  .catch(err => console.log('❌ Microphone error:', err))
```

### **Test 3: Simple Voice Test**
1. Go to: https://www.google.com
2. Click the microphone icon in search box
3. Try speaking
4. If Google voice works, your setup is correct!

---

## **Common Issues & Fixes**

### **Issue: "Microphone not found"**
**Fix:**
- Check microphone is plugged in
- Check system sound settings
- Try a different USB port
- Restart browser

### **Issue: "Permission denied"**
**Fix:**
- Clear browser cache and cookies
- Reset site permissions
- Try incognito/private mode
- Check system privacy settings

### **Issue: "No speech detected"**
**Fix:**
- Speak louder and clearer
- Move closer to microphone
- Check microphone volume in system settings
- Test microphone in another app

### **Issue: Voice works but Hindi doesn't**
**Fix:**
- Hindi support varies by browser
- Chrome has best Hindi support
- Try English first to verify setup
- Check language is set to "हिंदी (Hindi)"

---

## **Recommended Setup for Best Experience**

### **Optimal Configuration:**
```
Browser:  Google Chrome (latest version)
URL:      http://127.0.0.1:5001/ai-chat.html
Language: English (en-US) or हिंदी (hi-IN)
Mic:      Built-in or USB microphone
```

### **Steps for First-Time Setup:**
1. ✅ Open Google Chrome
2. ✅ Navigate to `http://127.0.0.1:5001/ai-chat.html`
3. ✅ Click "Speak" button
4. ✅ Click "Allow" when prompted for microphone
5. ✅ Speak clearly: "I have a headache"
6. ✅ Watch text appear automatically
7. ✅ Click "Read Aloud" to test audio output

---

## **Still Having Issues?**

### **Fallback Options:**

1. **Use Text Input** ✍️
   - Type your symptoms in the text box
   - Works 100% of the time
   - No permissions needed

2. **Use Text-to-Speech Only** 🔊
   - Type your message
   - Click "Read Aloud" to hear AI response
   - Doesn't require microphone permission

3. **Try Different Device** 📱
   - Test on phone/tablet
   - Mobile browsers often have better voice support
   - Android Chrome works great

4. **Contact Support** 💬
   - Provide browser name and version
   - Share error message from console (F12)
   - Describe what happens when you click "Speak"

---

## **Technical Details**

### **Why This Error Happens:**

The Web Speech API has security restrictions:
- ✅ **HTTPS sites** - Always allowed
- ✅ **localhost/127.0.0.1** - Usually allowed
- ❌ **HTTP sites** - Often blocked
- ❌ **File:// protocol** - Always blocked

### **Browser Compatibility:**

| Browser | Speech Recognition | Text-to-Speech |
|---------|-------------------|----------------|
| Chrome  | ✅ Excellent      | ✅ Excellent   |
| Edge    | ✅ Excellent      | ✅ Excellent   |
| Safari  | ⚠️ Limited        | ✅ Good        |
| Firefox | ❌ Poor           | ✅ Good        |

### **Language Support:**

| Language | Recognition | Synthesis |
|----------|-------------|-----------|
| English  | ✅ Excellent | ✅ Excellent |
| Hindi    | ✅ Good      | ✅ Good      |

---

## **Summary: Quick Fixes**

1. **Try this URL:** `http://127.0.0.1:5001/ai-chat.html`
2. **Use Chrome or Edge browser**
3. **Allow microphone permission**
4. **If still fails, use text input** (works perfectly!)

**Remember:** Voice is optional! The AI works great with text input, and "Read Aloud" works without microphone access. 🎉

---

**Need Help?** Check the browser console (F12) for detailed error messages and share them for better troubleshooting!