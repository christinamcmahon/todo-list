from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Sean has heard about a cool new online to-do list app.
        # He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do list straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # He types "Get a haircut" into a text box
        inputbox.send_keys('Get a haircut')

        # When he hits enter, the page updates, and now the page lists
        # "1: Get a haircut" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Get a haircut')

        # There is still a text box inviting him to add another item. 
        # He enters "Do 100 pushups"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do 100 pushups')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and shows both items on his list
        self.wait_for_row_in_list_table('1: Get a haircut')
        self.wait_for_row_in_list_table('2: Do 100 pushups')

        # Satisfied, he goes back to sleep. 

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Sean starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Get a haircut')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Get a haircut')

        # He notices that his list has a unique URL
        sean_list_url = self.browser.current_url
        self.assertRegex(sean_list_url, '/lists/.+')

        # Now a new user, Christina, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Sean's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Christina visits the home page. There is no sign of Sean's 
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Get a haircut', page_text)
        self.assertNotIn('Do 100 pushups', page_text)

        # Christina starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: But milk')

        # Christina gets her own unique URL
        christina_list_url = self.browser.current_url
        self.assertRegex(christina_list_url, '/lists/.+')
        self.assertNotEqual(christina_list_url, sean_list_url)

        # Again, there is no trace of Sean's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Get a haircut', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep. 