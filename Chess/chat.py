import openai
from credentials import OPENAI_API_KEY

# Set your API key
openai.api_key = OPENAI_API_KEY

# Start a chat session
chat_session = [
  {
    "role": "system",
    "content": "THIS IS NOT A CONVERSATION. YOU ARE ALONE. YOU ARE INTERFACING WITH A CHESS GAME."
  },
  {
    "role": "system",
    "content": """YOU WILL ALWAYS RESPOND WITH THE FOLLOWING SEQUENCE IN THE GIVEN ORDER:
1. SUMMARIZE THE STRONGEST PIECES IN THE POSITION (DO NOT REITERATE THE PGN)
2. SUMMARIZE POTENTIAL OPPONENT INTENTIONS
3. MAKE A MOVE AND EXPLAIN WHY YOU'RE MAKING IT
4. GUESS YOUR OPPONENTS NEXT MOVE"""
  }
]

# Call the ChatCompletion endpoint
response = openai.ChatCompletion.create(
  model="my-model",
  messages=chat_session
)

# Print the assistant's reply
print(response['choices'][0]['message']['content'])

