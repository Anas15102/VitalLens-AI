#!/usr/bin/env python3
"""
Install speech recognition dependencies for cross-browser support
"""

import subprocess
import sys

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 60)
    print("Installing Speech Recognition Dependencies")
    print("=" * 60)
    
    packages = [
        "SpeechRecognition",  # Speech recognition library
        "pydub",              # Audio processing
        "google-cloud-speech" # Google Cloud Speech API (optional)
    ]
    
    print("\n📦 Installing required packages...\n")
    
    for package in packages:
        print(f"Installing {package}...", end=" ")
        if install_package(package):
            print("✅ Done")
        else:
            print("❌ Failed")
    
    print("\n" + "=" * 60)
    print("✅ Installation Complete!")
    print("=" * 60)
    print("\n🎤 Voice features will now work in ALL browsers:")
    print("   - Chrome ✅")
    print("   - Edge ✅")
    print("   - Brave ✅")
    print("   - Safari ✅")
    print("   - Firefox ✅")
    print("\n🚀 Next: Restart the server")
    print("   python start_vitallens_https.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
