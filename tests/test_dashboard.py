#!/usr/bin/env python3
"""
Quick test script to verify the dashboard backend is working
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:5001"
    
    print("Testing Dashboard API...")
    print("=" * 60)
    
    # Test health endpoint
    try:
        print("\n1. Testing /api/health...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        print("   Start it with: cd backend && python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test depression endpoint
    try:
        print("\n2. Testing /api/depression...")
        response = requests.get(f"{base_url}/api/depression", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Depression endpoint working")
            print(f"   Score: {data.get('score', 'N/A')}")
            print(f"   Level: {data.get('emoji', '')} {data.get('level', 'N/A')}")
            print(f"   Breakdown sources: {len(data.get('breakdown', {}))}")
        else:
            print(f"❌ Depression endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test teams endpoint
    try:
        print("\n3. Testing /api/teams...")
        response = requests.get(f"{base_url}/api/teams", timeout=5)
        if response.status_code == 200:
            data = response.json()
            teams = data.get('teams', [])
            print("✅ Teams endpoint working")
            print(f"   Found {len(teams)} teams")
            for team in teams[:3]:  # Show first 3
                print(f"   - {team.get('name')}: {team.get('record')} ({team.get('depression_points', 0):.1f} pts)")
        else:
            print(f"❌ Teams endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test recent games endpoint
    try:
        print("\n4. Testing /api/recent-games...")
        response = requests.get(f"{base_url}/api/recent-games", timeout=5)
        if response.status_code == 200:
            data = response.json()
            games = data.get('games', [])
            print("✅ Recent games endpoint working")
            print(f"   Found {len(games)} recent games")
        else:
            print(f"❌ Recent games endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All API endpoints working!")
    print("\nNext steps:")
    print("1. Keep backend running (cd backend && python app.py)")
    print("2. In another terminal: cd frontend && npm install && npm run dev")
    print("3. Open http://localhost:3000 in your browser")
    return True

if __name__ == "__main__":
    # Wait a moment for backend to start if it just started
    time.sleep(1)
    test_api()

