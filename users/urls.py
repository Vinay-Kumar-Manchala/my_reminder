from . import views
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("login", views.login, name="Login"),
    path('', views.add_new_user, name="home"),
    path("add_job", views.add_job, name="add_job"),
    path("success", views.success, name="success"),
    path("show_jobs", views.show_jobs, name="show_jobs"),
    path("author", views.fetch_author_data, name="author"),
    path("submit_job", views.submit_job, name="submit_job"),
    path("delete_job", views.job_delete, name="delete_job"),
    path("signup", views.sign_up_form, name="get login form"),
    path("login-form", views.get_login_form, name="login-form"),
    path("user_options", views.user_options, name="user_options"),
    path("create-user", views.create_user, name="creating a user"),
    path('scheduled_jobs', views.scheduled_jobs, name="scheduled_jobs"),
    path("validate_mail", views.mail_validation, name="mail validation"),
    path("verify_email_link", views.verify_email_link, name="Link verification"),
]

urlpatterns += staticfiles_urlpatterns()