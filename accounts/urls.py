from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("contact/", views.contact_view, name="contact"),
    path("copyright/", views.copyright_view, name="copyright"),
    path("privacy/", views.privacy_view, name="privacy"),
    path("terms/", views.terms_view, name="terms"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("my/enrolled/", views.enrolled_view, name="enrolled"),
    path("my/completed/", views.completed_view, name="completed"),
    path("my/saved/", views.saved_view, name="saved"),
    path("my/profile/", views.profile_view, name="profile"),
    path("course/<int:course_id>/", views.course_detail_view, name="course_detail"),
    path("course/<int:course_id>/learn/", views.classroom_view, name="classroom"),
    path("course/<int:course_id>/learn/<int:lesson_id>/", views.classroom_view, name="classroom_lesson"),
    path("course/<int:course_id>/learn/<int:lesson_id>/toggle/", views.toggle_lesson_complete, name="toggle_lesson"),
    path("course/<int:course_id>/learn/<int:lesson_id>/complete/", views.complete_lesson_auto, name="complete_lesson"),
    path("course/<int:course_id>/enroll/", views.enroll_view, name="enroll_course"),
    path("course/<int:course_id>/complete/", views.complete_view, name="complete_course"),
    path("course/<int:course_id>/unenroll/", views.unenroll_view, name="unenroll_course"),
    path("course/<int:course_id>/toggle-save/", views.toggle_save_view, name="toggle_save"),
]
