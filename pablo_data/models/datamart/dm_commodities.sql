WITH movimentacao AS (
  SELECT
    data,
    simbolo,
    acao,
    quantidade
  FROM
    {{ ref('stg_movimentacao_commodities') }}
),
preco_aproximado AS (
  SELECT
    m.*,
    c.data AS data_commodity,
    c.valor_fechamento
  FROM
    movimentacao m
  JOIN LATERAL (
    SELECT
      c1.data,
      c1.valor_fechamento
    FROM
      {{ ref('stg_commodities') }} c1
    WHERE
      LOWER(TRIM(c1.simbolo)) = LOWER(TRIM(m.simbolo))
      AND c1.data >= m.data
    ORDER BY
      c1.data ASC
    LIMIT 1
  ) c ON TRUE
),
calculado AS (
  SELECT
    data_commodity AS data,
    simbolo,
    valor_fechamento,
    acao,
    quantidade,
    (quantidade * valor_fechamento) AS valor,
    CASE
      WHEN acao = 'sell' THEN (quantidade * valor_fechamento)
      WHEN acao = 'buy' THEN -(quantidade * valor_fechamento)
      ELSE 0
    END AS ganho
  FROM
    preco_aproximado
)
SELECT
  *
FROM
  calculado
