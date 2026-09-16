from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .forms import SignupForm, LoginForm
from .models import Course, Enrollment, SavedCourse


CATEGORIES = [
    "AI & Innovation", "Animation & 3D", "Art & Illustration", "Crafts & DIY",
    "Creative Career", "Design", "Development", "Film & Video",
    "Home & Lifestyle", "Marketing & Business", "Music & Audio",
    "Personal Development", "Photography",
]

DEMO_COURSES = [
    {"title": "DaVinci Resolve 20 Masterclass: The Complete Video Editing & Color Grading Class", "instructor": "Adi Singh", "rating": 4.9, "reviews": 20, "duration": "6h 44m", "students": "7.6k", "level": "beginner", "tags": "DaVinci Resolve", "extra_tags": 11, "emoji": "🎬", "staff_pick": True, "category": "Film & Video", "role": "Video Editor & Colorist", "lessons": 12},
    {"title": "Watercolor Illustration: From Sketch to Final Artwork", "instructor": "Marta Silva", "rating": 4.8, "reviews": 134, "duration": "4h 20m", "students": "2.3k", "level": "beginner", "tags": "Illustration, Watercolor", "extra_tags": 4, "emoji": "🎨", "staff_pick": True, "category": "Art & Illustration", "role": "Illustrator", "lessons": 10},
    {"title": "Python API Development with Django Rest Framework", "instructor": "José Machava", "rating": 4.8, "reviews": 421, "duration": "18h 0m", "students": "1.2k", "level": "intermediate", "tags": "Python, Django", "extra_tags": 6, "emoji": "🐙", "staff_pick": True, "is_new": True, "category": "Development", "role": "Backend Developer", "lessons": 14},
    {"title": "AWS Cloud Practitioner: Deploy & Scale Your First App", "instructor": "Ana Costa", "rating": 4.6, "reviews": 89, "duration": "8h 10m", "students": "3.1k", "level": "beginner", "tags": "AWS, Cloud", "extra_tags": 3, "emoji": "☁️", "staff_pick": True, "category": "Home & Lifestyle", "role": "Cloud Engineer", "lessons": 9},
    {"title": "Intro to Machine Learning with Python: From Zero to Deployed Model", "instructor": "Lena Müller", "rating": 4.7, "reviews": 312, "duration": "12h 30m", "students": "5.8k", "level": "beginner", "tags": "Python, PyTorch", "extra_tags": 8, "emoji": "🤖", "is_new": True, "category": "AI & Innovation", "role": "Data Scientist", "lessons": 12},
    {"title": "API Security & OAuth 2.0 Deep Dive: Protect Your Backend", "instructor": "Sara Chen", "rating": 4.9, "reviews": 55, "duration": "10h 15m", "students": "920", "level": "advanced", "tags": "OAuth 2.0, JWT", "extra_tags": 5, "emoji": "🔐", "staff_pick": True, "category": "Development", "role": "Security Engineer", "lessons": 8},
    {"title": "Brand Identity Design: Logo Systems That Stand Out", "instructor": "Paula Reis", "rating": 4.7, "reviews": 203, "duration": "5h 30m", "students": "4.2k", "level": "intermediate", "tags": "Branding, Logo", "extra_tags": 4, "emoji": "✨", "category": "Design", "role": "Brand Designer", "lessons": 10},
    {"title": "Sourdough Baking at Home: From Starter to Perfect Loaf", "instructor": "Marco Tamele", "rating": 4.8, "reviews": 167, "duration": "3h 15m", "students": "2.8k", "level": "beginner", "tags": "Baking, Sourdough", "extra_tags": 2, "emoji": "🍞", "category": "Home & Lifestyle", "role": "Baker", "lessons": 8},
    {"title": "Music Production with Ableton: Make Your First Track", "instructor": "DJ Langa", "rating": 4.6, "reviews": 98, "duration": "7h 45m", "students": "1.9k", "level": "beginner", "tags": "Ableton, Mixing", "extra_tags": 5, "emoji": "🎧", "staff_pick": True, "category": "Music & Audio", "role": "Music Producer", "lessons": 11},
    {"title": "Portrait Photography: Light, Pose & Edit Like a Pro", "instructor": "Nina Petrova", "rating": 4.9, "reviews": 311, "duration": "6h 05m", "students": "6.4k", "level": "intermediate", "tags": "Photography, Lightroom", "extra_tags": 6, "emoji": "📷", "category": "Photography", "role": "Photographer", "lessons": 10},
    {"title": "Freelance Playbook: Get Clients & Raise Your Rates", "instructor": "Tomás Nhaca", "rating": 4.5, "reviews": 76, "duration": "4h 50m", "students": "1.5k", "level": "beginner", "tags": "Freelance, Business", "extra_tags": 3, "emoji": "💼", "category": "Marketing & Business", "role": "Business Coach", "lessons": 7},
    {"title": "Blender 3D: Model & Animate Your First Character", "instructor": "Ken Watanabe", "rating": 4.7, "reviews": 189, "duration": "9h 20m", "students": "3.7k", "level": "intermediate", "tags": "Blender, 3D", "extra_tags": 7, "emoji": "🧊", "is_new": True, "category": "Animation & 3D", "role": "3D Artist", "lessons": 12},
    {"title": "Morning Habits: Build Focus & Energy That Lasts", "instructor": "Aida Sitoe", "rating": 4.8, "reviews": 240, "duration": "2h 40m", "students": "8.1k", "level": "beginner", "tags": "Habits, Focus", "extra_tags": 2, "emoji": "🌅", "category": "Personal Development", "role": "Productivity Coach", "lessons": 6},
    {"title": "Hand Lettering for Beginners: Styles & Composition", "instructor": "Lisa Bardot", "rating": 4.9, "reviews": 151, "duration": "5h 57m", "students": "30.9k", "level": "beginner", "tags": "Lettering, Procreate", "extra_tags": 4, "emoji": "✍️", "staff_pick": True, "category": "Art & Illustration", "role": "Illustrator & Letterer", "lessons": 10},
    {"title": "Prompt Engineering: Get More from AI Assistants", "instructor": "Omar Ali", "rating": 4.6, "reviews": 112, "duration": "3h 30m", "students": "5.2k", "level": "intermediate", "tags": "AI, Prompts", "extra_tags": 3, "emoji": "💡", "is_new": True, "category": "AI & Innovation", "role": "AI Consultant", "lessons": 8},
]


