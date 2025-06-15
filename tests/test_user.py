import requests
import time

for i in range(20):
    requests.post("http://localhost:8000/users/", json={
        "name": f"user{i}",
        "email": f"user{i}@example.com",
        "phone": f"555-{i:04}"
    })
    requests.get("http://localhost:8000/users/")
    time.sleep(1)
