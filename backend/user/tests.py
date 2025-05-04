from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from.models import CustomUser

class AuthSeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_registration(self):
        self.driver.get(f'{self.live_server_url}/api/auth/registration/')
        self.driver.find_element(
            By.NAME, 'email').send_keys('test@example.com')
        self.driver.find_element(By.NAME, 'full_name').send_keys('Test User')
        self.driver.find_element(By.NAME, 'role').select_by_value('USER')
        self.driver.find_element(
            By.NAME, 'password1').send_keys('testpassword123')
        self.driver.find_element(
            By.NAME, 'password2').send_keys('testpassword123')
        self.driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.assertIn('Account created', self.driver.page_source)

    def test_login_logout(self):
        # Create a user first
        user = CustomUser.objects.create_user(
            email='test@example.com', full_name='Test User', password='testpassword123'
        )
        self.driver.get(f'{self.live_server_url}/api/auth/login/')
        self.driver.find_element(
            By.NAME, 'email').send_keys('test@example.com')
        self.driver.find_element(
            By.NAME, 'password').send_keys('testpassword123')
        self.driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.assertIn('Welcome', self.driver.page_source)
        self.driver.get(f'{self.live_server_url}/api/auth/logout/')
        self.driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.assertIn('Logged out', self.driver.page_source)
