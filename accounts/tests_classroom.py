from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Course, Lesson, LessonProgress, Enrollment
from accounts.views import ensure_course_lessons, ensure_demo_courses

User = get_user_model()


class ClassroomTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="test@example.com", password="testpass123", first_name="Test", last_name="User")
        ensure_demo_courses()
        self.course = Course.objects.first()
        ensure_course_lessons(self.course)

    def test_ensure_course_lessons_creates_expected_count(self):
        lessons = Lesson.objects.filter(course=self.course)
        self.assertEqual(lessons.count(), self.course.lessons)
        # sections grouping
        sections = set(lessons.values_list("section", flat=True))
        self.assertGreaterEqual(len(sections), 2)

    def test_ensure_course_lessons_idempotent(self):
        before = Lesson.objects.filter(course=self.course).count()
        ensure_course_lessons(self.course)
        after = Lesson.objects.filter(course=self.course).count()
        self.assertEqual(before, after)

    def test_course_detail_redirects_to_classroom(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("course_detail", args=[self.course.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(f"/course/{self.course.id}/learn/", resp.url)

    def test_classroom_requires_login(self):
        resp = self.client.get(reverse("classroom", args=[self.course.id]))
        # should redirect to login
        self.assertEqual(resp.status_code, 302)
        self.assertIn("login", resp.url)

    def test_classroom_renders_left_and_player(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("classroom", args=[self.course.id]))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        # left: course content
        self.assertIn("Course content", content)
        # right: player
        self.assertIn("player", content.lower())
        # lessons listed - check first word to avoid html escaping
        first_lesson = Lesson.objects.filter(course=self.course).first()
        self.assertIn(first_lesson.title.split()[0], content)

    def test_classroom_lesson_selection(self):
        self.client.force_login(self.user)
        lessons = list(Lesson.objects.filter(course=self.course).order_by("section_order", "order"))
        target = lessons[2]
        resp = self.client.get(reverse("classroom_lesson", args=[self.course.id, target.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(target.title.split()[0], resp.content.decode())
        self.assertIn("automatically", resp.content.decode().lower())

    def test_toggle_lesson_complete_updates_progress(self):
        self.client.force_login(self.user)
        lesson = Lesson.objects.filter(course=self.course).first()
        # visit classroom to auto-enroll
        self.client.get(reverse("classroom", args=[self.course.id]))
        enrollment = Enrollment.objects.get(user=self.user, course=self.course)
        self.assertEqual(enrollment.progress, 0)
        # toggle complete
        resp = self.client.post(reverse("toggle_lesson", args=[self.course.id, lesson.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(LessonProgress.objects.filter(user=self.user, lesson=lesson, completed=True).exists())
        enrollment.refresh_from_db()
        self.assertGreater(enrollment.progress, 0)
        # toggle back
        self.client.post(reverse("toggle_lesson", args=[self.course.id, lesson.id]))
        self.assertFalse(LessonProgress.objects.filter(user=self.user, lesson=lesson, completed=True).exists())

    def test_dashboard_links_point_to_classroom(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("landing"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        # should contain classroom learn URL
        self.assertIn(f"/course/{self.course.id}/learn/", content)

    def test_classroom_uses_jwplayer(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("classroom", args=[self.course.id]))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        # right side must be JW Player, not plain iframe
        self.assertIn("jwplayer", content.lower())
        self.assertIn('id="jwplayer"', content)
        self.assertIn("cdn.jwplayer.com", content)
        self.assertIn('jwplayer("jwplayer").setup', content)
        # video lessons should have mp4 source for JW Player
        video_lesson = Lesson.objects.filter(course=self.course, kind="video").first()
        self.assertTrue(video_lesson.video_url.endswith(".mp4"))

    def test_auto_complete_is_idempotent(self):
        self.client.force_login(self.user)
        lesson = Lesson.objects.filter(course=self.course, kind="video").first()
        self.client.get(reverse("classroom", args=[self.course.id]))
        # first auto-complete via new endpoint (JSON)
        resp = self.client.post(reverse("complete_lesson", args=[self.course.id, lesson.id]), HTTP_X_REQUESTED_WITH="XMLHttpRequest", HTTP_ACCEPT="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["ok"])
        self.assertTrue(LessonProgress.objects.filter(user=self.user, lesson=lesson, completed=True).exists())
        done_before = LessonProgress.objects.filter(user=self.user, lesson__course=self.course, completed=True).count()
        # second call should not duplicate or un-complete
        resp2 = self.client.post(reverse("complete_lesson", args=[self.course.id, lesson.id]), HTTP_X_REQUESTED_WITH="XMLHttpRequest", HTTP_ACCEPT="application/json")
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(resp2.json()["completed"])
        done_after = LessonProgress.objects.filter(user=self.user, lesson__course=self.course, completed=True).count()
        self.assertEqual(done_before, done_after)

    def test_no_mark_complete_button(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("classroom", args=[self.course.id]))
        content = resp.content.decode()
        # Ensure manual button removed — completion is automatic
        self.assertNotIn('class="check-btn"', content)
        self.assertNotIn("Mark complete</button>", content)
        self.assertIn("completeRow", content)
        self.assertIn("/complete/", content)
        self.assertIn("automatically", content.lower())
