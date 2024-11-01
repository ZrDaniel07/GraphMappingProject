import asyncio
import websockets
from heapq import heappush, heappop
import sqlite3

# Conexão com o banco de dados SQLite para armazenar os resultados
conn = sqlite3.connect('results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS paths (id INTEGER PRIMARY KEY, path TEXT, total_weight REAL)''')
conn.commit()

async def map_graph(websocket_url):
    queue = []
    visited = set()
    paths = []  # Armazena todos os caminhos encontrados

    # Conectar ao servidor WebSocket
    async with websockets.connect(websocket_url) as websocket:
        # Receber o vértice inicial
        start_message = await websocket.recv()
        start_data = parse_vertex_data(start_message)
        
        # Inicializar a travessia com o vértice inicial
        heappush(queue, (0, start_data['vertex'], [start_data['vertex']]))

        while queue:
            current_weight, current_vertex, current_path = heappop(queue)

            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            # Solicitar a lista de adjacências do vértice atual
            await websocket.send(str(current_vertex))
            response = await websocket.recv()
            adjacents = parse_adjacency_data(response)

            for neighbor, weight in adjacents:
                if neighbor not in visited:
                    total_weight = current_weight + weight
                    new_path = current_path + [neighbor]
                    heappush(queue, (total_weight, neighbor, new_path))

                    # Armazenar cada caminho encontrado
                    paths.append((new_path, total_weight))

        # Salvar todos os caminhos encontrados no banco de dados
        for path, weight in paths:
            c.execute('INSERT INTO paths (path, total_weight) VALUES (?, ?)', (str(path), weight))
        conn.commit()

def parse_vertex_data(message):
    # Analisar a mensagem inicial para extrair o ID do vértice
    return {'vertex': int(message.split(":")[-1].strip())}

def parse_adjacency_data(message):
    # Analisar os dados de adjacência do servidor WebSocket
    return eval(message.split(":")[-1].strip())

def show_results():
    # Função para exibir os resultados armazenados no banco de dados
    c.execute('SELECT * FROM paths')
    rows = c.fetchall()
    for row in rows:
        print(f"Caminho: {row[1]}, Peso Total: {row[2]}")

# Exemplo de uso
if __name__ == "__main__":
    websocket_url = "ws://localhost:8000/ws/{grupo_id}/{labirinto_id}"  # URL do WebSocket
    asyncio.run(map_graph(websocket_url))
    show_results()

# Fechar a conexão com o banco de dados ao finalizar
conn.close()