def ensure_demo_courses():
    if Course.objects.exists():
        return
    for data in DEMO_COURSES:
        Course.objects.create(**data)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Bem-vindo, {user.first_name}! A sua conta foi criada.")
        return redirect("dashboard")
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        remember = form.cleaned_data.get("remember_me")
        login(request, user)
        if not remember:
            request.session.set_expiry(0)
        messages.success(request, f"Bem-vindo de volta, {user.first_name}!")
        return redirect("dashboard")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    messages.info(request, "Sessão terminada.")
    logout(request)
    return redirect("login")


def _course_context(user, category=None, query=None):
    ensure_demo_courses()
    courses = Course.objects.all().order_by("-created_at")
    if category:
        courses = courses.filter(category=category)
    if query:
        courses = courses.filter(title__icontains=query)
    if user.is_authenticated:
        enrolled_ids = set(Enrollment.objects.filter(user=user, status="enrolled").values_list("course_id", flat=True))
        completed_ids = set(Enrollment.objects.filter(user=user, status="completed").values_list("course_id", flat=True))
        saved_ids = set(SavedCourse.objects.filter(user=user).values_list("course_id", flat=True))
        enrollments = {e.course_id: e for e in Enrollment.objects.filter(user=user)}
    else:
        enrolled_ids, completed_ids, saved_ids, enrollments = set(), set(), set(), {}
    for c in courses:
        c.tag_list_cached = c.tag_list()
        c.is_enrolled = c.id in enrolled_ids
        c.is_completed = c.id in completed_ids
        c.is_saved = c.id in saved_ids
        c.enrollment = enrollments.get(c.id)
    return {
        "courses": courses,
        "categories": CATEGORIES,
        "active_category": category,
        "query": query or "",
        "enrolled_ids": enrolled_ids,
        "completed_ids": completed_ids,
        "saved_ids": saved_ids,
        "enrolled_count": len(enrolled_ids),
        "completed_count": len(completed_ids),
        "saved_count": len(saved_ids),
    }


PER_PAGE = 10


