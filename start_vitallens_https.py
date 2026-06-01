#!/usr/bin/env python3
"""
VitalLens HTTPS Server Launcher
Starts the API server with HTTPS for voice features
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CERT_FILE = BASE_DIR / "localhost.pem"
KEY_FILE = BASE_DIR / "localhost-key.pem"
CERT_GENERATOR = BASE_DIR / "scripts" / "generate_ssl_cert.py"

def check_ssl_certificates():
    """Check if SSL certificates exist"""
    if not CERT_FILE.exists() or not KEY_FILE.exists():
        print("❌ SSL certificates not found!")
        print("\n🔐 Generating certificates...")
        result = subprocess.run([sys.executable, str(CERT_GENERATOR)], cwd=str(BASE_DIR))
        
        if result.returncode != 0:
            print("\n❌ Failed to generate certificates")
            print("Please run: python scripts/generate_ssl_cert.py")
            return False
    
    return True

def main():
    """Main function to start HTTPS server"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    VitalLens HTTPS Server                    ║
║              AI-Powered Medical Analysis Platform            ║
║                    with Voice Features 🎤                    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check SSL certificates
    if not check_ssl_certificates():
        return
    
    os.chdir(BASE_DIR)
    
    try:
        # Import Flask app
        from api_server import app
        
        print("📊 VitalLens is starting up with HTTPS...")
        print("🔐 Secure Web Interface: https://localhost:5001")
        print("🔗 API Documentation:")
        print("   - Health Check: https://localhost:5001/api/health")
        print("   - Model Status: https://localhost:5001/api/models/status")
        print("\n🎤 Voice Features: ENABLED")
        print("   - Speech-to-Text: ✅ Available")
        print("   - Text-to-Speech: ✅ Available")
        print("   - Languages: English & Hindi")
        print("\n⚠️  Browser Security Warning:")
        print("   Your browser will show a security warning.")
        print("   Click 'Advanced' → 'Proceed to localhost (unsafe)'")
        print("   This is safe for local development!")
        print("\n💡 The web interface will open automatically in your browser")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 62)
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('https://localhost:5001/ai-chat.html')
            except:
                pass
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the Flask app with HTTPS
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=False,
            ssl_context=(str(CERT_FILE), str(KEY_FILE))
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 VitalLens HTTPS Server stopped")
    except FileNotFoundError as e:
        print(f"\n❌ SSL certificate files not found: {e}")
        print("Please run: python scripts/generate_ssl_cert.py")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if port 5001 is available")
        print("   2. Verify SSL certificates exist (localhost.pem, localhost-key.pem)")
        print("   3. Try running: python scripts/generate_ssl_cert.py")
        print("   4. Check Python dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
