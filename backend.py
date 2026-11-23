
import ollama

# Model name
MODEL_NAME = "llama3.2:1b"


# Function to communicate with Ollama
def ask_ollama(messages):

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages
    )

    return response["message"]["content"]
