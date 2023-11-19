import requests
import json
import os
import streamlit_js_eval

# from dotenv import load_dotenv

# load_dotenv()

class Users:

#constants which are there throughout


    def __init__(self):
        # SECRETS_DIR = "secrets"
        # API_KEY_FILE = os.path.join(SECRETS_DIR, "firebase_api_key.txt")
        # with open(API_KEY_FILE, "r") as key_file:
        #     self.FIREBASE_API_KEY = key_file.read().strip()

        self.FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")



#helper funcs

    
    def login_user(self, email, password):
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }   
        
        LOGIN_ENDPOINT = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.FIREBASE_API_KEY}"
        response = requests.post(LOGIN_ENDPOINT, headers={"Content-Type": "application/json"}, json=payload)
        return response

    def signup_user(self, email, password, username):
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
            "displayName": username
        }
        SIGNUP_ENDPOINT = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.FIREBASE_API_KEY}"
        response = requests.post(SIGNUP_ENDPOINT, headers={"Content-Type": "application/json"}, json=payload)
        return response

    def save_into_database(self, username, email, local_id):
        data = {
                local_id: {
                    'handle_name': username,
                    'local_id': local_id,
                    'email_id':email
                    # Add other relevant data fields as needed
                }
            
        }
        DATABASE_URL = f"https://finsight-2023-default-rtdb.asia-southeast1.firebasedatabase.app"
        users_url = f"{DATABASE_URL}/users.json"
        response = requests.patch(users_url, json.dumps(data))

        if response.status_code == 200:
            return {"success": True, "message": "Data saved into the database successfully."}
        else:
            return {"success": False, "message": f"Error saving data to the database: {response.text}"}
        
    def get_user_data(self, local_id):
        
        DATABASE_URL = f"https://finsight-2023-default-rtdb.asia-southeast1.firebasedatabase.app"
        users_url = f"{DATABASE_URL}/users/{local_id}.json"
        response = requests.get(users_url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

#main funcs called in the frontend
    def login_section(self, email, password):
        try:
            response = self.login_user(email, password)
            response.raise_for_status()

            # Extract localId from the login response
            local_id = response.json().get("localId")

            # Fetch user data from the database
            user_data = self.get_user_data(local_id)

            if user_data:
                # Display the username upon successful login
                username = user_data.get('handle_name', 'Unknown Username')
                return {"success": True, "message": f"Login successful! Welcome, {username}."}
            else:
                return {"success": False, "message": "Error: User data not found."}
        except requests.exceptions.HTTPError as err:
            try:
                error_message = response.json()["error"]["message"]
                if "INVALID_EMAIL" in error_message or "INVALID_CREDENTIALS" in error_message:
                    return {"success": False, "message": "Error: INVALID_DETAILS"}
                else:
                    return {"success": False, "message": f"Error occurred: {error_message}"}
            except (KeyError, json.JSONDecodeError):
                return {"success": False, "message": "Error: Unable to parse error response."}


    

    def signup_section(self, email, password, handle_name):
        try:
            response = self.signup_user(email, password, handle_name)
            response.raise_for_status()

            # Extract localId from the signup response
            local_id = response.json().get("localId")

            # Save user data into the database
            save_result = self.save_into_database(handle_name, email, local_id)

            if save_result["success"]:
                return {"success": True, "message": "Sign up successful!", "localId": local_id}
            else:
                return {"success": False, "message": f"Error occurred during data storage: {save_result['message']}"}
        except requests.exceptions.HTTPError as err:
            try:
                error_message = response.json()["error"]["message"]
                return {"success": False, "message": f"Error occurred: {error_message}"}
            except (KeyError, json.JSONDecodeError):
                return {"success": False, "message": "Error: Unable to parse error response."}


