from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class LandingFooterYearTests(TestCase):
    """Ensure landing renders via engine and via view with dynamic year and i18n suffix."""

    def test_landing_template_renders_current_year_and_suffix(self):
        from django.template import engines
        engine = engines['django']
        tmpl = engine.get_template('landing.html')
        html = tmpl.render({}, None)
        year = str(datetime.now().year)
        self.assertIn(f'Kutiva {year}.', html)
        self.assertIn('data-i18n="footer.copy_suffix"', html)
        # source uses Django now tag, not hardcoded 2022
        with open('templates/landing.html') as f:
            self.assertIn('{% now "Y" %}', f.read())

    def test_i18n_js_has_footer_suffix_translations(self):
        js = open('static/js/i18n.js').read()
        self.assertIn("'footer.copy_suffix': 'Todos os direitos reservados'", js)
        self.assertIn("'footer.copy_suffix': 'All rights reserved'", js)

    def test_landing_view_anonymous_renders_landing_with_kutiva(self):
        c = Client()
        resp = c.get(reverse('landing'))
        self.assertEqual(resp.status_code, 200)
        # anonymous should get landing.html (Kutiva footer)
        year = str(datetime.now().year)
        self.assertContains(resp, f'Kutiva {year}.')
        self.assertContains(resp, 'kutiva-footer')
        # uses landing template
        self.assertTemplateUsed(resp, 'landing.html')

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
