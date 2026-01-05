import openai

openai.api_key = OPENAI_API_KEY
openai.base_url = OPENAI_BASE_URL


# Simple chat function
def chat(message: str, model: str = "gpt-4o", system_message: str = "You are a helpful assistant."):
    """
    Send a message to the chat model and get a response.
    
    Args:
        message: The user's message
        model: The model to use (e.g., gpt-4o, gpt-4, gpt-3.5-turbo)
        system_message: The system message to set the assistant's behavior
    
    Returns:
        The assistant's response text
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in chat: {e}")
        return None


# Example usage
if __name__ == "__main__":
    user_input = "What is a bluetooth lock and how does it work?"
    response = chat(user_input)
    if response:
        print(f"User: {user_input}")
        print(f"Assistant: {response}")