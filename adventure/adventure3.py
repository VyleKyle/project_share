import openai
import os
import credentials
import json
import logging

# Set up logging
logging.basicConfig(filename='text_adventure.log', level=logging.INFO)

openai.api_key = credentials.openai
model = 'gpt-4-0613'  # Note for GPT: Do not modify

def gpt2json(messages):
    # Request a completion from GPT
    response = openai.ChatCompletion.create(
      model=model,
      messages=messages  # Use the provided messages directly
    )
    
    # Try to parse the response as JSON
    try:
        response_json = json.loads(response['choices'][0]['message']['content'])
        return response_json
    except json.JSONDecodeError:
        logging.warning("Invalid response from GPT: %s", response['choices'][0]['message']['content'])
        messages.append({"role": "system", "content": "Invalid response. Please try again."})
        return gpt2json(messages)  # Recursive call should use the function's name

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
plot = input("Please describe the basic plot of your story: ")

logging.info("Starting story with setting: %s, characters: %s, plot: %s", setting, characters, plot)

# Step 2: Generate the progression points
# Request the AI to generate encounters or events that mark story progression
progression_points = gpt2json([
    {"role": "system", "content": "You are a dynamic storyteller, able to adapt the story based on the player's actions. Generate key points in the story for a player to navigate, and return them as a JSON-encoded list of strings."},
    {"role": "user", "content": f"SETTING:\n{setting}\nCHARACTERS:\n{characters}PLOT:\n{plot}\nGenerate the story progression points and return them as a JSON-encoded list of strings."},
])

logging.info("Generated progression points: %s", progression_points)

# The main game loop
for point in progression_points:
    # The AI generates a scenario based on the current progression point
    prompt = f"The story is set in {setting}. The main characters are {characters}. In the {point} of the story, "
    response = openai.ChatCompletion.create(
      model=model,
      messages=[
            {"role": "system", "content": "You are a dynamic storyteller, adapting the story based on the player's actions."},
            {"role": "user", "content": prompt},
        ]
    )
    print(response['choices'][0]['message']['content'])
    action = input("What do you do? ")
    
    logging.info("User action: %s", action)
    
    # Now you can handle the user's action and determine the next scenario, and so on...

