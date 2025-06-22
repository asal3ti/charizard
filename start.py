#!/usr/bin/env python3
"""
Startup script for YouTube Analytics AI System
"""

import os
import sys
import subprocess
import time
import requests
from dotenv import load_dotenv

def check_ollama():
    """Check if Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama if not running."""
    print("🤖 Starting Ollama...")
    try:
        # Start Ollama in background
        subprocess.Popen(["ollama", "serve"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait for Ollama to start
        for i in range(30):  # Wait up to 30 seconds
            if check_ollama():
                print("✅ Ollama started successfully")
                return True
            time.sleep(1)
        
        print("❌ Ollama failed to start")
        return False
        
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first:")
        print("   curl -fsSL https://ollama.ai/install.sh | sh")
        return False

def check_model():
    """Check if required model is available."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            # Check for Gemma3 specifically
            if 'gemma3' in model_names:
                print(f"✅ Found Gemma3 model")
                return True
            
            # Check for other common models as fallback
            for model in ['llama2', 'mistral', 'codellama']:
                if model in model_names:
                    print(f"⚠️  Found model: {model} (Gemma3 recommended)")
                    return True
            
            print("⚠️  No models found. Available models:", model_names)
            return False
    except:
        return False

def download_model():
    """Download Gemma3 model if none available."""
    print("📥 Downloading Gemma3 model...")
    try:
        subprocess.run(["ollama", "pull", "gemma3"], check=True)
        print("✅ Gemma3 model downloaded successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to download Gemma3 model")
        return False

def check_env():
    """Check environment variables."""
    load_dotenv()
    
    if not os.getenv('YOUTUBE_API_KEY'):
        print("❌ YOUTUBE_API_KEY not found in .env file")
        print("   Please create a .env file with your YouTube API key")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Main startup function."""
    print("🚀 YouTube Analytics AI System - Startup")
    print("=" * 50)
    
    # Check environment
    if not check_env():
        sys.exit(1)
    
    # Check/start Ollama
    if not check_ollama():
        if not start_ollama():
            sys.exit(1)
    
    # Check/download model
    if not check_model():
        if not download_model():
            print("⚠️  No models available. Please download Gemma3 manually:")
            print("   ollama pull gemma3")
            print("   or other models:")
            print("   ollama pull llama2")
            print("   ollama pull mistral")
    
    # Start the Flask app
    print("\n🌐 Starting Flask server...")
    try:
        subprocess.run([sys.executable, "src/app.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

if __name__ == "__main__":
    main() 