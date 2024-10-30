-- import

WITH source as (
    SELECT
        "Date",
        "Close",
        simbolo
    from 
        {{ source ('datapablo', 'commodities')}}     
),

-- renamed
renamed as (
    SELECT
        CAST("Date" as date) as data,
        "Close" as valor_fechamento,
        simbolo
    FROM
        source
)
-- select * from

SELECT * FROM renamed