import pytest
from base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from recipes.tests.test_recipe_base import RecipeMixin
from unittest.mock import patch


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

    @patch('recipes.views.all.PER_PAGE', new=2)
    def test_home_page_is_paginating(self) -> None:
        # cria 10 receitas
        self.make_recipe_in_batch()

        # o usuário abre o site
        self.browser.get(self.live_server_url)

        # clica na página 2
        page_2: WebElement = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page_2.click()

        # o usuário vê duas receitas
        recipes: list[WebElement] = self.browser.find_elements(
            By.CLASS_NAME,
            'card-container'
        )

        self.assertEqual(len(recipes), 2)
