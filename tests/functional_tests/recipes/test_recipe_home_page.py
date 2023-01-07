import pytest
from base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from recipes.tests.test_recipe_base import RecipeMixin
from time import sleep


@pytest.mark.functional_test
class RecipeHomePageFunctionalTestCase(RecipeBaseFunctionalTest, RecipeMixin):
    def test_home_page_whitout_recipes_no_recipe_found(self) -> None:
        self.browser.get(self.live_server_url)
        body: WebElement = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipe found', body.text)

    def test_search_input_find_correct_recipe(self) -> None:
        # make 10 recipes
        self.make_recipe_in_batch()

        # open the browser
        self.browser.get(self.live_server_url)

        # get the search input by XPATH
        search_input: WebElement = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="buscar receita"]',
            )
        # type 'Recipe Title-1'
        search_input.send_keys('Recipe Title-1')
        # press ENTER
        search_input.send_keys(Keys.ENTER)

        # get box-card element
        recipe: WebElement = self.browser.find_element(
            By.CLASS_NAME,
            'box-card-info'
            )

        # the user see the result in browser
        self.assertIn('Recipe Title-1', recipe.text)
