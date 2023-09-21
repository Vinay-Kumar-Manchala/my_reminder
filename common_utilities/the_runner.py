import sys
from mailer import SmtpMailer
from postgres_utility import PostgresUtil


sql_obj = PostgresUtil()
mailer_obj = SmtpMailer()

job_argument = sys.argv[1]
jobs_data, _ = sql_obj.fetch_data_from_postgres(query=f"SELECT * FROM users_jobs WHERE job_id='{job_argument}'")
for each in jobs_data:
    email_id = each['email_id']
    subject = each['subject']
    message = each['message']
    mailer_obj = mailer_obj.send_email_to_user(receiver_email_list=[email_id], subject=subject, content=message)