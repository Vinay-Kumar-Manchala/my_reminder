import uuid
import datetime
import urllib.parse
from logMaker.log import logger
from .models import Jobs, Accounts
from django.contrib import messages
from django.shortcuts import render
from common_utilities.mailer import SmtpMailer
from rest_framework.decorators import api_view
from .validation.get_validated import Validator
from common_utilities.aes_encryption import AESCipher
from .constants import Templates, CommonConstants, Http


@api_view([Http.GET])
def add_new_user(request):
    try:
        return render(request, Templates.home)

    except Exception as e:
        logger.error(f"Error occurred in add_new_user due to {str(e)}")


@api_view([Http.GET])
def success(request):
    return render(request, Templates.success)


@api_view([Http.GET])
def scheduled_jobs(request):
    try:
        cookie = request.COOKIES.get('cookie', None)
        flag, email_id = Validator().cookie_validator(cookie) if cookie not in [None, ''] else False
        if flag:
            jobs_data = Jobs.objects.filter(email_id=email_id)
            return render(request, Templates.list_jobs,
                          {"people": jobs_data, CommonConstants.name: jobs_data[0].name if jobs_data else "-"})

        else:
            return render(request, Templates.invalid_session)

    except Exception as e:
        logger.error(f"Error occurred in scheduled_jobs due to {str(e)}")


@api_view([Http.POST])
def submit_job(request):
    try:
        input_data = request.data
        cookie = request.COOKIES.get('cookie', None)
        flag, email_id = Validator().cookie_validator(cookie) if cookie not in [None, ''] else False
        if flag and email_id.lower().strip() == input_data[CommonConstants.email_id].lower().strip():
            job_id = uuid.uuid4()
            Jobs.objects.create(job_id=job_id, name=input_data[CommonConstants.name],
                                email_id=input_data[CommonConstants.email_id], subject=input_data[CommonConstants.subject],
                                message=input_data[CommonConstants.message], created_at=datetime.datetime.now(),
                                cron_schedule=input_data[CommonConstants.schedule_time])
            add_cron(job_id=str(job_id), cron=input_data[CommonConstants.schedule_time])
            return render(request, Templates.success)

        else:
            return render(request, Templates.invalid_session)

    except Exception as e:
        logger.error(f"Error occurred in submit_job due to {str(e)}")
        return render(request, Templates.invalid_session)


@api_view([Http.GET])
def add_job(request):
    try:
        cookie = request.COOKIES.get('cookie', None)
        flag, _ = Validator().cookie_validator(cookie) if cookie not in [None, ''] else False
        if flag:
            return render(request, Templates.add_job)

        else:
            return render(request, Templates.invalid_session)

    except Exception as e:
        logger.error(f"Error occurred in add_job due to {e}")


@api_view([Http.POST])
def show_jobs(request):
    try:
        input_data = request.data
        jobs_data = Jobs.objects.filter(email_id=input_data[CommonConstants.email_id])
        return render(request, Templates.list_jobs, {"people": jobs_data, CommonConstants.name: jobs_data[0].name if jobs_data else "-"})

    except Exception as e:
        logger.error(f"Error occurred in show_jobs due to {e}")


@api_view([Http.GET])
def fetch_author_data(request):
    try:
        return render(request, Templates.author)

    except Exception as e:
        logger.error(f"Error occurred in fetch_author_data due to {e}")


@api_view([Http.POST])
def job_delete(request):
    try:
        input_json = request.data
        Jobs.objects.filter(job_id=input_json[CommonConstants.job_id]).delete()
        messages.success(request, 'Job deleted successfully.')
        return render(request, Templates.user_options)

    except Exception as e:
        logger.error(f"Error occurred in job_delete due to {e}")


@api_view([Http.GET])
def sign_up_form(request):
    try:
        return render(request, Templates.signup)

    except Exception as e:
        logger.error(f"Error occurred while validating the user mail due to {e}")
        return render(request, Templates.something_went_wrong)


@api_view([Http.GET])
def user_options(request):
    try:
        cookie = request.COOKIES.get('cookie', None)
        flag, email_id = Validator().cookie_validator(cookie) if cookie not in [None, ''] else False
        if flag and email_id not in ["", None]:
            return render(request, Templates.user_options)

        else:
            return render(request, Templates.invalid_session)

    except Exception as e:
        logger.error(f"Error occurred while validating the user mail due to {e}")
        return render(request, Templates.something_went_wrong)


@api_view([Http.POST])
def create_user(request):
    try:
        input_data = request.data
        if Accounts.objects.filter(email_id=input_data[CommonConstants.email_id]):
            return render(request, Templates.user_already_exists)

        else:
            encrypted_password = AESCipher(key="I Seek Vengeance").encrypt(input_data[CommonConstants.password])
            Accounts.objects.create(email_id=input_data[CommonConstants.email_id], name=input_data[CommonConstants.name],
                                    password=encrypted_password, created_at=datetime.datetime.now())
            return render(request, Templates.user_created)

    except Exception as e:
        logger.error(f"Exception occurred while creating user due to {e}")
        return render(request, Templates.something_went_wrong)


@api_view([Http.GET])
def get_login_form(request):
    return render(request, Templates.login)


@api_view([Http.GET])
def verify_email_link(request):
    try:
        email_id = request.GET.get(CommonConstants.email_id)
        cookie = request.GET.get('cookie')
        cookie = urllib.parse.unquote(cookie)
        if email_id not in [None, ""]:
            data = Accounts.objects.get(email_id=email_id)
            data.is_verified = 1
            data.save()

        render_obj = render(request, Templates.success)
        render_obj.set_cookie('cookie', cookie)
        return render_obj

    except Exception as e:
        logger.error(f"Error occurred while fetching login form due to {str(e)}")
        return render(request, Templates.something_went_wrong)


@api_view([Http.GET])
def mail_validation(request):
    try:
        cookie = request.COOKIES.get('cookie', None)
        flag, _ = Validator().cookie_validator(cookie) if cookie not in [None, ''] else False
        if flag:
            return render(request, Templates.notify_user_mail_verification)

        else:
            return render(request, Templates.invalid_session)

    except Exception as e:
        logger.error(f"Error occurred while fetching login form due to {str(e)}")
        return render(request, Templates.something_went_wrong)


@api_view([Http.POST])
def login(request):
    try:
        flag, message, resp = Validator().validate_login(request)
        if flag:
            user_data = Accounts.objects.filter(email_id=request.data["email"], is_verified=1)
            if user_data:
                render_result = render(request, Templates.user_options)

            else:
                SmtpMailer().verification_mail(email_id=request.data["email"], cookie=resp)
                render_result = render(request, Templates.notify_user_mail_verification)

        elif message == "password_mismatch":
            render_result = render(request, Templates.password_mismatch)

        else:
            render_result = render(request, Templates.user_does_not_exist)

        render_result.set_cookie('cookie', resp, max_age=3600)
        return render_result

    except Exception as e:
        logger.error(f"Error occurred while login in due to {str(e)}")
        return render(request, Templates.something_went_wrong)


def add_cron(job_id: str, cron: str):
    try:
        # path in VM
        # mounted with cron-vol docker volume
        with open(r'/var/spool/cron/crontabs/root', 'r') as cron_file:
            cron_contents = cron_file.read()
        cron_contents += f"\n{cron} /usr/local/bin/python3 /app/common_utilities/the_runner.py {job_id}\n \n"
        cron_contents += "\n"
        with open(r'/var/spool/cron/crontabs/root', 'w') as cron_file:
            cron_file.write(cron_contents)

    except Exception as e:
        logger.error(f"Error occurred while adding cron to the file due to {e}")

