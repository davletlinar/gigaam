import requests

link = "https://vats455535.megapbx.ru/api/v2/call-records/record/2024-09-30/998a952f-9b11-4d56-9eb4-f61ca4c7dc73/79177982656_in_2024_09_30-07_55_53_79063741444_jufl.mp3"

if requests.get('http://localhost:1488/health').status_code == 200:
    response = requests.post('http://localhost:1488/transcribe', json={"uid": "test", "record": link})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["transcription"][0:4] == "алло"
else:
    print("Server not healthy")