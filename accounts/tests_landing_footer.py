from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class LandingFooterYearTests(TestCase):
    """Footer is removed for now — verify it is not rendered (admin remains)."""

    def test_landing_template_footer_removed(self):
        from django.template import engines
        engine = engines['django']
        tmpl = engine.get_template('landing.html')
        html = tmpl.render({}, None)
        self.assertNotIn('<footer', html)
        # footer HTML removed, but CSS may remain; check that no footer element is rendered
        with open('templates/landing.html') as f:
            content = f.read()
            # remove CSS block check, only check for footer element
            self.assertNotIn('<footer', content)

    def test_i18n_js_has_footer_suffix_translations(self):
        js = open('static/js/i18n.js').read()
        self.assertIn("'footer.copy_suffix': 'Todos os direitos reservados'", js)
        self.assertIn("'footer.copy_suffix': 'All rights reserved'", js)

    def test_landing_view_anonymous_renders_dashboard_logout_without_footer(self):
        c = Client()
        resp = c.get(reverse('landing'))
        self.assertEqual(resp.status_code, 200)
        # landing is dashboard for everyone; footer removed for now
        self.assertTemplateUsed(resp, 'dashboard.html')
        self.assertNotContains(resp, '<footer')
        # logout view: sidebar hidden, main visible
        self.assertNotContains(resp, 'id="sidebar"')
        self.assertContains(resp, '<main>')

    def test_landing_view_authenticated_renders_dashboard(self):
        user = User.objects.create_user(email="auth@example.com", password="pass123", first_name="A", last_name="B")
        c = Client()
        c.force_login(user)
        resp = c.get(reverse('landing'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'dashboard.html')


class ProfileLanguageToggleTests(TestCase):
    def test_toggle_only_in_profile(self):
        with open('templates/profile.html') as f:
            profile = f.read()
        with open('templates/login.html') as f:
            login = f.read()
        with open('templates/signup.html') as f:
            signup = f.read()
        self.assertIn('lang-switch', profile)
        self.assertNotIn('lang-switch', login)
        self.assertNotIn('lang-switch', signup)
