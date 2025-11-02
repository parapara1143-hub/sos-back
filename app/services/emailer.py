from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..config import Config

def send_email(to, subject, html):
    api_key = Config().SENDGRID_API_KEY
    sender = Config().SENDGRID_FROM_EMAIL
    if not api_key or not sender:
        return False, "SENDGRID_API_KEY or FROM not configured"
    message = Mail(from_email=sender, to_emails=to, subject=subject, html_content=html or "")
    try:
        sg = SendGridAPIClient(api_key)
        resp = sg.send(message)
        return 200 <= resp.status_code < 300, resp.status_code
    except Exception as e:
        return False, str(e)
