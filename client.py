import asyncio
import json
import websockets
from algorithms import explore_maze, reconstruct_path
from utils import get_group_id, get_labyrinths, get_websocket_url, send_solution

API_URL = "http://localhost:8000"
GROUP_NAME = "O_Melhor"

async def main():
    # Obter ou criar o ID do grupo
    group_id = await get_group_id(API_URL, GROUP_NAME)
    print(f"Grupo ID: {group_id}")

    # Obter a lista de labirintos disponíveis
    labyrinths = await get_labyrinths(API_URL, group_id)
    print(f"Labirintos disponíveis: {labyrinths}")

    # Escolher um labirinto para explorar
    labyrinth_id = labyrinths[0]['LabirintoId']  # Escolhe o primeiro labirinto
    print(f"Iniciando exploração do labirinto {labyrinth_id}")

    # Obter a URL do WebSocket para o labirinto escolhido
    websocket_url = await get_websocket_url(API_URL, group_id, labyrinth_id)
    print(f"Conectando ao WebSocket: {websocket_url}")

    # Conectar ao WebSocket e iniciar a exploração
    async with websockets.connect(websocket_url) as websocket:
        # Receber o vértice inicial e adjacentes
        initial_message = await websocket.recv()
        print(f"Mensagem inicial: {initial_message}")

        current_vertex, adjacents, vertex_type = parse_vertex_message(initial_message)
        visited, path, exit_vertex = await explore_maze(websocket, current_vertex)
        print(f"Labirinto explorado. Vértices visitados: {visited}")

        # Reconstruir o melhor caminho até uma saída
        best_path = reconstruct_path(path, exit_vertex)
        print(f"Melhor caminho encontrado: {best_path}")

        # Enviar a solução para a API
        response = await send_solution(API_URL, labyrinth_id, group_id, best_path)
        print(f"Solução enviada com sucesso: {response}")

def parse_vertex_message(message):
    # Analisar a mensagem JSON recebida
    data = json.loads(message)
    current_vertex = data['Id']
    adjacents = data['Adjacencia']
    vertex_type = data['Tipo']
    return current_vertex, adjacents, vertex_type

if __name__ == "__main__":
    asyncio.run(main())
