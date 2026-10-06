from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .forms import SignupForm, LoginForm
from .models import Course, Enrollment, SavedCourse, Lesson, LessonProgress


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
    # lessons are created lazily per-course when classroom is opened


def ensure_course_lessons(course):
    # Heal legacy URLs (YouTube embeds or empty video for video-kind) to MP4 so JW Player can play them
    _fix_samples = [
        "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
    ]
    legacy_yt = Lesson.objects.filter(course=course, video_url__contains="youtube.com/embed")
    if legacy_yt.exists():
        for i, ls in enumerate(legacy_yt.order_by("section_order", "order")):
            ls.video_url = _fix_samples[i % len(_fix_samples)]
            ls.save(update_fields=["video_url"])
    legacy_empty = Lesson.objects.filter(course=course, kind="video", video_url="")
    if legacy_empty.exists():
        for i, ls in enumerate(legacy_empty.order_by("section_order", "order")):
            ls.video_url = _fix_samples[i % len(_fix_samples)]
            ls.save(update_fields=["video_url"])
    if Lesson.objects.filter(course=course).exists():
        return
    # Build a Coursera-like curriculum derived from course metadata
    total = course.lessons or 10
    # Split into 3 sections
    if total <= 6:
        splits = [2, 2, total - 4]
    elif total <= 9:
        splits = [3, 3, total - 6]
    else:
        splits = [4, 4, total - 8]
    splits = [s for s in splits if s > 0]
    titles_by_course = {
        "DaVinci": [
            "Welcome & Workspace Overview", "Importing & Organizing Media", "Basic Cuts & Timeline Tricks",
            "Color Page Fundamentals", "Nodes & Primary Correction", "Secondaries & Power Windows",
            "Fairlight Audio Mix", "Fusion Titles & Effects", "Delivery & Export Presets",
            "Project: Short Film Grade", "Review & Feedback Session", "Final Export & Portfolio"
        ],
        "Watercolor": [
            "Materials & Paper Guide", "Mixing & Color Theory", "Sketching Lightly",
            "First Wash Techniques", "Layering & Glazing", "Details & Texture",
            "Flowers & Botanicals", "Landscape Elements", "Final Artwork Session", "Scan & Share Your Work"
        ],
        "Python API": [
            "Project Setup & DRF Intro", "Models & Serializers", "ViewSets & Routing",
            "Authentication with JWT", "Permissions & Throttling", "Filtering, Search & Pagination",
            "Testing Your API", "Documentation with Swagger", "Deploying to Cloud",
            "OAuth & Security Hardening", "Caching & Performance", "Capstone: Production API",
            "CI/CD Pipeline", "Monitoring & Logs"
        ],
    }
    # Pick a pool based on title keyword or fallback to generic
    pool = None
    for key, lst in titles_by_course.items():
        if key.lower() in course.title.lower():
            pool = lst
            break
    if pool is None:
        pool = [
            "Course Overview & Goals", "Setting Up Your Workspace", "Core Concepts Explained",
            "Hands-on: First Exercise", "Deeper Dive & Best Practices", "Common Pitfalls",
            "Guided Practice Session", "Peer Review & Feedback", "Advanced Techniques",
            "Capstone Project Kickoff", "Build & Iterate", "Final Review & Next Steps",
            "Bonus: Tips from the Instructor", "Resources & Further Learning",
        ]
    sections = [
        ("Introduction & Foundations", "Get oriented and set up for success"),
        ("Core Skills & Techniques", "Master the essential tools and workflows"),
        ("Project & Mastery", "Apply everything in a real-world project"),
    ]
    # take as many sections as needed
    sections = sections[:len(splits)]
    # Generic durations rotation
    durations = ["4:12", "6:45", "8:02", "5:33", "7:18", "10:04", "3:55", "12:20", "9:11", "6:00", "11:33", "14:05", "5:47", "8:50"]
    kinds = ["video", "video", "video", "reading", "video", "video", "quiz"]
    idx = 0
    lesson_counter = 1
    for sec_idx, count in enumerate(splits):
        sec_title, sec_sub = sections[sec_idx]
        for j in range(count):
            title = pool[idx % len(pool)] if idx < len(pool) else f"Lesson {lesson_counter}: Deep Dive {lesson_counter}"
            idx += 1
            # JW Player needs a direct media file (MP4/HLS), not a YouTube embed.
            # Rotate a few public sample MP4s so every video lesson has a playable source.
            _samples = [
                "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
                "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
            ]
            is_video = not (lesson_counter % 5 == 0 and kinds[(lesson_counter - 1) % len(kinds)] != "video")
            # Recompute kind first
            kind_val = kinds[(lesson_counter - 1) % len(kinds)] if lesson_counter % 5 == 0 else "video"
            is_video = kind_val == "video"
            sample = _samples[(lesson_counter - 1) % len(_samples)]
            Lesson.objects.create(
                course=course,
                section=sec_title,
                section_order=sec_idx + 1,
                title=title,
                duration=durations[(lesson_counter - 1) % len(durations)],
                order=j + 1,
                kind=kind_val,
                description=f"In this lesson you'll learn {title.lower()}. Follow along with the instructor and practice at your own pace. Resources and notes are available below the player.",
                video_url=sample if is_video else "",
            )
            lesson_counter += 1


