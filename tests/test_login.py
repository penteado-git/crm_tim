from app.core.login import *
import os


def test_get_driver():
    driver = get_driver()
    driver.get('https://www.google.com.br')
    assert 'google' in driver.current_url


def test_get_token():
    load_token_env()
    assert isinstance(os.getenv('JWT_TOKEN'), str)
