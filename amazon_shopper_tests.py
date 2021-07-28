import amazon_shopper
import unittest


class TestAmazonShopper(unittest.TestCase):
    # def __init__(self):
    #     self.ashop = None
    #     super().__init__()

    def setUp(self) -> None:
        self.ashop = amazon_shopper.AmazonShopper()
        self.ashop.open_site()

    def tearDown(self) -> None:
        self.ashop.close_site()

    def test_search_positive(self):
        self.ashop.run_search("blah")
        found_products = self.ashop.find_products()
        self.assertGreater(len(found_products), 0, "Did not find any products")

        best_seller_list = self.ashop.find_best_sellers(found_products)
        self.assertGreater(len(best_seller_list), 0, "No best seller products found")

    def test_search_negative(self):
        try:
            self.ashop.run_search("\n")
            raise AssertionError("Search should not have succeeded")
        except AssertionError:
            # expected result
            pass

        try:
            found_products = self.ashop.find_products()
            raise AssertionError("No products should have been found")
        except AssertionError:
            # expected result
            pass

        try:
            best_seller_list = self.ashop.find_best_sellers([])
            raise AssertionError("No best sellers should have been found")
        except AssertionError:
            # expected result
            pass



if __name__ == '__main__':
    unittest.main()
