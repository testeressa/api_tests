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
    assert resp.json()["status"] == "success"


@pytest.mark.parametrize('breed,subbreed', [('hound', 'afghan'), ('bulldog', 'french')])
def test_get_sub_breed_images(breed, subbreed):
    resp = requests.get(f'{BASE_URL}/breed/{breed}/{subbreed}/images')
    assert resp.status_code == 200
    assert isinstance(resp.json()['message'], list)


def test_multiple_images():
    resp = requests.get(f'{BASE_URL}/breed/hound/afghan/images/random/3')
    assert resp.status_code == 200
    assert len(resp.json()['message']) == 3
