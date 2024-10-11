import asyncio
import websockets

async def map_graph(websocket_url):
    # Conecta ao servidor WebSocket
    async with websockets.connect(websocket_url) as websocket:
        # Recebe a mensagem inicial do servidor
        message = await websocket.recv()
        print(f"Mensagem recebida: {message}")

        # Analisa a mensagem para extrair o ID do vértice atual e os adjacentes
        try:
            # Divide a mensagem em 'Vértice atual: X' e 'Adjacentes: [...]'
            vertex_part, adjacents_part = message.split(', Adjacentes:')
            # Extrai o ID do vértice atual
            current_vertex_id = int(vertex_part.split(':')[1].strip())
            # Extrai a string dos adjacentes
            adjacents_str = adjacents_part.strip()
            # Remove colchetes e aspas
            adjacents_str = adjacents_str.strip("[]")
            adjacents_list = adjacents_str.split(',')
            # Converte os adjacentes para inteiros
            adjacent_vertices = [int(v.strip().strip("'").strip('"')) for v in adjacents_list if v.strip()]
        except Exception as e:
            print(f"Erro ao analisar a mensagem inicial: {e}")
            return

        # Inicializa as estruturas de dados para a travessia do grafo
        visited = set()   # Conjunto para manter os vértices visitados
        graph = {}        # Dicionário para armazenar o grafo mapeado
        to_visit = []     # Lista de vértices a serem visitados

        # Marca o vértice atual como visitado e armazena no grafo
        visited.add(current_vertex_id)
        graph[current_vertex_id] = adjacent_vertices

        # Adiciona os adjacentes à lista de visita
        to_visit.extend(adjacent_vertices)

        # Loop principal para percorrer o grafo
        while to_visit:
            # Obtém o próximo vértice a visitar
            next_vertex = to_visit.pop(0)
            if next_vertex in visited:
                continue  # Se já foi visitado, ignora

            # Envia o comando para ir ao próximo vértice
            command = f"ir:{next_vertex}"
            await websocket.send(command)

            # Recebe a resposta do servidor
            message = await websocket.recv()
            print(f"Mensagem recebida: {message}")

            # Analisa a mensagem para extrair o ID do vértice atual e os adjacentes
            try:
                # Divide a mensagem em 'Vértice atual: X' e 'Adjacentes: [...]'
                vertex_part, adjacents_part = message.split(', Adjacentes:')
                # Extrai o ID do vértice atual
                current_vertex_id = int(vertex_part.split(':')[1].strip())
                # Extrai a string dos adjacentes
                adjacents_str = adjacents_part.strip()
                # Remove colchetes e aspas
                adjacents_str = adjacents_str.strip("[]")
                adjacents_list = adjacents_str.split(',')
                # Converte os adjacentes para inteiros
                adjacent_vertices = [int(v.strip().strip("'").strip('"')) for v in adjacents_list if v.strip()]
            except Exception as e:
                print(f"Erro ao analisar a mensagem: {e}")
                continue  # Em caso de erro, continua para o próximo vértice

            # Marca o vértice atual como visitado e armazena no grafo
            visited.add(current_vertex_id)
            graph[current_vertex_id] = adjacent_vertices

            # Adiciona os adjacentes não visitados à lista de visita
            for v in adjacent_vertices:
                if v not in visited and v not in to_visit:
                    to_visit.append(v)

        # Após a travessia, imprime o grafo mapeado
        print("Mapeamento do Grafo Completo:")
        for vertex, adjacents in graph.items():
            print(f"Vértice {vertex}: Adjacentes {adjacents}")

# Substitua pela URL real obtida anteriormente
websocket_url = "ws://localhost:8000/ws/d731905b-b9aa-4b5f-aa90-101316674829/1"

# Executa a função assíncrona usando asyncio.run()
asyncio.run(map_graph(websocket_url))
