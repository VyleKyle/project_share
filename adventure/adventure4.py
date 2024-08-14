import openai
import json
import credentials

openai.api_key = credentials.openai
model = 'gpt-3.5-turbo-0613'

def manage_inventory(action, item, inventory):
    """Manage the player's inventory."""
    if action == "add":
        inventory.append(item)
    elif action == "remove" and item in inventory:
        inventory.remove(item)
    print("...?")
    return json.dumps(inventory)

def trim_messages(messages, token_limit, beginning_messages_to_keep):
    # Separate the beginning and recent messages
    beginning_messages = messages[:beginning_messages_to_keep]
    recent_messages = messages[beginning_messages_to_keep:]
    
    # Count the total tokens in the recent messages
    total_tokens = sum([len(message['content']) for message in recent_messages])/2

    # Trim the recent messages until the total token count is under the limit
    while total_tokens > token_limit:
        # Remove the oldest recent message
        oldest_message = recent_messages.pop(0)

        # Subtract the length of the removed message from the total token count
        total_tokens -= len(oldest_message['content'])

    # Combine the beginning and recent messages and return
    return beginning_messages + recent_messages

def run_adventure():
    # Initial setup
    setting = input("Please describe the setting of your story: ")
    characters = input("Please describe the main characters of your story: ")
    plot = input("Please describe the basic plot of your story: ")
    inventory = []  # Initial empty inventory for the player
    
    # Intended progression points can be set up here or requested from the model

    messages = [
        {"role": "system", "content": "You are a Dungeon Master guiding the player through a dynamic story."},
        {"role": "user", "content": f"Setting: {setting}. Characters: {characters}. Plot: {plot}. Begin the story."},
    ]

    functions = [
        {
            "name": "manage_inventory",
            "description": "Manage the player's inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["add", "remove"]},
                    "item": {"type": "string"},
                    "inventory": {
                        "type": "array",
                        "items": {"type": "string"}
                        }
                },
                "required": ["action", "item", "inventory"],
            }
        }
    ]

    while True:
        try:
            response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call="auto",
            )
        except openai.error.OpenAIError as e:
            #print(e)
            print("Error Details:", e.json_body)
        response_message = response["choices"][0]["message"]
        if response_message["content"] is None:
            print(response_message)
        print(response_message["content"])  # Display the AI's response to the user
        action = input("What do you do? ")  # Get the user's action
        
        # Append user's action to messages
        messages.append({"role": "user", "content": action})
        
        # Check if a function call is required
        if response_message.get("function_call"):
            print("Making call!")
            available_functions = {
                "manage_inventory": manage_inventory,
            }
            function_name = response_message["function_call"]["name"]
            fuction_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = fuction_to_call(
                action=function_args.get("action"),
                item=function_args.get("item"),
                inventory=function_args.get("inventory"),
            )

            # Update the inventory based on the function's response
            inventory = json.loads(function_response)
            
            # Append function response to messages
            messages.append({
                "role": "function",
                "name": function_name,
                "content": function_response,
            })

        # Trim messages to ensure they don't exceed token limit
        messages = trim_messages(messages, 4090, 5)  # Assuming a rough token limit

print(run_adventure())

