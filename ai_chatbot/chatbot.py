import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response(user_message):
    system_prompt = """You are TripWise AI, a smart and friendly travel expense assistant built into the TripWise app.
You help with expense splitting, trip budgeting, payment settlements, and travel money tips.
Always be friendly, use simple English or Hinglish, keep responses short with emojis and clear calculations using rupee symbol."""

    full_prompt = f"{system_prompt}\n\nUser: {user_message}\nAssistant:"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"Sorry, error: {str(e)}"

if __name__ == "__main__":
    print("TripWise AI ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply = get_ai_response(user_input)
        print(f"AI: {reply}\n")