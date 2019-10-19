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
        u = User.objects.create_user('hello@world.check', 'crock', 'check123')
        u.save()
        self.selenium.get('%s%s' % (self.live_server_url, '/auth/'))
        auth_form = self.selenium.find_elements_by_xpath(
            '//form[@id = "auth_form"]//input')
        auth_form[1].send_keys('rock')
        auth_form[2].send_keys('Check')
        self.selenium.find_element_by_id('auth_button').click()
        cookie = self.selenium.get_cookie('usr')
        self.assertEqual(cookie, None, f'failed, cookie: {cookie}')

        self.selenium.get('%s%s' % (self.live_server_url, '/auth/'))
        auth_form = self.selenium.find_elements_by_xpath(
            '//form[@id = "auth_form"]//input')
        auth_form[1].send_keys('crock')
        auth_form[2].send_keys("check123")
        self.selenium.find_element_by_id('auth_button').click()
        cookie = self.selenium.get_cookie('usr')
        self.assertEqual(int(cookie['value']), u.id, f'failed, cookie: {cookie}, id: {u.id}')
