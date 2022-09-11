from api import PetFriends
from settings import *
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список. """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Рыж', animal_type='кот',
                                     age='4', pet_photo='images/foto.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/foto.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Кот', age=1):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


########################################################################################################################
# + 10 тестов
# 1 новый питомец без фото
def test_add_new_pet_with_valid_data_no_foto(name='Вася', animal_type='рыба',
                                             age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


# 2 успешное обновление фото
def test_successful_update_foto():
    """Проверяем возможность обновления фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/foto_new.jpg')
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)
    assert status == 200


# 3 Тест на ввод неправильного email
def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 """
    status, result = pf.get_api_key(email, password)
    assert status == 403


# 4 Тест на ввод неправильного пароля
def test_get_api_key_for_invalid_pass(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 """
    status, result = pf.get_api_key(email, password)
    assert status == 403


# 5 Тест на ввод пустого емейла
def test_get_api_key_for_empty_mail(email=empty_mail, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 """
    status, result = pf.get_api_key(email, password)
    assert status == 403


# 6 Тест на ввод пустого пароля
def test_get_api_key_for_empty_pass(email=valid_email, password=empty_password):
    """ Проверяем что запрос api ключа возвращает статус 403 """
    status, result = pf.get_api_key(email, password)
    assert status == 403


# 7 новый питомец c отрицательным возрастом (провален)
def test_add_new_pet_with_invalid_age(name='Рыж', animal_type='кот',
                                      age='-10', pet_photo='images/foto.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == name


# 8 новый питомец c фото некорректного расширения (провален)
def test_add_new_pet_with_invalid_photo(name='Барс', animal_type='кот',
                                        age='2', pet_photo='images/foto2.txt'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert result['name'] == name


# 9 обновление питомца, некорректный возраст (провален)
def test_add_new_no_foto_age_word(name='Вася', animal_type='рыба',
                                  age='слово'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_foto(auth_key, name, animal_type, age)
    assert status == 400


# 10 пустой логин и пароль
def test_get_api_key_for_empty_data(email=empty_mail, password=empty_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
