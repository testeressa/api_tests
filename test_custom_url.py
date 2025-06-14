import pytest
import requests

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://ya.ru", help="URL to test")
    parser.addoption("--status_code", action="store", default=200, type=int, help="Expected status code")

@pytest.fixture
def url(request):
    return request.config.getoption("--url")

@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")

def test_url_status_code(url, status_code):
    response = requests.get(url)
    assert response.status_code == status_code