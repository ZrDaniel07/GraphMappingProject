# Graph Mapping Project

Este projeto tem como objetivo realizar a varredura de grafos gerados por uma API via WebSocket e encontrar os melhores caminhos de forma eficiente. Ele é capaz de lidar com grafos direcionais e não direcionais, considerando diferentes pesos em suas arestas. Os resultados encontrados são armazenados em um banco de dados SQLite para futuras análises.

## Requisitos
- Python 3.8+
- WebSockets
- FastAPI
- SQLite

## Passos para Configuração do Ambiente de Desenvolvimento

1. **Clonar o Repositório**
   ```sh
   git clone https://github.com/seu-usuario/GraphMappingProject.git
   cd GraphMappingProject
   ```

2. **Criar um Ambiente Virtual**
   Crie um ambiente virtual para o projeto para gerenciar as dependências de forma isolada:
   ```sh
   python -m venv venv
   ```

3. **Ativar o Ambiente Virtual**
   - No Windows:
     ```sh
     venv\Scripts\activate
     ```
   - No Linux/macOS:
     ```sh
     source venv/bin/activate
     ```

4. **Instalar as Dependências**
   Instale as dependências necessárias listadas no arquivo `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

5. **Executar a API de Grafos**
   Navegue até o diretório da API e execute-a usando o Uvicorn:
   ```sh
   cd apiGrafos-main
   uvicorn api.main:app --reload
   ```

6. **Executar o Cliente de Busca de Grafos**
   Navegue de volta para o diretório principal e execute o script `client.py` para iniciar a busca pelos melhores caminhos nos grafos:
   ```sh
   cd ..
   python client.py
   ```

## Testar o WebSocket

Você pode testar a comunicação com o WebSocket usando ferramentas como o Postman. Para isso, use a URL do WebSocket fornecida pelo servidor (exemplo: `ws://localhost:8000/ws/{grupo_id}/{labirinto_id}`).

## Estrutura do Projeto

- **apiGrafos-main/**: Contém a API que gera os grafos e fornece os dados via WebSocket.
- **client.py**: Cliente que se conecta à API via WebSocket, executa a busca nos grafos e armazena os resultados.
- **requirements.txt**: Lista de dependências do projeto.
- **results.db**: Banco de dados SQLite onde os caminhos encontrados são armazenados.

## Funcionamento do Cliente (`client.py`)

1. **Conexão via WebSocket**: O cliente se conecta ao servidor WebSocket para receber o vértice inicial e, posteriormente, solicita a lista de adjacências de cada vértice.
2. **Busca Múltipla**: Utiliza uma fila de prioridade para realizar a busca do melhor caminho (similar ao algoritmo de Dijkstra) e armazena todos os caminhos encontrados.
3. **Armazenamento em Banco de Dados**: Todos os caminhos são armazenados em um banco de dados SQLite (`results.db`) para análise posterior.
4. **Exibição dos Resultados**: Ao final, os caminhos encontrados são exibidos no console.

## Exemplos de Comandos Úteis

- **Adicionar novas dependências**:
  ```sh
  pip freeze > requirements.txt
  ```
