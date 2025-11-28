#!/usr/bin/env python3
"""
Simple test - verify the backend can start and respond
"""

import subprocess
import time
import requests
import sys
import os

def test_backend():
    print("🧪 Testing Dashboard Backend")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Start server in background
    print("\n1. Starting backend server...")
    try:
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        print("   Waiting for server to start...")
        time.sleep(3)
        
        # Test endpoints
        base_url = "http://localhost:5001"
        
        print("\n2. Testing API endpoints...")
        
        # Health check
        try:
            response = requests.get(f"{base_url}/api/health", timeout=2)
            if response.status_code == 200:
                print("   ✅ Health endpoint: OK")
            else:
                print(f"   ❌ Health endpoint: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Health endpoint: {e}")
            print("   (Server might still be starting...)")
        
        # Depression endpoint
        try:
            response = requests.get(f"{base_url}/api/depression", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Depression endpoint: OK")
                print(f"      Score: {data.get('score', 'N/A')}")
                print(f"      Level: {data.get('emoji', '')} {data.get('level', 'N/A')}")
            else:
                print(f"   ❌ Depression endpoint: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Depression endpoint: {e}")
        
        # Teams endpoint
        try:
            response = requests.get(f"{base_url}/api/teams", timeout=2)
            if response.status_code == 200:
                data = response.json()
                teams = data.get('teams', [])
                print(f"   ✅ Teams endpoint: OK ({len(teams)} teams)")
            else:
                print(f"   ❌ Teams endpoint: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Teams endpoint: {e}")
        
        print("\n" + "=" * 60)
        print("✅ Backend test complete!")
        print("\nTo keep the server running:")
        print("  cd backend && python3 app.py")
        print("\nThen in another terminal:")
        print("  cd frontend && npm install && npm run dev")
        print("=" * 60)
        
        # Clean up
        process.terminate()
        process.wait(timeout=2)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_backend()

