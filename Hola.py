import json
import time

import requests


def create_folder(headers):
    response = requests.put(
        "https://cloud-api.yandex.net/v1/disk/resources",
        headers=headers,
        params={"path": "PYQA-140"}
    )


def upload_cat(headers, text):
    disk_path = f"PYQA-140/{text}.jpg"

    response = requests.post(
        "https://cloud-api.yandex.net/v1/disk/resources/upload",
        headers=headers,
        params={
            "path": disk_path,
            "url": f"https://cataas.com/cat/says/{text}"
        }
    )
    response.raise_for_status()
    operation_url = response.json()["href"]

    while True:
        response = requests.get(operation_url, headers=headers)
        response.raise_for_status()

        status = response.json()["status"]
        print(f"Статус загрузки: {status}")

        if status == "success":
            break

        if status == "failed":
            raise RuntimeError("Не удалось загрузить картинку")

        time.sleep(1)

    return disk_path


def save_info(headers, disk_path):
    response = requests.get(
        "https://cloud-api.yandex.net/v1/disk/resources",
        headers=headers,
        params={"path": disk_path}
    )
    response.raise_for_status()

    file_info = response.json()
    data = {
        "filename": file_info["name"],
        "size_bytes": file_info["size"]
    }

    with open("info.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Информация сохранена в info.json")


text = input("Введите текст: ")
yd_token = input("Введите токен: ")
headers = {"Authorization": f"OAuth {yd_token}"}

create_folder(headers)
disk_path = upload_cat(headers, text)
save_info(headers, disk_path)
