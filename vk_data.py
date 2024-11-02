


import requests
import json
import os


user_id = "203083218"
output_file = "vk_data.json"
access_token = "TOKEN"
# Функция для выполнения запроса к VK API
def vk_request(method, access_token, params=None):
    url = f"https://api.vk.com/method/{method}"
    params = params or {}
    params.update({
        "access_token": access_token,
        "v": "5.131"  # Версия API
    })
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Функция для получения данных о пользователе, друзьях, подписках и группах
def get_user_info(access_token, user_id):
    try:
        user_info = vk_request("users.get", access_token, {"user_ids": user_id, "fields": "bdate,city,country"})
        friends = vk_request("friends.get", access_token, {"user_id": user_id, "fields": "nickname"})
        followers = vk_request("users.getFollowers", access_token, {"user_id": user_id, "fields": "nickname"})
        subscriptions = vk_request("users.getSubscriptions", access_token, {"user_id": user_id})
        groups = vk_request("groups.get", access_token, {"user_id": user_id, "extended": 1})

        return {
            "user_info": user_info,
            "friends": friends,
            "followers": followers,
            "subscriptions": subscriptions,
            "groups": groups
        }
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API VK: {e}")
        return None
    except KeyError as e:
        print(f"Ошибка в структуре ответа от API VK: {e}")
        return None

    # Функция для сохранения данных в JSON файл
def save_to_json(data, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Данные успешно сохранены в {file_path}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    # Основная функция
def main():
        # Вставьте сюда ваш токен
        access_token = "TOKEN"

        # Получение данных
        user_data = get_user_info(access_token, user_id)
        if user_data:
            # Получаем путь к текущему скрипту и добавляем название файла
            script_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(script_dir, output_file)

            # Сохранение данных в JSON
            save_to_json(user_data, file_path)

if __name__ == "__main__":
        main()
