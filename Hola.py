import json
import time

import requests


text = input("Введите текст: ")
url = f"https://cataas.com/cat/says/{text}"

yd_token = input("Введите токен: ")
headers = {"Authorization": f"OAuth {yd_token}"}

folder_response = requests.put(
    "https://cloud-api.yandex.net/v1/disk/resources",
    headers=headers,
    params={"path": "PYQA-140"}
)


filename = f"{text}.jpg"
disk_path = f"PYQA-140/{filename}"

upload_response = requests.post(
    "https://cloud-api.yandex.net/v1/disk/resources/upload",
    headers=headers,
    params={
        "path": disk_path,
        "url": url
    }
)
upload_response.raise_for_status()

operation_url = upload_response.json()["href"]


while True:
    operation_response = requests.get(
        operation_url,
        headers=headers
    )
    operation_response.raise_for_status()

    status = operation_response.json()["status"]
    print(f"Статус загрузки: {status}")

    if status == "success":
        print("Картинка загружена")
        break

    if status == "failed":
        raise RuntimeError("Не удалось загрузить картинку")

    time.sleep(1)


file_response = requests.get(
    "https://cloud-api.yandex.net/v1/disk/resources",
    headers=headers,
    params={"path": disk_path}
)
file_response.raise_for_status()

size = file_response.json()["size"]

data = {
    "filename": filename,
    "disk_path": disk_path,
    "size_bytes": size
}


with open("info.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)