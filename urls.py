
from django.urls import path
from . import views

app_name = "onlinecourse"

urlpatterns = [
    path(
        "course/<int:course_id>/",
        views.course_details,
        name="course_details"
    ),
    path(
        "submit/<int:course_id>/",
        views.submit,
        name="submit"
    ),
    path(
        "exam_result/<int:submission_id>/",
        views.show_exam_result,
        name="show_exam_result"
    ),
    path(
        "logout/",
        views.logout_user,
        name="logout"
    ),
]

