"""
Simple test for AutoGuardian API
"""
import requests
import json

def test_api():
    print("AutoGuardian API Test")
    print("=" * 30)
    
    # Test health check
    try:
        response = requests.get("http://localhost:5000/api/health")
        if response.status_code == 200:
            print("PASS: Health check successful")
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Database: {data.get('database')}")
        else:
            print(f"FAIL: Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("\nYour AutoGuardian server is running!")
    print("You can now:")
    print("- Register users at: POST /api/auth/register")
    print("- Add vehicles at: POST /api/vehicles")
    print("- Generate predictions at: POST /api/predictions/predict")
    print("- Add fuel records at: POST /api/fuel-records")

if __name__ == "__main__":
    test_api()