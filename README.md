# data-project

```mermaid
graph TD;
    A[Início] --> B[Extrair Dados de Commodities]
    B --> C[Consolidar e Preparar Dados]
    C --> D[Carregar Dados no PostgreSQL]
    D --> E[Fim]

    subgraph Extrair
        B1[buscar_dados_decommodities]
        B2[buscar_todos_dados_commodities]
        B --> B1 --> B2
    end

    subgraph Transformar
        C1[Concatenar Dados]
        C2[Formatar para Carregamento]
        B2 --> C1 --> C2
    end

    subgraph Carregar
        D1[salvar_no_postgres]
        C2 --> D1
    end
