import os
from twilio.rest import Client
import dotenv

# Twilio credentials (store them securely as environment variables)
account_sid = os.environ.get("SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

print(account_sid)
print(auth_token)


client = Client(account_sid, auth_token)



from_whatsapp_number = "whatsapp:+14155238886"  # No space after "whatsapp:"
to_whatsapp_number = os.environ.get("MY_WHATSAPP_NUMBER")
print(to_whatsapp_number)

## function starts here 

if to_whatsapp_number:
    message = client.messages.create(
        body="Ahoy World",
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    print(f"Message sent successfully! SID: {message.sid}")
else:
    print("Error: MY_WHATSAPP_NUMBER environment variable is not set.")
