from app.api import PetFriends
from app.settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

# Test(positive) 1 passed
def test_get_api_key_user_id_valid(email=valid_email, password=valid_password):
    #  проверяем запрос API и валидность почтового ящика и пароля
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(f'\n {email}, {password}, {status}, {result}')


# Test(negative) 2 passed
def test_get_api_key_user_id_invalid(email=invalid_email, password=invalid_password):
    #  проверям что запрос API возвращает код 403 на неверный почтовый ящик и пароль
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} теста с неправильным почтовым почтовым ящиком и паролем')


# Test(positive) 3 passed
def test_get_list_of_pets(filter='my_pets'):
    # проверка того, что API возвращает не пустой список
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0
    num = len(result['pets'])
    if filter == 'my_pets':
        print(f' {num} моих питомцев на сайте')
    else:
        print(f'список не пустой')


# Test(positive) 4 passed
def test_add_new_valid_pet(name= 'Fire', animal_type='Red', age='4', pet_photo='images/cat_1.jpg'):
    #  проверка на добавление питомца с корректными данными
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')


# Test(positive) 5 passed
def test_delete_valid_pet():
    #  проверка возможности удаления питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Lion", "cat", "7", "images/cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print(f'В списке было, {num} питомцев')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
    num = len(my_pets['pets'])
    print(f'В списке , {num} питомцев')


# Test(positive) 6 passed
def test_add_valid_pet_without_photo(name='Simple_dog', animal_type='Dog', age='10'):
    # проверка добавления питомца без фото
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Добавлен {result}')

# Test(negative) 7 passed
def test_add_new_invalid_pet(name= '№;%:', animal_type='Dog', age='11'):
    #  проверка на добавление питомца с некорректными данными, спецсимволы
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert name, 'Добавлен питомец с невозможным именем'
    print(f'\n Сайт позволяет добавлять питомца с невозможным именем {name}')


# Test(negative) 8 passed
def test_add_new_pet_with_empty_data():
    #  проверка на добавление питомца с некорректными данными, пустые поля данных
    name = ''
    animal_type = ''
    age = ''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Сайт позволяет добавить питомца с пустым именем {result}')


# Test(negative) 9 passed
def test_add_pet_with_255_simbols(animal_type='Dog', age='4', pet_photo='images/dog_2.jpg'):
    #  проверка на добавление питомца с 255 символами в имени

    name = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea c'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name']
    letter_count = len(list_name)

    assert status == 200
    assert letter_count == 255, 'Питомец добавлен с именем больше 255 букв'
    print('ok')
    print(f'Сайт позволяет добавлять  питомецев с именем больше 255 букв. {letter_count}')


# Test(positive) 10 passed
def test_update_pet_info(name='Rex', animal_type='Dog', age=9):
    #  проверка на добавление информации к уже существующему питомцу

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
        print('ok')
        print(result)
    else:
        raise Exception("Питомец отсутствует")


# Test(negative) 11 passed
def test_add_new_pet_with_invalid_foto(name='Gann', animal_type='Shepard', age='3', pet_photo='images/dog_4.jpg'):
    # проверка добавления питомца с неккоректной фотографией, при ошибке меняем на имеющееся изображение

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    if not os.path.exists(pet_photo):
        print(f'\n Нет {pet_photo}')
        pet_photo = 'images/dog_1.jpg'
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        print(f'Замена фотографии на {pet_photo}')

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Добавлен {result}')

# Test(positive) 12 passed
def test_successful_delete_pet():
    # проверка возможности удаления питомца

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'В списке {num} питомцев')


# Test 13(negative) passed
def test_successful_delete_invalid_key_pet():
    # проверка удаления питомца по неправильному auth_key

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    print()
    print(auth_key)
    # {'key': 'a0d169f2bdd827cd839bbf3604339e9ca8143b6f994d2fce80ea2389'} #правильный ключ
    auth_key = {'key': '0ad169f2bdd827cd839bbf3604339e9ca8143b6f994d2fce80ea2389'} #неправильный ключ
    print(auth_key)
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Rare", "Dog", "1", "images/dog_2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'В списке было, {num} питомцев')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен 403 и в списке питомцев нет изменений
    assert status == 403
    #assert pet_id in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'В списке {num} питомцев')