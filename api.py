import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email, password):
        headers = {
            'email': email,
            'password': password
        }
        response = requests.get(self.base_url + 'api/key', headers=headers)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        response = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)

        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def create_pet_simple(self, auth_key, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def delete_pet(self, auth_key, pet_id):
        headers = {'auth_key': auth_key['key']}

        response = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def update_pet_information(self, auth_key, pet_id, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)

        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def add_pet_photo(self, auth_key, pet_id, photo):
        data = MultipartEncoder(
            fields={
                'pet_photo': (photo, open(photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        response = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def add_new_pet_full_info(self, auth_key, name, animal_type, age, photo):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (photo, open(photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        response = requests.post(self.base_url + 'api/pets', headers=headers, data=data)

        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result
