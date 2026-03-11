import requests

EMAIL_SERVICE_URL = "http://localhost:3000/dev/email/send"


def send_email_notification(payload):
    try:
        response = requests.post(
            EMAIL_SERVICE_URL,
            json=payload,
            timeout=5
        )
        return response.json()
    except Exception as e:
        print("Email service error:", e)
        return None