from api import PetFriends
import settings as s

pf = PetFriends()


def test_get_key(email: str = s.email, password: str = s.password):
    status, result = pf.get_api_key(email, password)
    assert status == 200 and 'key' in result


def test_add_pet(email: str = s.email, password: str = s.password, photo: str = 'images/cat.jpg'):
    _, key = pf.get_api_key(email, password)
    status, result = pf.add_pet('Кот', 'cat', '3', key['key'], photo)
    assert status == 200 and result['name'] == 'cat'


def test_get_pets(email: str = s.email, password: str = s.password, flr: str = 'my_pets',
                  photo: str = 'images/cat.jpg'):
    _, key = pf.get_api_key(email, password)
    status, my_pets = pf.get_pets(key['key'], flr)
    if not my_pets['pets']:
        _, result_add = pf.add_pet('Кот', 'cat', '3', key['key'], photo)
        _, my_pets = pf.get_pets(key['key'], 'my_pets')
    assert status == 200 and my_pets['pets']


def test_update(email: str = s.email, password: str = s.password, photo: str = 'images/cat.jpg'):
    _, key = pf.get_api_key(email, password)
    _, my_pets = pf.get_pets(key['key'], 'my_pets')
    if not my_pets['pets']:
        _, result_add = pf.add_pet('Кот', 'cat', '3', key['key'], photo)
        _, my_pets = pf.get_pets(key['key'], 'my_pets')

    status, result_update = pf.update_pet(key['key'], my_pets['pets'][0]['id'], name='Tonny', animal_type='dog')
    assert status == 200 and result_update['name'] == 'Tonny' and result_update['animal_type'] == 'dog'


def test_delete(email: str = s.email, password: str = s.password, photo: str = 'images/cat.jpg'):
    _, key = pf.get_api_key(email, password)
    _, my_pets = pf.get_pets(key['key'], 'my_pets')
    if not my_pets['pets']:
        _, result_add = pf.add_pet('Кот', 'cat', '3', key['key'], photo)
        _, my_pets = pf.get_pets(key['key'], 'my_pets')

    status, result = pf.del_pet(key['key'], my_pets['pets'][0]['id'])
    assert status == 200 and not result


def test_get_key_incorrect_data(email: str = s.unemail, password: str = s.unpassword):
    status, key = pf.get_api_key(email, password)
    assert status != 200 and "This user wasn't found in database" in key


def test_get_key_incorrect_password(email: str = s.email, password: str = s.unpassword):
    status, key = pf.get_api_key(email, password)
    assert status != 200 and "This user wasn't found in database" in key


def test_add_pet_no_data(email: str = s.email, password: str = s.password, photo: str = 'images/cat.jpg'):
    _, key = pf.get_api_key(email, password)
    status, result = pf.add_pet('', '', '', key['key'], photo)
    assert status == 200 and result['name'] == ''


def test_add_pet_no_photo(email: str = s.email, password: str = s.password, photo: str = 'images/1.txt'):
    _, key = pf.get_api_key(email, password)
    status, result = pf.add_pet('Кот', 'cat', '3', key['key'], photo)
    assert status == 500


def test_add_pet_incorrect_key(photo: str = 'images/cat.jpg'):
    status, result = pf.add_pet('Кот', 'cat', '3', '123', photo)
    assert status != 200 and "Please provide 'auth_key'" in result


def test_get_pet_incorrect_filter(email: str = s.email, password: str = s.password):
    _, key = pf.get_api_key(email, password)
    status, result = pf.get_pets(key['key'], '123')
    assert status != 200 and "Filter value is incorrect" in result


def test_get_pet_incorrect_key():
    status, result = pf.get_pets('123', 'my_pets')
    assert status != 200 and "Please provide 'auth_key' Header" in result


def test_update_incorrect_key(email: str = s.email, password: str = s.password, photo: str = 'images/cat.jpg'):
    _, key = pf.get_api_key(email, password)
    _, my_pets = pf.get_pets(key['key'], 'my_pets')
    if not my_pets['pets']:
        _, result_add = pf.add_pet('Кот', 'cat', '3', key['key'], photo)
        _, my_pets = pf.get_pets(key['key'], 'my_pets')
    status, result = pf.update_pet('123', my_pets['pets'][0]['id'])
    assert status != 200 and "Please provide 'auth_key' Header" in result


def test_update_incorrect_pet_id(email: str = s.email, password: str = s.password):
    _, key = pf.get_api_key(email, password)
    status, result = pf.update_pet(key['key'], '123')
    assert status != 200 and "Pet with this id wasn't found!" in result


def test_delete_incorrect_pet_id(email: str = s.email, password: str = s.password):
    _, key = pf.get_api_key(email, password)
    status, result = pf.del_pet(key['key'], '123')
    assert status != 200 and "Pet with this id wasn't found!" in result
