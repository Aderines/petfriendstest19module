from api import PetFriends
from settings import valid_email, valid_password, invalid_password

pf = PetFriends()


# Проверки авторизации: негативный и позитивный тест
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_for_user_without_pass(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    assert "This user wasn't found in database" in result


# Проверки выдачи списка питомцев: всех, своих или с неправильным фильтром
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # ?
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_my_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # ?
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) == 0 or len(result['pets']) > 0


def test_get_pets_with_wrong_filter(filter='ololo'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # ?
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200
    assert "Filter value is incorrect" in result


# Проверка на создание питомца
def test_create_pet_simple(name='test', animal_type='test', age='test'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['id'] is not None


# Проверки на удаление питомца - существующего и несуществующего
def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 200


def test_delete_nonexistent_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = 'olololo'
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status != 200, 'Бага'


# Проверка на обновлении инф-ции питомца:
def test_update_pet(name='test2', animal_type='test2', age='test2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][0]['id']
    status, result = pf.update_pet_information(auth_key, pet_id, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


# Проверка на добавление фото к сущ. питомцу
def test_add_pet_photo(photo='images/cat.png'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][0]['id']
    status, result = pf.add_pet_photo(auth_key, pet_id, photo)

    assert status == 200
    assert result['pet_photo'] is not None
    assert 'jpeg' in result['pet_photo']


# Проверка на создание питомца с фото
def test_create_pet_with_photo(name='salem', animal_type="lazy", age='1000', photo='images/salem.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_full_info(auth_key, name, animal_type, age, photo)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['id'] is not None
    assert result['pet_photo'] is not None
    assert 'jpeg' in result['pet_photo']
