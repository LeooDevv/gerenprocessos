# 🧠 Simulador de Algoritmos de Escalonamento de Tarefas

### 📌 Objetivo  
Este projeto tem como objetivo simular o comportamento de diferentes algoritmos de escalonamento de tarefas, calcular os tempos médios de **execução** e **espera**, além de gerar uma visualização em linha do tempo da execução das tarefas.

---

## 🧩 Etapas da Simulação

### 1. Definição de Tarefas  
Cada tarefa possui os seguintes atributos:

- **Nome** (ex: T1, T2, ...)
- **Tempo de chegada** (quando entra na fila)
- **Duração** (tempo total de execução)
- **Prioridade** (quanto menor o número, maior a prioridade)

**Exemplo de entrada:**

| Tarefa | Chegada | Duração | Prioridade |
|--------|---------|---------|------------|
| T1     | 0       | 5       | 2          |
| T2     | 0       | 2       | 3          |
| T3     | 1       | 4       | 1          |
| T4     | 3       | 1       | 4          |
| T5     | 5       | 2       | 5          |

---

### 2. Algoritmos de Escalonamento Implementados

- **FCFS** – First Come First Served  
- **RR** – Round Robin (com quantum ajustável, ex: 2s)  
- **SJF** – Shortest Job First  
- **SRTF** – Shortest Remaining Time First  
- **PRIOc** – Prioridade Cooperativa  
- **PRIOp** – Prioridade Preemptiva  

---

### 3. Cálculo dos Tempos

- **Tempo de execução (turnaround)** = término - chegada  
- **Tempo de espera** = turnaround - duração  
- Suporte a tempo de **troca de contexto** opcional (ex: 0.5s ou 1s)

---

### 4. Geração do Diagrama de Escalonamento

Visualização gráfica da execução na linha do tempo, com marcações para:

- Tarefas executadas
- Trocas de contexto (representadas como `CTX`)

---

## 💡 Funcionalidades Extras

- Versão manual em **planilha** (Excel ou Google Sheets)  
- Versão interativa em **Python** (interface no terminal ou Jupyter Notebook)  
- Geração de **gráficos de Gantt** com `matplotlib` ou outras bibliotecas  
- Comparação dos **tempos médios** entre os algoritmos  
- Discussões sobre a **adequação de algoritmos** em diferentes contextos:  
  - Sistemas embarcados  
  - Servidores web  
  - Ambientes de tempo real  

---

## 🛠️ Tecnologias

- Python 3.x  
- Jupyter Notebook (opcional)  
- matplotlib  
- pandas  

---

## 📬 Contato

Se quiser trocar uma ideia ou entender melhor o projeto:

--[🔗 LnkedIn](https://www.linkedin.com/in/daviteramoto/)
---[🔗 LnkedIn](https://www.linkedin.com/in/gustavo-henrique-portari-300b05205/)
---[🔗 LnkedIn](https://www.linkedin.com/in/jo%C3%A3o-vitor-antunes-nascimento/)
---[🔗 LnkedIn](https://www.linkedin.com/in/leonardo-rodrigues-471a611b8/)
