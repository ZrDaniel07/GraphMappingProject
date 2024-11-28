import asyncio
import websockets
import json
import heapq

def parse_response(response):
    if "Vértice inválido." in response or "Erro ao acessar o vértice desejado." in response:
        print(f"Recebido uma mensagem de erro: {response}")
        return None, None, []
    try:
        vertex_label = "Vértice atual:"
        tipo_label = ", Tipo:"
        adjacents_label = ", Adjacentes(Vertice, Peso):"
        vertex_index = response.find(vertex_label)
        tipo_index = response.find(tipo_label)
        adjacents_index = response.find(adjacents_label)
        if vertex_index == -1 or tipo_index == -1 or adjacents_index == -1:
            print("Não foi possível encontrar as etiquetas na resposta")
            return None, None, []
        vertex_id_str = response[vertex_index + len(vertex_label): tipo_index].strip()
        vertex_id = int(vertex_id_str)
        tipo_str = response[tipo_index + len(tipo_label): adjacents_index].strip()
        if tipo_str.lower() == 'entrada' or tipo_str == '1':
            tipo = 1
        elif tipo_str.lower() == 'saida' or tipo_str == '2':
            tipo = 2
        else:
            tipo = 0
        adjacents_str = response[adjacents_index + len(adjacents_label):].strip()
        import ast
        try:
            adjacents_list = ast.literal_eval(adjacents_str)
            adjacents = [(int(a[0]), int(a[1])) for a in adjacents_list]
        except Exception as e:
            print(f"Erro ao avaliar os adjacentes: {e}")
            return None, None, []
        return vertex_id, tipo, adjacents
    except Exception as e:
        print(f"Falha ao interpretar a resposta: {response}")
        print(e)
        return None, None, []

async def adaptive_bfs(websocket, start_vertex, stop_at_first_exit=True):
    visited = set()
    distances = {}
    vertex_info = {}
    queue = [(0, start_vertex, [])]
    exits = []
    while queue:
        current_cost, current_vertex, path = heapq.heappop(queue)
        if current_vertex in visited:
            continue
        visited.add(current_vertex)
        path = path + [current_vertex]
        distances[current_vertex] = current_cost
        if current_vertex in vertex_info:
            vertex, tipo, adjacents = vertex_info[current_vertex]
        else:
            await websocket.send(f"ir:{current_vertex}")
            response = await websocket.recv()
            print(f"Recebido: {response}")
            vertex, tipo, adjacents = parse_response(response)
            if vertex is None:
                continue
            vertex_info[current_vertex] = (vertex, tipo, adjacents)
        if tipo == 2:
            if stop_at_first_exit:
                return path, current_cost
            else:
                exits.append((current_cost, path))
                continue
        neighbor_weights = {}
        for neighbor, weight in adjacents:
            if neighbor not in neighbor_weights or weight < neighbor_weights[neighbor]:
                neighbor_weights[neighbor] = weight
        for neighbor, weight in neighbor_weights.items():
            if neighbor not in visited:
                new_cost = current_cost + weight
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path))
    if exits:
        exits.sort()
        return exits[0][1], exits[0][0]
    return [], float('inf')

async def main():
    group_id = "6ec1b5b7-0ca0-4f47-b867-360f713c5a24"
    labyrinth_id = 1
    ws_url = f"ws://localhost:8000/ws/{group_id}/{labyrinth_id}"
    try:
        async with websockets.connect(ws_url) as websocket:
            start_vertex = 0
            print("Explorando o labirinto...")
            path, cost = await adaptive_bfs(websocket, start_vertex)
            if path:
                print(f"Saída encontrada! Caminho: {path}, Custo total: {cost}")
            else:
                print("Não foi possível encontrar a saída.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Conexão fechada pelo servidor: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

asyncio.run(main())