def ensure_all_lessons():
    ensure_demo_courses()
    for c in Course.objects.all():
        ensure_course_lessons(c)


def landing_view(request):
    if request.method == "POST":
        messages.success(request, "Subscrição confirmada! Bem-vindo à Academy.")
        return redirect("landing")
    ctx = _dashboard_context(
        request.user,
        request.GET.get("category") or None,
        request.GET.get("q") or None,
    )
    return render(request, "dashboard.html", ctx)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("landing")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Bem-vindo, {user.first_name}! A sua conta foi criada.")
        return redirect("landing")
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("landing")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        remember = form.cleaned_data.get("remember_me")
        login(request, user)
        if not remember:
            request.session.set_expiry(0)
        messages.success(request, f"Bem-vindo de volta, {user.first_name}!")
        return redirect("landing")
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


def _dashboard_context(user, category=None, query=None):
    ctx = _course_context(user)
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
    if not category and not query and getattr(user, "is_authenticated", False):
        inprog_ids = list(
            Enrollment.objects.filter(user=user, status="enrolled")
            .order_by("-updated_at")
            .values_list("course_id", flat=True)
        )
        if inprog_ids:
            order = {cid: i for i, cid in enumerate(inprog_ids)}
            inprog = [c for c in all_courses if c.id in order]
            inprog.sort(key=lambda c: order[c.id])
            sections.insert(0, {"title": "In Progress", "courses": inprog})
    ctx["sections"] = sections
    ctx["active_category"] = category
    ctx["query"] = query or ""
    ctx["bottom"] = "all"
    return ctx


def dashboard_view(request):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    qs = request.META.get("QUERY_STRING", "")
    url = reverse("landing") + (f"?{qs}" if qs else "")
    return HttpResponseRedirect(url)


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
    # Redirect old detail URL to the classroom (Coursera-style)
    return redirect("classroom", course_id=course_id)


@login_required
def classroom_view(request, course_id, lesson_id=None):
    ensure_demo_courses()
    course = get_object_or_404(Course, pk=course_id)
    ensure_course_lessons(course)
    course.tag_list_cached = course.tag_list()

    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    # Auto-enroll on first classroom visit (Coursera allows preview, but we enroll silently)
    if enrollment is None:
        enrollment = Enrollment.objects.create(user=request.user, course=course, status="enrolled", progress=0)

    lessons = list(Lesson.objects.filter(course=course).order_by("section_order", "order"))
    # Build sections grouping
    from collections import OrderedDict
    sections_dict = OrderedDict()
    for ls in lessons:
        if ls.section not in sections_dict:
            sections_dict[ls.section] = []
        sections_dict[ls.section].append(ls)
    sections = [{"title": k, "lessons": v} for k, v in sections_dict.items()]

    # Current lesson selection
    current = None
    if lesson_id is not None:
        current = next((l for l in lessons if l.id == lesson_id), None)
        if current is None:
            current = lessons[0] if lessons else None
    else:
        # try last unfinished, otherwise first
        completed_ids = set(LessonProgress.objects.filter(user=request.user, lesson__course=course, completed=True).values_list("lesson_id", flat=True))
        current = next((l for l in lessons if l.id not in completed_ids), lessons[0] if lessons else None)

    # Progress calculation based on completed lessons
    completed_ids = set(LessonProgress.objects.filter(user=request.user, lesson__course=course, completed=True).values_list("lesson_id", flat=True))
    total = len(lessons) or 1
    completed_count = len(completed_ids)
    pct = int(round(completed_count / total * 100))

    # Keep Enrollment.progress in sync
    if enrollment and enrollment.progress != pct:
        enrollment.progress = pct
        if pct == 100 and enrollment.status != "completed":
            enrollment.status = "completed"
        elif pct < 100 and enrollment.status == "completed":
            enrollment.status = "enrolled"
        enrollment.save(update_fields=["progress", "status", "updated_at"])

    # Prev/next navigation
    cur_idx = lessons.index(current) if current and current in lessons else 0
    prev_lesson = lessons[cur_idx - 1] if cur_idx > 0 else None
    next_lesson = lessons[cur_idx + 1] if cur_idx + 1 < len(lessons) else None

    # completed map
    completed_map = {lid: True for lid in completed_ids}

    ctx = _course_context(request.user)
    # hide sidebar categories in classroom? keep but not needed
    ctx.update({
        "course": course,
        "sections_data": sections,
        "lessons": lessons,
        "current": current,
        "completed_ids": completed_ids,
        "completed_map": completed_map,
        "progress_pct": pct,
        "completed_count": completed_count,
        "total_lessons": total,
        "prev_lesson": prev_lesson,
        "next_lesson": next_lesson,
        "enrollment": enrollment,
        "is_saved": SavedCourse.objects.filter(user=request.user, course=course).exists(),
        "bottom": "all",
    })
    return render(request, "classroom.html", ctx)


