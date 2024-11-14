import requests
import json

async def get_group_id(api_url, group_name):
    response = requests.post(f"{api_url}/grupo", json={"nome": group_name})
    response.raise_for_status()
    return response.json()["GrupoId"]

async def get_labyrinths(api_url, group_id):
    response = requests.get(f"{api_url}/labirintos/{group_id}")
    response.raise_for_status()
    return response.json()["labirintos"]

async def get_websocket_url(api_url, group_id, labyrinth_id):
    response = requests.post(f"{api_url}/generate-websocket/", json={
        "grupo_id": str(group_id),
        "labirinto_id": labyrinth_id
    })
    response.raise_for_status()
    return response.json()["websocket_url"]

async def send_solution(api_url, labyrinth_id, group_id, vertices):
    response = requests.post(f"{api_url}/resposta", json={
        "labirinto": labyrinth_id,
        "grupo": str(group_id),
        "vertices": vertices
    })
    response.raise_for_status()
    return response.json()
