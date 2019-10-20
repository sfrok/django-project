from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from baseapp.models import User


class TestRegAuth(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_registration_form(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/registration/'))
        all_inputs = self.selenium.find_elements_by_xpath(
            '//form[@id = "registration"]//input')
        for input_field in all_inputs[1:]:
            input_field.send_keys('$$$$')
        self.selenium.find_element_by_id('submit_btn').click()
        u = User.objects.all()
        self.assertFalse(u.exists(), f'failed, len = {len(u)}')

    def test_auth_form(self):
        entries = [
            ('right entries',            'crock', 'check123')
            ('wrong username (r -> cr)', 'rock',  'check123')
            ('wrong username (C -> c)',  'Crock', 'check123')
            ('wrong password (2 -> 23)', 'crock', 'check12')
            ('wrong password (C -> c)',  'crock', 'Check123')
            ('wrong entries',            'rock',  'Check')
        ]
        u = User.objects.create_user('hello@world.check', entries[0][1], entries[0][2])
        u.save()
        for entry in entries:
            self.selenium.get('%s%s' % (self.live_server_url, '/auth/'))
            self.selenium.find_element_by_id('username').send_keys(entry[1])
            self.selenium.find_element_by_id('password').send_keys(entry[2])
            self.selenium.find_element_by_id('auth_button').click()
            cookie = self.selenium.get_signed_cookie('usr')
            user_id = u.id if entry[1] is u.username and entry[2] is u.password else None
            self.selenium.delete_cookie('usr')
            self.assertEqual(int(cookie['value']), user_id, f'{entry[0]}, cookie: {cookie}')
