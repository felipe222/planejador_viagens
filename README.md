# Planejador de Viagens (Travel Planner)

Uma aplicação web avançada para otimização de roteiros de viagens complexos, utilizando algoritmos genéticos (NSGA-II) para balancear múltiplos objetivos (custo e tempo).

## Funcionalidades Principais

- **Otimização Multiobjetivo**: Encontra o equilíbrio ideal entre custo total e duração da viagem.
- **Integração Real (Parcial)**:
    - **Aeroportos**: Autocomplete com dados locais (JSON) de cidades brasileiras.
    - **Dados Estáticos**: Integração com base de dados JSON para hotéis, aluguel de carros e distâncias reais entre cidades selecionadas.
    - **Simulação (Mock)**: Fallback inteligente para rotas aéreas ou locais sem dados específicos.
- **Interface Interativa**: Frontend em Next.js para construção fácil de roteiros multi-destino.

## Estrutura de Dados (Backend)

O sistema utiliza arquivos JSON locais (`backend/data/`) para enriquecer a geração de rotas:

- **`cidades.json`**: Cadastro de cidades com coordenadas e IDs (IATA).
- **`hoteis.json`**: Lista de opções de hospedagem reais por cidade, incluindo nome e custo diário.
- **`aluguel_carros.json`**: Locadoras disponíveis por cidade e custo médio da diária.
- **`distancias_carro.json`**: Matriz de distâncias reais entre cidades para cálculo preciso de deslocamentos terrestres.

Esses dados são carregados pelo `scraper.py` e têm prioridade sobre a geração aleatória.

## Modelo Matemático (Resumo)

A otimização é realizada por um algoritmo genético **NSGA-II** que busca minimizar duas funções objetivo conflitantes:

1.  **Custo Total ($f_1$)**: Soma de passagens aéreas, aluguel de carros e hospedagens.
2.  **Duração Total ($f_2$)**: Tempo total gasto em deslocamentos (voos + estradas).

O algoritmo evolui uma população de "Soluções de Viagem" ao longo de gerações, aplicando cruzamento e mutação para encontrar a **Fronteira de Pareto** — o conjunto de roteiros onde não é possível melhorar o custo sem piorar o tempo (e vice-versa).

## Configuração (`backend/config.py`)

As principais variáveis de ajuste do sistema:

- **`SCRAPER_MODE`**: `"mock"` (padrão, usa dados locais/simulados) ou `"live"` (futuro scraping em tempo real).
- **Parâmetros do Algoritmo Genético**:
    - `POPULATION_SIZE`: Tamanho da população por geração (padrão: 50).
    - `GENERATIONS`: Número de iterações de evolução (padrão: 20).
- **Fatores de Custo (Fallback)**: Valores usados quando não há dados reais (R$/km, R$/noite).

## Guia de Instalação e Execução

### Pré-requisitos
- Python 3.10+
- Node.js 18+ e npm
- Chave de API (opcional, para autocomplete de aeroportos)

## Cenários de Teste Sugeridos

Para verificar a integração com os dados locais (`backend/data`), tente os seguintes roteiros:

### 1. Viagem Rio-SP (Dados Completos)
- **Origem**: Rio de Janeiro (SDU)
- **Destino**: São Paulo (GRU)
- **Data**: Daqui a 30 dias
- **Resultado Esperado**:
    - Deve mostrar opções de **Carro** com custo baseado em distâncias reais (~400km).
    - Deve mostrar hotéis específicos em SP com nomes reais (do JSON).

### 2. Roteiro Multi-Cidades (Sudeste)
- **Origem**: Campinas (VCP)
- **Destino**: Rio de Janeiro (GIG)
- **Parada**: Belo Horizonte (CNF) - Mínimo 2 dias
- **Resultado Esperado**:
    - Otimização de múltiplos trechos.
    - Se houver conexão direta de carro cadastrada (ex: VCP->CNF), usará; caso contrário, usará a estimativa (Haversine).

### 3. Rota sem Dados Específicos (Fallback)
- **Origem**: Curitiba (CWB) - *Cidade não está no JSON de hotéis*
- **Destino**: Florianópolis (FLN)
- **Resultado Esperado**:
    - O sistema funcionará normalmente, mas usará **dados simulados (Mock)** para hotéis e carros, pois essas cidades não estão na base de dados de exemplo.

### 4. Voo Internacional (Dados do JSON)
- **Origem**: Goiânia (GYN)
- **Destino**: Miami (MIA)
- **Data**: 01/05/2026 (Qualquer data futura)
- **Resultado Esperado**:
    - Deve encontrar voo direto com preço base próximo a **R$ 500** (valor do `voos.json`), com pequena variação aleatória simulada.
    - Detalhes do voo indicarão "Source: JSON Data".

### 5. Voo Doméstico Caro (Exemplo VCP->GIG)
- **Origem**: Campinas (VCP)
- **Destino**: Rio de Janeiro (GIG)
- **Data**: 15/06/2026
- **Resultado Esperado**:
    - Preço base próximo a **R$ 2000** (conforme `voos.json`), bem mais caro que a média, refletindo o dado estático.

### 1. Configurar o Backend

1.  Entre na pasta `backend`:
    ```bash
    cd backend
    ```
2.  Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # ou venv\Scripts\activate no Windows
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Inicie o servidor API:
    ```bash
    uvicorn main:app --reload --port 8001
    ```
    O backend estará rodando em `http://localhost:8001`.

### 2. Configurar o Frontend

1.  Entre na pasta `frontend` (em novo terminal):
    ```bash
    cd frontend
    ```
2.  Instale as dependências:
    ```bash
    npm install
    ```
3.  Inicie a aplicação:
    ```bash
    npm run dev
    ```
4.  Acesse `http://localhost:3000` no navegador.

## Solução de Problemas

- **Erro de Conexão**: Certifique-se de que o backend está rodando na porta 8001 e o frontend na 3000.
- **Dados "estranhos"**: Se você buscar rotas não cobertas pelos arquivos JSON em `backend/data`, o sistema gerará dados simulados (mock) para garantir que o fluxo não quebre.

