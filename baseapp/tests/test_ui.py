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

    def test_registration_form_check(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/registration/'))
        all_inputs = self.selenium.find_elements_by_xpath(
            '//form[@id = "registration"]//input')
        for input_field in all_inputs[1:]:
            input_field.send_keys('$$$$')
        self.selenium.find_element_by_id('submit_btn').click()
        u = User.objects.all()
        self.assertFalse(u.exists(), f'failed, len = {len(u)}')
