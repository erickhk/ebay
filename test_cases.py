import unittest, time
from ddt import ddt, data, file_data, unpack
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class EbayPage:
    def search_for(self, container, search_term):
        """Handles searching"""
        search_bar = container.find_element_by_css_selector('header[role=\'banner\'] input[type=\'text\']')
        search_bar.click()
        search_bar.clear()
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.ENTER)
        
    def go_to_cart(self, container):
        search_bar = container.find_element_by_css_selector('header[role=\'banner\'] #gh-cart-i')
        
    def navigate_to_category(self, container, primary_cat, secondary_cat=''):
        pass

class HomePage(EbayPage):
    pass
        
class ProductListPage(EbayPage):

    def select_first_product(self, container):
        prod_link = container.find_element_by_css_selector('ul.srp-results > li a.s-item__link')
        prod_link.click()

    def select_product(self, container, product_name):
        """Select first result item"""
        prod_link = container.find_element_by_link_text(product_name)
        prod_link.click()

class ProductDetailsPage(EbayPage):

    def add_to_cart(self, container):
        """Add current item to cart"""
        add_button = container.find_element_by_xpath('.//a[contains(normalize-space(),"Add to cart")]')
        add_button.click()
        
    def get_recomendation_popup(self, container):
        return container.find_element_by_css_selector('div[role=\'dialog\']')
        
    def select_first_option(self, container):
        dropdown = Select(container.find_element_by_css_selector('select#msku-sel-1'))
        dropdown.select_by_index(1)
        time.sleep(1)
    
class RecommendationPopup():
    def go_to_cart(self, container):
        container.find_element_by_link_text('Go to cart').click()

@ddt
class SimpleTestCase(unittest.TestCase):

    prod_url = 'https://www.ebay.com.au/'
    prod_user = '???'
    prod_pass = '???'
    home_page = HomePage()
    product_list = ProductListPage()
    product_details = ProductDetailsPage()
    popup_functions = RecommendationPopup()

    def setUp(self):
        """Initial state is user on home page"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(4)

        # Get the landing page
        self.driver.get(self.prod_url)
        # Extend with login, perhaps?

    def tearDown(self):
        """Clean up"""
        self.driver.quit()

    @data('umbrella', 'plate')
    def test_add_to_cart(self, search_term):
        self.home_page.search_for(self.driver, search_term)
        self.product_list.select_first_product(self.driver)
        
        # Handle both items with and without options
        try:
            self.product_details.select_first_option(self.driver)
        except:
            pass
        self.product_details.add_to_cart(self.driver)
        
        # In case the business rule changes..
        try:
            popup = self.product_details.get_recomendation_popup(self.driver)
            self.popup_functions.go_to_cart(popup)
        except:
            self.product_details.go_to_cart(self.driver)
        
        # For demo purposes
        time.sleep(4)

    @unittest.skip("Possible extension")
    def test_2(self):
        pass

if __name__ == '__main__':
    """Used for demo purposes"""
    unittest.main()