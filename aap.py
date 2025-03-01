from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from openai import OpenAI
import os
import uvicorn
import logging

# Initialize FastAPI app

app = FastAPI()

# Load API Key
openai_api = os.environ.get("OPENAI_API_KEY")
client =OpenAI(api_key=openai_api)
if not openai_api:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
genai.configure(api_key=openai_api)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_details(user_complaint, model_name):
    """
    This function extracts information from a given user complaint using a specific LLM (Large Language Model).

    Parameters:
    user_complaint (str): The text of the user's complaint.
    model_name (str): The name of the specific LLM model to use for extraction.
    """

    system_content = """
        Given a customer complaint text, extract and return the following information in JSON (dict) format:
        - Topic
        - Problem
        - Customer_Dissatisfaction_Index
    """

    # Generate a response using the specified model and the user's complaint
    response = client.chat.completions.create(
        model = model_name,
        messages=[
            {"role": "system", "content": system_content},  # System content explaining the expected output
            {"role": "user", "content": user_complaint}  # User's complaint passed as content
        ]
    )

@app.get("/")
def home():
    return "FastAPI is runningggg!"

@app.post("/webhook")
async def webhook(From: str = Form(...), Body: str = Form(...)):
    logger.info(f"Received message from {From}: {Body}")

    # Initialize Twilio response
    twilio_response = MessagingResponse()

    try:
        # Generate response using Gemini
        model = genai.GenerativeModel("ft:gpt-3.5-turbo-0125:jamalnasir::B5xh9w1H")
        gemini_response = model.generate_content(
            f"You are a helpful assistant that provides information about Pakistan with character limit not exceeding 1000 characters. be focused and do not deviate  {Body}"
        )

        # Extract text response
        reply_text = gemini_response.text if hasattr(gemini_response, "text") else "I'm not sure how to respond."

    except Exception as e:
        logger.error(f"Error responding: {e}")
        reply_text = "Sorry, I couldn't process your request."

    # Send the reply back to WhatsApp
    twilio_response.message(reply_text)

    # Log the TwiML response
    logger.info(f"TwiML Response: {str(twilio_response)}")

    # Return the response with the correct Content-Type header
    return Response(content=str(twilio_response), media_type="text/xml")

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)