"""
Example usage of the Polls API
This file demonstrates how to interact with the API
"""

import requests

BASE_URL = "http://localhost:5000/api"

# Example 1: Register a user
def register_user(username, password):
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "password": password
    })
    return response.json()

# Example 2: Login
def login(username, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": username,
        "password": password
    })
    return response.json()

# Example 3: Create a poll (requires authentication)
def create_poll(token, question, is_public=True, requires_admin=False):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/polls", json={
        "question": question,
        "is_public": is_public,
        "requires_admin": requires_admin
    }, headers=headers)
    return response.json()

# Example 4: Vote on a poll
def vote_on_poll(poll_id, choice, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.post(f"{BASE_URL}/votes/poll/{poll_id}", json={
        "choice": choice
    }, headers=headers)
    return response.json()

# Example 5: Get votes for a poll
def get_votes(poll_id):
    response = requests.get(f"{BASE_URL}/votes/poll/{poll_id}")
    return response.json()

if __name__ == "__main__":
    print("Example API usage:")
    print("1. Register: register_user('user1', 'password123')")
    print("2. Login: login('user1', 'password123')")
    print("3. Create poll: create_poll(token, 'What is your favorite color?')")
    print("4. Vote: vote_on_poll(1, 'Blue')")
    print("5. Get votes: get_votes(1)")

