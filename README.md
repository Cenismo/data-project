# data-project
'''mermaid
graph TD;
    A[Início] --> B[Buscar Dados de Commodities]
    B --> C[Consolidar Dados de Todas as Commodities]
    C --> D[Transformar e Preparar Dados]
    D --> E[Carregar Dados no PostgreSQL]
    E --> F[Fim]

    subgraph Extrair
        B1[buscar_dados_decommodities]
        B2[buscar_todos_dados_commodities]
        B --> B1
        B1 --> B2
    end

    subgraph Transformar
        C1[Concatenar Todos os Dados]
        C2[Preparar DataFrame para Carregamento]
        B2 --> C1
        C1 --> C2
    end

    subgraph Carregar
        D1[salvar_no_postgres]
        C2 --> D1
    end

    B --> B2
    B2 --> C1
    C1 --> C2
    C2 --> D1
    D1 --> E
'''