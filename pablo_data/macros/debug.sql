-- macros/debug.sql

{% macro debug_commodities() %}
    SELECT
        data,
        simbolo,
        valor_fechamento
    FROM {{ ref('stg_commodities') }}
{% endmacro %}
