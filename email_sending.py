import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = "onyxai.technology@gmail.com"
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login("onyxai.technology@gmail.com", "djffozbelobdlhiu")

        server.sendmail("onyxai.technology@gmail.com", receiver_email, msg.as_string())
        sending_status = f"Email has been sent to: {receiver_email}"

        print(sending_status)
        server.quit()
        return True
    except Exception:
        return False