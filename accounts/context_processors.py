from .models import Course, Enrollment


def notifications(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {"notifications": [], "notif_count": 0}
    items = []
    enrollments = (
        Enrollment.objects.filter(user=user)
        .select_related("course")
        .order_by("-updated_at")[:5]
    )
    for e in enrollments:
        if e.status == "completed":
            items.append({
                "kind": "done",
                "title": "Course completed",
                "text": e.course.title,
                "when": e.updated_at,
                "course_id": e.course_id,
            })
        else:
            items.append({
                "kind": "enrolled",
                "title": "You're enrolled",
                "text": e.course.title,
                "when": e.enrolled_at,
                "course_id": e.course_id,
            })
    enrolled_ids = set(
        Enrollment.objects.filter(user=user).values_list("course_id", flat=True)
    )
    for c in Course.objects.filter(is_new=True).order_by("-created_at")[:3]:
        if c.id not in enrolled_ids:
            items.append({
                "kind": "new",
                "title": "New class",
                "text": c.title,
                "when": c.created_at,
                "course_id": c.id,
            })
    items.sort(key=lambda x: x["when"], reverse=True)
    items = items[:6]
    return {"notifications": items, "notif_count": len(items)}
