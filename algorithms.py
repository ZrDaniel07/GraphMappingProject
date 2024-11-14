import asyncio
import heapq
import json

async def explore_maze(websocket, start_vertex):
    visited = set()
    path = {}
    queue = [(0, start_vertex, None)]  # (custo, id_vértice, id_pai)

    while queue:
        cost, current_vertex, parent = heapq.heappop(queue)
        if current_vertex in visited:
            continue
        visited.add(current_vertex)
        if parent is not None:
            path[current_vertex] = parent

        # Solicitar informações sobre o vértice atual
        await websocket.send(f"Ir:{current_vertex}")
        response = await websocket.recv()
        current_vertex_id, adjacents, vertex_type = parse_vertex_message(response)

        # Verificar se o vértice atual é uma saída
        if is_exit(vertex_type):
            print(f"Saída encontrada no vértice {current_vertex_id}")
            return visited, path, current_vertex_id

        # Processar vértices adjacentes
        for adj in adjacents:
            adj_id, weight = adj
            if adj_id not in visited:
                heapq.heappush(queue, (cost + weight, adj_id, current_vertex_id))

    return visited, path, None  # Nenhuma saída encontrada

def reconstruct_path(path, exit_vertex):
    # Reconstruir o caminho do início até o vértice de saída
    current = exit_vertex
    reverse_path = []
    while current is not None:
        reverse_path.append(current)
        current = path.get(current)
    return list(reversed(reverse_path))

def is_exit(vertex_type):
    # Determinar se o vértice é uma saída com base em seu tipo
    return vertex_type == 1  # Tipo == 1 indica uma saída

def parse_vertex_message(message):
    # Analisar a mensagem JSON do servidor
    data = json.loads(message)
    current_vertex_id = data['Id']
    adjacents = data['Adjacencia']  # Lista de [id_vértice, peso]
    vertex_type = data['Tipo']
    return current_vertex_id, adjacents, vertex_type
