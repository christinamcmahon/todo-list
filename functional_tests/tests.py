from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
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
        time.sleep(1)
        self.check_for_row_in_list_table('1: Get a haircut')

        # There is still a text box inviting him to add another item. 
        # He enters "Do 100 pushups"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do 100 pushups')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and shows both items on his list
        self.check_for_row_in_list_table('1: Get a haircut')
        self.check_for_row_in_list_table('2: Do 100 pushups')

        # Sean wonders whether the site will remember his list. Then he sees
        # that the site has generated a unique URL for him -- there is some 
        # explanatory text to that effect. 
        self.fail('Finish the test!')

        # He visits the URL - his to-do list is still there. 

        # Satisfied, he gets back to work