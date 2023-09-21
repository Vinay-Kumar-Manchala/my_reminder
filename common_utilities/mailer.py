#!/usr/bin/python3
import ssl
import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SmtpMailer:
    def __init__(self):
        self.email = "optimusprime7675@gmail.com"
        self.context = ssl.create_default_context()
        self.mail_server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context)
        self.mail_server.login(self.email, "pxgmpjecnereptya")

    def send_email_to_user(self, receiver_email_list, subject, content, cc_list=None):
        try:
            message = self.form_mime_multipart(receiver_email_list, cc_list, subject, content)
            self.send_mail_as_mime_message(message.as_string(), receiver_email_list)

        except Exception as e:
            print(f"Exception in send_email_to_user due to {e}")
        return True

    def send_mail_as_mime_message(self, message, receiver_email_list):
        try:
            self.mail_server.sendmail(from_addr=self.email, to_addrs=receiver_email_list,
                                      msg=message)
            return True

        except Exception as e:
            print(f"Exception occurred in send_mail_as_mime_message due to {str(e)}")
            return False

        finally:
            self.mail_server.quit()

    @staticmethod
    def form_mime_multipart(receiver_email, cc_list, subject, body):
        try:
            message = MIMEMultipart()
            message["From"] = "My Reminder"
            message["To"] = ",".join(receiver_email)
            message["Subject"] = subject
            if cc_list not in [None, []]:
                message["Cc"] = ",".join(cc_list)
            message.attach(MIMEText(body, "plain"))
            return message

        except Exception as e:
            print(f"Exception occurred in form_mime_multipart due to {str(e)}")

    def verification_mail(self, email_id, cookie):
        try:
            message = MIMEMultipart()
            cookie = urllib.parse.quote(cookie)
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head></head>
            <body>
                <h1>My Reminder: Email Verification</h1>
                <p>This email has been sent to verify your email address. Kindly click on the link below to verify your email:</p>
                <a href="http://34.100.243.227:8989/verify_email_link?email_id={email_id}&cookie={cookie}">Verify Email</a>
                <p>If the link doesn't work, you can copy and paste the following URL into your browser's address bar:</p>
                <p><code>http://34.100.243.227:8989/verify_email_link?email_id={email_id}&cookie={cookie}</code></p>
            </body>
            </html>
            """

            message.attach(MIMEText(html_content, "html"))
            message["From"] = "My Reminder"
            message["To"] = email_id
            message["Subject"] = "Mail Verification"
            message.attach(MIMEText(html_content, 'html'))
            self.send_mail_as_mime_message(message=message.as_string(), receiver_email_list=[email_id])

        except Exception as e:
            print(str(e))