def _paginate(request, items):
    paginator = Paginator(items, PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    qs = params.urlencode()
    return page_obj, qs


@login_required
def dashboard_view(request):
    category = request.GET.get("category") or None
    query = request.GET.get("q") or None
    ctx = _course_context(request.user)
    all_courses = list(ctx["courses"])
    if category:
        all_courses = [c for c in all_courses if c.category == category]
        sections = [{"title": category, "courses": all_courses}]
    elif query:
        q = query.lower()
        found = [c for c in all_courses if q in c.title.lower()]
        sections = [{"title": f'Results for "{query}"', "courses": found}]
    else:
        new = [c for c in all_courses if c.is_new]
        trending = new + [c for c in all_courses if not c.is_new]
        sections = [{"title": "New and Trending", "courses": trending[:8]}]
        for cat in CATEGORIES:
            items = [c for c in all_courses if c.category == cat]
            if items:
                sections.append({"title": cat, "courses": items})
    ctx["sections"] = sections
    ctx["bottom"] = "all"
    return render(request, "dashboard.html", ctx)


@login_required
def enrolled_view(request):
    ctx = _course_context(request.user)
    ids = ctx["enrolled_ids"] | ctx["completed_ids"]
    ctx["courses"] = [c for c in ctx["courses"] if c.id in ids]
    ctx["page"] = "enrolled"
    ctx["page_title"] = "Enrolled"
    ctx["page_sub"] = "Courses you are currently learning and have finished."
    ctx["bottom"] = "enrolled"
    ctx["empty_msg"] = "You are not enrolled in any course yet."
    ctx["courses"], ctx["base_qs"] = _paginate(request, ctx["courses"])
    return render(request, "my_courses.html", ctx)


@login_required
def completed_view(request):
    ctx = _course_context(request.user)
    ctx["courses"] = [c for c in ctx["courses"] if c.id in ctx["completed_ids"]]
    ctx["page"] = "completed"
    ctx["page_title"] = "Completed"
    ctx["page_sub"] = "Courses you have finished. Well done!"
    ctx["bottom"] = "completed"
    ctx["empty_msg"] = "No completed courses yet. Finish a course to see it here."
    ctx["courses"], ctx["base_qs"] = _paginate(request, ctx["courses"])
    return render(request, "my_courses.html", ctx)


@login_required
def saved_view(request):
    ctx = _course_context(request.user)
    ctx["courses"] = [c for c in ctx["courses"] if c.id in ctx["saved_ids"]]
    ctx["page"] = "saved"
    ctx["page_title"] = "Saved"
    ctx["page_sub"] = "Your bookmarked courses. Watch them later."
    ctx["bottom"] = "saved"
    ctx["empty_msg"] = "No saved courses yet. Tap the bookmark icon on any course."
    ctx["courses"], ctx["base_qs"] = _paginate(request, ctx["courses"])
    return render(request, "my_courses.html", ctx)


import re as _re


def _time_left(duration, progress):
    m = _re.match(r"(?:(\d+)h\s*)?(?:(\d+)m)?", duration or "")
    if not m:
        return ""
    total = int(m.group(1) or 0) * 60 + int(m.group(2) or 0)
    left = round(total * (100 - (progress or 0)) / 100)
    if left <= 0:
        return ""
    h, mn = divmod(left, 60)
    return f"{h}h {mn}m left" if h else f"{mn}m left"


@login_required
def course_detail_view(request, course_id):
    ensure_demo_courses()
    course = get_object_or_404(Course, pk=course_id)
    course.tag_list_cached = course.tag_list()
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    course.enrollment = enrollment
    course.is_enrolled = enrollment is not None and enrollment.status == "enrolled"
    course.is_completed = enrollment is not None and enrollment.status == "completed"
    course.is_saved = SavedCourse.objects.filter(user=request.user, course=course).exists()
    progress = enrollment.progress if enrollment else 0
    ctx = _course_context(request.user)
    picks = [c for c in ctx["courses"] if c.id != course.id]
    same = [c for c in picks if c.category == course.category]
    others = [c for c in picks if c.category != course.category]
    ctx.update({
        "course": course,
        "progress": progress,
        "time_left": _time_left(course.duration, progress),
        "picks": (same + others)[:10],
        "bottom": "all",
    })
    return render(request, "course_detail.html", ctx)


@login_required
def profile_view(request):
    ctx = _course_context(request.user)
    ctx["bottom"] = "profile"
    return render(request, "profile.html", ctx)


@login_required
@require_POST
def enroll_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course, defaults={"status": "enrolled"}
    )
    if created:
        messages.success(request, f"You are now enrolled in '{course.title[:50]}'.")
    nxt = request.POST.get("next", "dashboard")
    return redirect(nxt if nxt in ("dashboard", "enrolled", "completed", "saved") else "dashboard")


@login_required
@require_POST
def complete_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    enrollment.status = "completed"
    enrollment.progress = 100
    enrollment.save()
    messages.success(request, f"Course '{course.title[:50]}' marked as completed.")
    nxt = request.POST.get("next", "enrolled")
    return redirect(nxt if nxt in ("dashboard", "enrolled", "completed", "saved") else "enrolled")


@login_required
@require_POST
def unenroll_view(request, course_id):
    Enrollment.objects.filter(user=request.user, course_id=course_id).delete()
    messages.info(request, "Enrollment removed.")
    nxt = request.POST.get("next", "enrolled")
    return redirect(nxt if nxt in ("dashboard", "enrolled", "completed", "saved") else "enrolled")


@login_required
@require_POST
def toggle_save_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    obj, created = SavedCourse.objects.get_or_create(user=request.user, course=course)
    if not created:
        obj.delete()
        messages.info(request, "Removed from saved courses.")
    else:
        messages.success(request, "Course saved for later.")
    nxt = request.POST.get("next", "dashboard")
    return redirect(nxt if nxt in ("dashboard", "enrolled", "completed", "saved") else "dashboard")
