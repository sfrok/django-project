from django.test import TestCase
from baseapp.models import User
from selenium import webdriver
import logging

LOGGER = logging.getLogger(__name__)


class TestRegAuth(TestCase):
    driver = webdriver.Chrome()

    def test_registration_form_check(self):
        TestRegAuth.driver.get("http://127.0.0.1:9012/registration/")
        all_inputs = TestRegAuth.driver.find_elements_by_xpath(
            '//form[@id = "registration"]//input')
        for input in all_inputs[1:]:
            input.send_keys('$$$$')
        TestRegAuth.driver.find_element_by_id('submit_btn').click()
        u = User.objects.all()
        self.assertFalse(u.exists(), f'failed, len = {len(u)}')