@login_required
@require_POST
def toggle_lesson_complete(request, course_id, lesson_id):
    """Legacy toggle — kept for backwards compat, now also supports auto-complete via fetch."""
    lesson = get_object_or_404(Lesson, pk=lesson_id, course_id=course_id)
    prog, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    # toggle
    if not created and prog.completed:
        prog.completed = False
        prog.save(update_fields=["completed", "updated_at"])
    else:
        prog.completed = True
        prog.save(update_fields=["completed", "updated_at"])
    lessons = Lesson.objects.filter(course_id=course_id)
    total = lessons.count() or 1
    done = LessonProgress.objects.filter(user=request.user, lesson__course_id=course_id, completed=True).count()
    pct = int(round(done / total * 100))
    enrollment = Enrollment.objects.filter(user=request.user, course_id=course_id).first()
    if enrollment:
        enrollment.progress = pct
        enrollment.status = "completed" if pct == 100 else "enrolled"
        enrollment.save(update_fields=["progress", "status", "updated_at"])
    # JSON for fetch (auto-complete)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", ""):
        from django.http import JsonResponse
        return JsonResponse({"ok": True, "progress": pct, "completed": prog.completed, "total": total, "done": done})
    nxt = request.POST.get("next_lesson")
    if nxt:
        return redirect("classroom_lesson", course_id=course_id, lesson_id=int(nxt))
    return redirect("classroom_lesson", course_id=course_id, lesson_id=lesson_id)


@login_required
@require_POST
def complete_lesson_auto(request, course_id, lesson_id):
    """Idempotent auto-complete — marks lesson as completed, never un-completes. Used by JW Player on('complete')."""
    lesson = get_object_or_404(Lesson, pk=lesson_id, course_id=course_id)
    prog, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson, defaults={"completed": True})
    if not created and not prog.completed:
        prog.completed = True
        prog.save(update_fields=["completed", "updated_at"])
    lessons = Lesson.objects.filter(course_id=course_id)
    total = lessons.count() or 1
    done = LessonProgress.objects.filter(user=request.user, lesson__course_id=course_id, completed=True).count()
    pct = int(round(done / total * 100))
    enrollment = Enrollment.objects.filter(user=request.user, course_id=course_id).first()
    if enrollment:
        enrollment.progress = pct
        enrollment.status = "completed" if pct == 100 else "enrolled"
        enrollment.save(update_fields=["progress", "status", "updated_at"])
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", ""):
        from django.http import JsonResponse
        return JsonResponse({"ok": True, "progress": pct, "completed": True, "total": total, "done": done})
    return redirect("classroom_lesson", course_id=course_id, lesson_id=lesson_id)


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
    nxt = request.POST.get("next", "landing")
    if nxt == "dashboard":
        nxt = "landing"
    return redirect((nxt if nxt in ("landing", "dashboard", "enrolled", "completed", "saved") else "landing"))


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
    return redirect((nxt if nxt in ("landing", "dashboard", "enrolled", "completed", "saved") else "enrolled"))


@login_required
@require_POST
def unenroll_view(request, course_id):
    Enrollment.objects.filter(user=request.user, course_id=course_id).delete()
    messages.info(request, "Enrollment removed.")
    nxt = request.POST.get("next", "enrolled")
    return redirect((nxt if nxt in ("landing", "dashboard", "enrolled", "completed", "saved") else "enrolled"))


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
    nxt = request.POST.get("next", "landing")
    if nxt == "dashboard":
        nxt = "landing"
    return redirect((nxt if nxt in ("landing", "dashboard", "enrolled", "completed", "saved") else "landing"))
