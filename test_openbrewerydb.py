import pytest
import requests

BASE_URL = "https://api.openbrewerydb.org/v1"


def test_get_breweries_per_page():
    per_page = 3
    resp = requests.get(f'{BASE_URL}/breweries?per_page={per_page}')
    assert resp.status_code == 200
    assert len(resp.json()) == per_page


@pytest.mark.parametrize('city', ['Marseille', 'Louisville', 'San Diego'])
def test_get_breweries_by_city(city):
    resp = requests.get(f'{BASE_URL}/breweries?by_city={city}')
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.parametrize("name", ["Almanac Beer Company", "Russian River Brewing Company"])
def test_search_breweries_by_name(name):
    response = requests.get(f"{BASE_URL}/breweries?by_name={name}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_breweries():
    response = requests.get(f"{BASE_URL}/breweries")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_random_brewery():
    response = requests.get(f"{BASE_URL}/breweries/random")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
