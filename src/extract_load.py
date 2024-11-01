# Imports
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Import das variáveis de ambiente
commodities = ['CL=F', 'GC=F', 'SI=F']

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def buscar_dados_decommodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_dados_commodities():
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_decommodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

def salvar_no_postgres(df, schema='public'):
    # Conexão com o banco para remover as views e a tabela antes de recriar
    with engine.connect() as conn:
        # Remover as views dependentes com CASCADE
        conn.execute(text("DROP VIEW IF EXISTS public.dm_commodities CASCADE"))
        conn.execute(text("DROP VIEW IF EXISTS public.stg_commodities CASCADE"))
        
        # Remover a tabela commodities com CASCADE
        conn.execute(text("DROP TABLE IF EXISTS public.commodities CASCADE"))

    # Inserir a nova tabela commodities
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Date', schema=schema)

    # Recriar as views depois de substituir a tabela
    with engine.connect() as conn:
        # Exemplo das definições das views (substitua pelos comandos SQL reais)
        conn.execute(text("CREATE VIEW public.stg_commodities AS SELECT * FROM public.commodities"))
        conn.execute(text("CREATE VIEW public.dm_commodities AS SELECT * FROM public.stg_commodities"))

if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_commodities()
    salvar_no_postgres(dados_concatenados, schema=DB_SCHEMA or 'public')
