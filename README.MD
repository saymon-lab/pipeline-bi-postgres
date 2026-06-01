# 📊 Dashboard de Inteligência Executiva com Python & PostgreSQL

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.4-blue.svg)](https://www.postgresql.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interface-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este projeto consiste em um ecossistema completo de **Business Intelligence (BI)** e Engenharia de Dados de ponta a ponta. A aplicação realiza a extração de dados analíticos de um banco de dados relacional **PostgreSQL**, executa o tratamento e modelagem das informações utilizando **Pandas**, e renderiza indicadores estratégicos reativos (KPIs e gráficos de market share) em um painel web dinâmico desenvolvido em **Streamlit**.

---

##  Principais Funcionalidades

- **Métricas Executivas (KPIs):** Cálculo dinâmico em tempo real de Faturamento Total, Volume de Pedidos Faturados e Ticket Médio Operacional.
- **Análise Temporal:** Gráfico interativo de evolução cronológica de faturamento utilizando Plotly Express.
- **Market Share por Cliente:** Gráfico de rosca detalhando a participação financeira e relevância de cada comprador na receita.
- **Filtros Avançados Dinâmicos:** Barra lateral que permite segmentação instantânea por tipo de produto e intervalo de datas via calendário conectado ao banco.
- **Auditoria de Dados:** Tabela nativa para visualização consolidada e conferência das transações extraídas via SQL.

---

##  Arquitetura e Fluxo de Dados

A aplicação segue o fluxo clássico de consumo de dados analíticos estruturados em ambiente corporativo:

1. **Camada de Armazenamento:** PostgreSQL gerenciando a tabela `fat_vendas`.
2. **Camada de Conexão:** Driver `psycopg2` realizando o handshake local e forçando codificação segura para o ecossistema Windows (`WIN1252`).
3. **Camada de ETL & Computação:** Pandas executando queries de agregação (`GROUP BY`), filtros de data (`.dt.date`) e tratamento de nulos.
4. **Camada de Apresentação:** Streamlit servindo os componentes visuais de forma assíncrona.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem Principal:** Python 3
- **Banco de Dados Relacional:** PostgreSQL + DBeaver (Interface de Gerenciamento)
- **Manipulação e Análise de Dados:** Pandas
- **Driver do Banco de Dados:** Psycopg2-binary
- **Visualização de Dados Interativa:** Plotly Express
- **Framework de Interface Web:** Streamlit

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
Certifique-se de ter o **Python 3** instalado em sua máquina e uma instância do **PostgreSQL** ativa com a tabela `fat_vendas` criada (conforme os scripts SQL contidos na pasta).
