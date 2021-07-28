from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import amazon_xpath_settings as settings
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import visibility_of_element_located


class AmazonShopper:
    def __init__(self):
        self.url = "https://www.amazon.com/"
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def open_site(self):
        self.driver.get(self.url)

        # make sure we are at the correct web site
        assert self.driver.current_url == self.url

    def run_search(self, search_term):
        search_successful = False

        self.driver.find_element(By.NAME, "field-keywords").send_keys(search_term + Keys.RETURN)
        # wait for page buttons to appear before moving on
        try:
            self.wait.until(
                visibility_of_element_located(
                    (By.XPATH, settings.page_buttons_xpath)
                )
            )
            search_successful = True
        except TimeoutException:
            pass

        assert search_successful, "Page buttons not found"


    def find_products(self):
        # get all product elements from the page
        try:
            result_elements = self.driver.find_elements_by_xpath(settings.search_result_xpath)
        except NoSuchElementException:
            result_elements = []

        # ensure there are results
        assert len(result_elements) > 0, "No products found"
        return result_elements

    def find_best_sellers(self, product_elements):
        best_seller_links = []
        best_seller_elements = []

        # search for those with a best seller badge
        for cur_element in product_elements:
            try:
                best_seller_badge = cur_element.find_element_by_xpath(
                    settings.best_seller_badge_xpath
                )
                best_seller_elements.append(cur_element)
            except NoSuchElementException:
                pass

        # put links in list
        for cur_element in best_seller_elements:
            try:
                product_link_element = cur_element.find_element_by_xpath(
                    settings.product_link_xpath
                )
                best_seller_links.append(product_link_element.get_attribute("href"))
            except NoSuchElementException:
                print("link not found?")

        # check to be sure there are best sellers detected
        assert len(best_seller_links) > 0

        return best_seller_links

    def add_multiple_products_to_cart(self, link_list):
        for link_item in link_list:
            self.add_product_to_cart(link_item)

    def add_product_to_cart(self, product_link):
        product_added = False
        self.driver.get(product_link)
        self.wait.until(
            visibility_of_element_located(
                (By.XPATH, settings.add_cart_button_xpath)
            )
        )
        self.driver.find_element_by_xpath(
            settings.add_cart_button_xpath
        ).click()

        try:
            self.wait.until(
                visibility_of_element_located(
                    (By.XPATH, settings.added_to_cart_text_xpath)
                )
            )
            product_added = True
        except TimeoutException:
            # handle insurance item
            try:
                self.wait.until(
                    visibility_of_element_located(
                        (By.XPATH, settings.no_coverage_button_xpath)
                    )
                )
                self.driver.find_element_by_xpath(
                    settings.no_coverage_button_xpath
                ).click()
                self.wait.until(
                    visibility_of_element_located(
                        (By.XPATH, settings.close_sidesheet_button_xpath)
                    )
                )
                self.driver.find_element_by_xpath(
                    settings.close_sidesheet_button_xpath
                ).click()
                product_added = True
            except NoSuchElementException:
                pass
            except TimeoutException:
                pass

        # check to be sure product was added
        assert product_added, "Product was not added:  {0}".format(product_link)

    def show_cart(self):
        cart_shown = False
        try:
            self.driver.find_element_by_xpath(
                settings.go_to_cart_button_xpath
            ).click()
            cart_shown = True
        except NoSuchElementException:
            pass

        # check to see if cart shown
        assert cart_shown, "Unable to show cart"

    def close_site(self):
        self.driver.close()


if __name__ == "__main__":
    ashop = AmazonShopper()
    ashop.open_site()
    ashop.run_search("girls bicycle")
    found_products = ashop.find_products()
    best_seller_product_links = ashop.find_best_sellers(found_products)
    ashop.add_multiple_products_to_cart(best_seller_product_links)
    ashop.show_cart()

    # ashop.close_site()
