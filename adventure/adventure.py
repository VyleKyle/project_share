import openai
import os
import credentials
import json


openai.api_key = credentials.openai



def gpt2json(messages):
    prompt = "".join([message['content'] for message in messages])  # Invalid prompt configuration.
    
    response = openai.ChatCompletion.create(
      model="gpt-4.0-turbo",
      messages=[  # Messages are provided to the function, and then needlessly redefined here.
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    
    try:
        response_json = json.loads(response['choices'][0]['message']['content'])
        return response_json
    except json.JSONDecodeError:
        print("Invalid response from GPT:", response['choices'][0]['message']['content'])
        messages.append({"role": "system", "content": "Invalid response. Please try again."})
        return gpt2json(messages)


def trim_messages(messages, token_limit, beginning_messages_to_keep):
    # Separate the beginning and recent messages
    beginning_messages = messages[:beginning_messages_to_keep]
    recent_messages = messages[beginning_messages_to_keep:]
    
    # Count the total tokens in the recent messages
    total_tokens = sum([len(message['content']) for message in recent_messages])

    # Trim the recent messages until the total token count is under the limit
    while total_tokens > token_limit:
        # Remove the oldest recent message
        oldest_message = recent_messages.pop(0)

        # Subtract the length of the removed message from the total token count
        total_tokens -= len(oldest_message['content'])

    # Combine the beginning and recent messages and return
    return beginning_messages + recent_messages


# Step 1: Get the basic story details from the user
setting = input("Please describe the setting of your story: ")
characters = input("Please describe the main characters of your story: ")
plot = input("Please describe the basic plot of your story: ")  # Unused?

# Step 2: Generate the progression points
# Request the AI to generate encounters or events that mark story progression
progression_points = []

# The main game loop
for point in progression_points:
    # The AI generates a scenario based on the current progression point
    prompt = f"The story is set in {setting}. The main characters are {characters}. In the {point} of the story, "
    response = openai.ChatCompletion.create(
      model="gpt-4.0-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    print(response['choices'][0]['message']['content'])
    action = input("What do you do? ")
    
    # Now you can handle the user's action and determine the next scenario, and so on...



