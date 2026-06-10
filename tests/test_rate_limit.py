import requests

API = "https://fishid.binhtvu.com"
IMAGE = "src/samples/trout.png"

print("Testing rate limit - sending 12 requests...")
for i in range(12):
    with open(IMAGE, "rb") as f:
        response = requests.post(f"{API}/predict", files={"file": f})
    print(f"Request {i+1}: {response.status_code} - {response.json()}")
    if response.status_code == 429:
        print("Rate limit hit as expected")
        break
