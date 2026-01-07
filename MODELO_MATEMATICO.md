# Especificação do Modelo Matemático

Este documento descreve a modelagem formal utilizada no **Travel Planner** para resolver o problema de seleção de roteiros. O sistema emprega Programação Linear Inteira Mista (MILP) para determinar a estratégia de viagem mais eficiente, balanceando custos de transporte, hospedagem e aluguel de veículos.

## Visão Geral

O problema consiste em selecionar um trajeto entre uma **Origem ($O$)** e um **Destino ($D$)**, optando por uma dentre três modalidades de transporte:
1.  **Aéreo**: Viagem completa por avião.
2.  **Rodoviário**: Viagem completa por carro.
3.  **Híbrido**: Combinação de carro até um aeroporto intermediário, voo, e carro no destino.

O objetivo central é minimizar a função de custo global $C_{total}$, sujeita a restrições operacionais e lógicas.

---

## 1. Definições e Parâmetros do Sistema

Abaixo estão listados os parâmetros de entrada e conjuntos utilizados na formulação.

### Dados Geográficos e de Infraestrutura
*   **Locais Principais**: $O$ (Origem), $D$ (Destino).
*   **Aeroportos/Cidades de Conexão**:
    *   $C_{orig}$: Aeroportos acessíveis a partir da origem.
    *   $C_{dest}$: Aeroportos acessíveis próximos ao destino.
*   **Serviços Disponíveis**:
    *   $H_{dest}$: Lista de hotéis na região de destino.
    *   $L_{orig}$: Locadoras de veículos na região de origem.
    *   $L_{dest}$: Locadoras de veículos na região de destino.

### Parâmetros de Custo e Tempo
| Parâmetro | Definição |
| :--- | :--- |
| $N_{pax}$ | Número de viajantes |
| $D_{viagem}$ | Duração total da estadia (em dias) |
| $ \alpha_{voo}(i,j) $ | Preço da passagem aérea entre $i$ e $j$ (unitário) |
| $ \delta(i,j) $ | Distância rodoviária entre $i$ e $j$ (km) |
| $ \beta_{km} $ | Custo operacional rodoviário (R$/km) |
| $ \gamma_{hotel}(h) $ | Diária do hotel $h$ |
| $ \rho_{carro}(l) $ | Diária de locação de veículo na locadora $l$ |

---

## 2. Variáveis de Decisão

O modelo utiliza variáveis binárias ($v \in \{0,1\}$) para representar as escolhas exclusivas do sistema.

### Modalidade de Transporte
Definem a estrutura macro da viagem:
*   $y_{AR}$: Rota estritamente Aérea.
*   $y_{RD}$: Rota estritamente Rodoviária.
*   $y_{HB}$: Rota Híbrida (Carro + Avião + Carro).

### Pontos de Conexão (Apenas para Rota Híbrida)
*   $x_{partida}(i)$: Indica se a cidade $i \in C_{orig}$ é o ponto de partida do voo.
*   $x_{chegada}(j)$: Indica se a cidade $j \in C_{dest}$ é o ponto de chegada do voo.

### Serviços Complementares
*   $z_{hosp}(h)$: Seleção do hotel $h \in H_{dest}$.
*   $w_{loc\_orig}(l)$: Seleção da locadora $l \in L_{orig}$ (usado nas rotas Rodoviária ou Híbrida/Origem).
*   $w_{loc\_dest}(l)$: Seleção da locadora $l \in L_{dest}$ (usado na rota Híbrida/Destino).

---

## 3. Função Objetivo

A função a ser minimizada é o Custo Total, composto por três grandes componentes:

$$ \text{Min } Z = \text{Custo}_{transp} + \text{Custo}_{hosp} + \text{Custo}_{loc} $$

### Componentes

**1. Transporte ($ \text{Custo}_{transp} $)**
Engloba passagens aéreas e custos de combustível/deslocamento terrestre.

$$
\begin{aligned}
\text{Custo}_{transp} = & \left[ \alpha_{voo}(O, D) \cdot N_{pax} \cdot y_{AR} \right] + \\
                        & \left[ \delta(O, D) \cdot \beta_{km} \cdot y_{RD} \right] + \\
                        & \underbrace{\sum_{i \in C_{orig}} \sum_{j \in C_{dest}} \left( \alpha_{voo}(i, j) \cdot N_{pax} \cdot \mu_{ij} \right)}_{\text{Custo Aéreo na Rota Híbrida}}
\end{aligned}
$$
*Nota: $\mu_{ij}$ é uma variável auxiliar linearizada que representa a escolha do trecho aéreo $i \to j$ na rota híbrida.*

**2. Hospedagem ($ \text{Custo}_{hosp} $)**
$$ \text{Custo}_{hosp} = \sum_{h \in H_{dest}} \gamma_{hotel}(h) \cdot D_{viagem} \cdot z_{hosp}(h) $$

**3. Locação de Veículos ($ \text{Custo}_{loc} $)**
Considera aluguel na origem (para viagem de carro) ou nas pontas (para viagem híbrida).

$$
\begin{aligned}
\text{Custo}_{loc} = & \sum_{l \in L_{orig}} \rho_{carro}(l) \cdot D_{viagem} \cdot w_{loc\_orig}(l) \cdot y_{RD} \hspace{2mm} + \\
                     & \sum_{l \in L_{dest}} \rho_{carro}(l) \cdot D_{viagem} \cdot w_{loc\_dest}(l) \cdot y_{HB}
\end{aligned}
$$

---

## 4. Restrições do Modelo

As restrições garantem a consistência lógica da solução encontrada.

**R1. Exclusividade de Modalidade**
Deve-se escolher exatamente um tipo de transporte principal.
$$ y_{AR} + y_{RD} + y_{HB} = 1 $$

**R2. Consistência da Rota Híbrida**
Se a modalidade Híbrida for ativa ($y_{HB}=1$), o sistema deve selecionar um par único de aeroportos (origem e destino).
$$ \sum_{i \in C_{orig}} x_{partida}(i) = y_{HB} $$
$$ \sum_{j \in C_{dest}} x_{chegada}(j) = y_{HB} $$

**R3. Obrigatoriedade de Hospedagem**
O usuário deve ter uma (e apenas uma) opção de hospedagem no destino.
$$ \sum_{h \in H_{dest}} z_{hosp}(h) = 1 $$

**R4. Vinculação de Locadora (Origem)**
Se a viagem for feita inteiramente de carro, uma locadora na origem deve ser alocada.
$$ \sum_{l \in L_{orig}} w_{loc\_orig}(l) = y_{RD} $$

**R5. Vinculação de Locadora (Destino)**
Se a viagem for híbrida, um carro é necessário no destino final.
$$ \sum_{l \in L_{dest}} w_{loc\_dest}(l) = y_{HB} $$

### Linearização (Técnica Big-M)

Para resolver o produto de variáveis binárias no custo de transporte híbrido (que tornaria o modelo não-linear), utilizamos a variável auxiliar $\mu_{ij}$ com as seguintes restrições lógicas:

Para todo par $i, j$:
1. $\mu_{ij} \le x_{partida}(i)$
2. $\mu_{ij} \le x_{chegada}(j)$
3. $\mu_{ij} \ge x_{partida}(i) + x_{chegada}(j) - 1$
4. $\sum \sum \mu_{ij} = y_{HB}$

---

Esta formulação permite que *solvers* de otimização matemática encontrem a solução global ótima de forma determinística e eficiente.
