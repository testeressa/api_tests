import pytest
import requests

BASE_URL = "https://dog.ceo/api"

def test_breeds_list_all():
    resp = requests.get(f'{BASE_URL}/breeds/list/all')
    assert resp.status_code == requests.codes.ok
    assert isinstance(resp.json()['message'], dict)


def test_get_random_breed_image():
    resp = requests.get(f'{BASE_URL}/breeds/image/random')
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"


@pytest.mark.parametrize('breed', ['hound','poodle','bulldog'])
def test_get_random_image_by_breed(breed):
    resp = requests.get(f'{BASE_URL}/breed/{breed}/images/random')
    assert resp.status_code == 200

    data = resp.json()
    assert data["status"] == "success"

    image_url = data["message"]
    assert breed in image_url.lower(), f"Ожидалось изображение породы '{breed}', но получен урл: {image_url}"


@pytest.mark.parametrize('breed,subbreed', [('hound', 'afghan'), ('bulldog', 'french')])
def test_get_sub_breed_images(breed, subbreed):
    resp = requests.get(f'{BASE_URL}/breed/{breed}/{subbreed}/images')
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data['message'], list), "Ответ должен содержать список изображений"
    assert len(data['message']) > 0, "Список изображений не должен быть пустым"

    for image_url in data['message']:
        assert breed in image_url.lower() and subbreed in image_url.lower(), \
            f"Ожидались изображения {breed}/{subbreed}, но получен URL: {image_url}"


@pytest.mark.parametrize('subbreed,count', [('afghan', 1), ('blood', 5),])
def test_get_multiple_images_by_subbreed(subbreed, count):
    breed = 'hound'
    resp = requests.get(f'{BASE_URL}/breed/{breed}/{subbreed}/images/random/{count}')

    assert resp.status_code == 200

    data = resp.json()

    assert isinstance(data['message'], list)
    assert len(data['message']) == count, f"Ожидалось {count} изображений, получено {len(data['message'])}"

    for image_url in data['message']:
        assert breed in image_url.lower() and subbreed in image_url.lower(), \
            f"Ожидались изображения {breed}/{subbreed}, но получен URL: {image_url}"
