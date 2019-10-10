from django.test import TestCase
from baseapp.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging

LOGGER = logging.getLogger(__name__)


class TestClassRegAuthSystem(TestCase):
    driver = webdriver.Chrome()

    def test_registration_form_check(self):
        TestClassRegAuthSystem.driver.get("http://127.0.0.1:9012/registration/")
        all_inputs = TestClassRegAuthSystem.driver.find_elements_by_xpath('//form[@id = "registration"]//input')
        for input in all_inputs[1:]:
            input.send_keys('$$$$')
        TestClassRegAuthSystem.driver.find_element_by_id('submit_btn').click()
        u = User.objects.all()
        self.assertFalse(u.exists(), f'failed, len = {len(u)}')

    # def test_authorization_form_check(self):
    #     driver.get("http://127.0.0.1:8090/auth/")
