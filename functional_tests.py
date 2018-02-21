from selenium import webdriver

browser = webdriver.Firefox()

# Sean has heard about a cool new online to-do list app.
# He goes to check out its homepage
browser.get('http://localhost:8000')

# He notices the page title and header mention to-do lists
assert 'To-Do' in browser.title

# He is invited to enter a to-do list straight away

# He types "Get a haircut" into a text box

# When he hits enter, the page updates, and now the page lists
# "1: Get a haircut" as an item in a to-do list

# There is still a text box inviting him to add another item. 
# He enters "Do 100 pushups"

# The page updates again, and shows both items on her list

# Sean wonders whether the site will remember her list. Then he sees
# that the site has generated a unique URL for him -- there is some 
# explanatory text to that effect. 

# He visits the URL - his to-do list is still there. 

# Satisfied, he gets back to work

browser.quit()

