import requests
from openai import api

class JumpCloudPlugin(api.Plugin):
    def handle_message(self, message: api.Message) -> api.Response:
        # Extracting the command from the message
        command = message.content.get('command')
        
        # Check if command is defined, if not return an error message
        if not command:
            return api.Response.create(error="Command not defined")

        # Define JumpCloud's API endpoint
        api_endpoint = "https://console.jumpcloud.com/api/insights/v1"

        # Define your JumpCloud API Key
        api_key = "Your_API_Key"

        # Define the headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": api_key
        }

        # Make the API request
        response = requests.get(f"{api_endpoint}/{command}", headers=headers)
        
        # Check if the request was successful, if not return an error message
        if response.status_code != 200:
            return api.Response.create(error="API request failed")

        # Return the data from the API request
        return api.Response.create(content=response.json())
