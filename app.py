import streamlit as st
import pandas as pd
import psycopg2  # O conector oficial do PostgreSQL!
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA (Sempre o primeiro comando do Streamlit)
st.set_page_config(page_title="Executive Dashboard - PostgreSQL", layout="wide")

# 2. FUNÇÃO PARA CONECTAR E BUSCAR OS DADOS DO POSTGRESQL
@st.cache_data
def buscar_dados_postgres():
    conexao = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="SUA_SENHA_AQUI",  
        port="5432"
    )
    conexao.set_client_encoding('WIN1252')
    
    # Adicionamos o cliente e a categoria na nossa busca SQL
    query = """
        SELECT data_venda, valor_total, produto, cliente, categoria 
        FROM fat_vendas 
        WHERE status_nota = 'EMITIDA'
    """
    
    df = pd.read_sql(query, con=conexao)
    conexao.close()
    
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    return df

# Tratamento de erro estruturado
try:
    df_vendas = buscar_dados_postgres()
    
    # =========================================================================
    # 3. BARRA LATERAL (FILTROS INTERATIVOS)
    # =========================================================================
    st.sidebar.header("🎯 Painel de Filtros")

    # Filtro 1: Produtos (Multiselect)
    produtos_disponiveis = df_vendas['produto'].unique()
    filtro_produto = st.sidebar.multiselect("Selecione os Produtos:", options=produtos_disponiveis, default=produtos_disponiveis)

    # Filtro 2: Período (Calendário Dinâmico)
    data_minima = df_vendas['data_venda'].min().date()
    data_maxima = df_vendas['data_venda'].max().date()
    filtro_data = st.sidebar.date_input("Selecione o Período:", value=(data_minima, data_maxima), min_value=data_minima, max_value=data_maxima)

    # Aplicando os filtros no DataFrame
    df_filtrado = df_vendas[df_vendas['produto'].isin(filtro_produto)]


    if isinstance(filtro_data, tuple) and len(filtro_data) == 2:
        data_inicio, data_fim = filtro_data
        df_filtrado = df_filtrado[(df_filtrado['data_venda'].dt.date >= data_inicio) & (df_filtrado['data_venda'].dt.date <= data_fim)]


    # =========================================================================
    # 4. CABEÇALHO E CARDS DE INDICADORES (KPIs)
    # =========================================================================
    st.title("📊 Dashboard Executivo de Inteligência de Negócios")
    st.markdown("Indicadores corporativos integrados nativamente ao banco de dados PostgreSQL.")
    st.write("---")

    # Cálculos das métricas operacionais
    faturamento_total = df_filtrado['valor_total'].sum()
    total_pedidos = df_filtrado.shape[0]
    ticket_medio = faturamento_total / total_pedidos if total_pedidos > 0 else 0.0

    # Criando 3 colunas para os Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💰 Faturamento Total", value=f"R$ {faturamento_total:,.2f}")
    with col2:
        st.metric(label="📦 Total de Pedidos", value=total_pedidos)
    with col3:
        st.metric(label="📈 Ticket Médio por Venda", value=f"R$ {ticket_medio:,.2f}")

    st.write("---")


    # =========================================================================
    # 5. BLOCO DE GRÁFICOS (LINHA E ROSCA)
    # =========================================================================
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Evolução de Vendas no Tempo")
        df_tempo = df_filtrado.groupby('data_venda')['valor_total'].sum().reset_index()
        fig_linha = px.line(df_tempo, x='data_venda', y='valor_total', title="Faturamento por Data", markers=True)
        st.plotly_chart(fig_linha, width="stretch")

    with col5:
        st.subheader("Share de Faturamento por Cliente")
        df_cliente = df_filtrado.groupby('cliente')['valor_total'].sum().reset_index()
        # Criando o gráfico de pizza e transformando em rosca usando o parâmetro 'hole'
        fig_rosca = px.pie(df_cliente, values='valor_total', names='cliente', title="Participação por Comprador", hole=0.4)
        st.plotly_chart(fig_rosca, width="stretch")

    st.write("---")


    # =========================================================================
    # 6. BLOCO INFERIOR (BARRAS E TABELA DE CONSOLIDAÇÃO)
    # =========================================================================
    col6, col7 = st.columns(2)

    with col6:
        st.subheader("Faturamento por Produto")
        df_prod = df_filtrado.groupby('produto')['valor_total'].sum().reset_index()
        fig_barra = px.bar(df_prod, x='produto', y='valor_total', title="Volume Financeiro por Item", color='produto')
        st.plotly_chart(fig_barra, width="stretch")

    with col7:
        st.subheader("📋 Dados Consolidados")
        # Exibe uma tabela limpa e interativa com os dados que estão gerando os gráficos acima
        st.dataframe(df_filtrado, hide_index=True, use_container_width=True)

except Exception as e:
    st.error("❌ Erro de Conexão ou Leitura no PostgreSQL")
    st.code(str(e))