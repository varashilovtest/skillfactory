import requests as rq
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.__url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str):
        """Метод для получения API ключа"""

        headers = {
            'email': email,
            'password': password
        }
        res = rq.get(self.__url + 'api/key', headers=headers)
        return PetFriends.__get_result(res)

    def get_pets(self, key: str, flr: str = ''):
        """Метод для получения списка питомцев. flt = 'my_pets' - только свои питомцы"""

        headers = {'auth_key': key}
        flr = {'filter': flr}

        res = rq.get(self.__url + 'api/pets', headers=headers, params=flr)
        return PetFriends.__get_result(res)

    def add_pet(self, name: str, animal_type: str, age: str, key: str, pet_photo: str):
        """Метод для добавления питомца на сайт"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'))
            })

        headers = {
            'auth_key': key,
            'Content-Type': data.content_type
        }

        res = rq.post(self.__url + 'api/pets', headers=headers, data=data)
        return PetFriends.__get_result(res)

    def update_pet(self, key: str, pet_id: str, name: str = '', animal_type: str = '', age: int = ''):
        """Метод для изменения информации о питомце"""

        headers = {
            'auth_key': key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = rq.put(self.__url + 'api/pets/{0}'.format(pet_id), headers=headers, data=data)
        return PetFriends.__get_result(res)

    def del_pet(self, key: str, pet_id: str):
        """Метод для удаления питомца с сайта"""

        res = rq.delete(self.__url + 'api/pets/{0}'.format(pet_id), headers={'auth_key': key})
        return PetFriends.__get_result(res)

    @staticmethod
    def __get_result(res: rq.models.Response) -> tuple[int, str | dict]:
        """Метод для возврата результатов методов"""

        try:
            result = res.json()
        except:
            result = res.text
        return res.status_code, result
