import pytest
import requests

BASE_URL = "https://api.openbrewerydb.org/v1"


@pytest.mark.parametrize('per_page', [0, -1, 3])
def test_get_breweries_per_page(per_page):
    try:
        resp = requests.get(f'{BASE_URL}/breweries?per_page={per_page}')
        resp.raise_for_status()

        data = resp.json()

        assert resp.status_code == 200

        if per_page > 0:
            assert isinstance(data, list)
            assert len(data) == per_page
        else:
            assert isinstance(data, dict)
            assert "message" in data

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка при запросе: {e}")


@pytest.mark.parametrize('city', ['Marseille', 'Louisville', 'San Diego'])
def test_get_breweries_by_city(city):
    resp = requests.get(f'{BASE_URL}/breweries?by_city={city}')
    resp.raise_for_status()

    data = resp.json()

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(data) > 0, f"Для города {city} получен пустой список пивоварен"

    for brewery in data:
        assert city.lower() in brewery["city"].lower(), f"Ожидался город {city}, получен {brewery['city']} "\
                                                        f"(полные данные: {brewery})"


@pytest.mark.parametrize("name", ["Almanac Beer Company", "Gordon Biersch Brewery Restaurant - San Diego"])
def test_search_breweries_by_name(name):
    resp = requests.get(f"{BASE_URL}/breweries?by_name={name}")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0, f"Не найдено пивоварен по имени '{name}'"

    for brewery in data:
        assert name.lower() in brewery["name"].lower(), \
            f"Ожидалось имя содержащее '{name}', получено '{brewery['name']}'"


def test_list_breweries():
    resp = requests.get(f"{BASE_URL}/breweries")

    data = resp.json()

    assert resp.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0, "Сервер вернул пустой список пивоварен"


def test_get_random_brewery():
    resp = requests.get(f"{BASE_URL}/breweries/random")
    assert resp.status_code == 200

    data = resp.json()

    assert isinstance(data, list)
    assert len(data) > 0, "Сервер вернул пустой список случайных пивоварен"
    assert len(data) == 1, f"Ожидалась одна пивоварня, получено {len(data)}"
