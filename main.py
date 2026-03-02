# tests/main_test.py
import pytest
from main import login, create_driver

@pytest.fixture()
def driver():
    return create_driver()

def test_login_success(driver):
    username = 'test_user'
    password = 'test_password'
    assert login(driver, username, password)

def test_login_failure(driver):
    username = 'invalid_user'
    password = 'wrong_password'
    assert not login(driver, username, password)