#!/usr/bin/env python3
"""
Generate self-signed SSL certificate for local development
This allows HTTPS on localhost for voice features
"""

import os
import sys

def generate_certificate():
    """Generate self-signed SSL certificate using OpenSSL"""
    
    print("🔐 Generating SSL certificate for HTTPS...")
    print("=" * 60)
    
    # Check if OpenSSL is available
    if os.system("openssl version > /dev/null 2>&1") != 0:
        print("❌ OpenSSL not found!")
        print("\n📦 Please install OpenSSL:")
        print("   macOS: brew install openssl")
        print("   Windows: Download from https://slproweb.com/products/Win32OpenSSL.html")
        print("   Linux: sudo apt-get install openssl")
        return False
    
    # Generate private key and certificate
    cert_file = "localhost.pem"
    key_file = "localhost-key.pem"
    
    # Check if files already exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"✅ Certificate files already exist:")
        print(f"   - {cert_file}")
        print(f"   - {key_file}")
        return True
    
    print("\n📝 Generating certificate (this may take a moment)...")
    
    # Generate certificate valid for 365 days
    cmd = f"""openssl req -x509 -newkey rsa:4096 -nodes \
        -out {cert_file} \
        -keyout {key_file} \
        -days 365 \
        -subj "/C=IN/ST=Delhi/L=Delhi/O=VitalLens/OU=Development/CN=localhost" \
        -addext "subjectAltName=DNS:localhost,DNS:127.0.0.1,IP:127.0.0.1" \
        2>/dev/null"""
    
    result = os.system(cmd)
    
    if result == 0 and os.path.exists(cert_file) and os.path.exists(key_file):
        print("\n✅ SSL Certificate generated successfully!")
        print(f"   - Certificate: {cert_file}")
        print(f"   - Private Key: {key_file}")
        print("\n⚠️  Browser Security Warning:")
        print("   Your browser will show a security warning because this is")
        print("   a self-signed certificate. This is normal for development.")
        print("\n   To proceed:")
        print("   1. Click 'Advanced' or 'Show Details'")
        print("   2. Click 'Proceed to localhost (unsafe)' or 'Accept Risk'")
        print("   3. This is safe for local development!")
        return True
    else:
        print("\n❌ Failed to generate certificate")
        print("   Please check OpenSSL installation")
        return False

if __name__ == "__main__":
    success = generate_certificate()
    
    if success:
        print("\n" + "=" * 60)
        print("🚀 Next Steps:")
        print("=" * 60)
        print("1. Run: python start_vitallens_https.py")
        print("2. Open: https://localhost:5001/ai-chat.html")
        print("3. Accept the security warning (safe for local dev)")
        print("4. Click 'Speak' and allow microphone access")
        print("5. Voice features will now work! 🎤")
        print("=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)
