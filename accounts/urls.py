from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("my/enrolled/", views.enrolled_view, name="enrolled"),
    path("my/completed/", views.completed_view, name="completed"),
    path("my/saved/", views.saved_view, name="saved"),
    path("my/profile/", views.profile_view, name="profile"),
    path("course/<int:course_id>/", views.course_detail_view, name="course_detail"),
    path("course/<int:course_id>/enroll/", views.enroll_view, name="enroll_course"),
    path("course/<int:course_id>/complete/", views.complete_view, name="complete_course"),
    path("course/<int:course_id>/unenroll/", views.unenroll_view, name="unenroll_course"),
    path("course/<int:course_id>/toggle-save/", views.toggle_save_view, name="toggle_save"),
]
