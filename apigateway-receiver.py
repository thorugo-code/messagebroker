import requests
import json


def get_messages_and_save_to_json():
    url = "https://qzr6ct4n50.execute-api.us-east-1.amazonaws.com/QualityReceiver"

    # Make a GET request to retrieve messages
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Convert the response content to JSON
        messages = response.json()

        # Save the messages to a JSON file
        with open('received_messages.json', 'w') as file:
            json.dump(messages, file, indent=4)

        print("Messages received successfully and saved to 'received_messages.json' file.")
    else:
        print(f"Failed to retrieve messages. Status code: {response.status_code}")


if __name__ == "__main__":
    get_messages_and_save_to_json()
