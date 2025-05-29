{#
    This macro converts the datatype of minutes column from string to decimal
#}

{% macro convert_minutes(minutes) %}

    CASE {{ minutes }}
        WHEN '0 hours 0 minutes 0 seconds' THEN 0.0
        ELSE 
            (
            CAST(SPLIT(minutes, ':')[OFFSET(0)] AS INT64) * 60     -- hours to minutes
            + CAST(SPLIT(minutes, ':')[OFFSET(1)] AS INT64) * 1      -- minutes
            + CAST(SPLIT(minutes, ':')[OFFSET(2)] AS FLOAT64) / 60.0
            )   -- seconds to fractional minutes
    END

{% endmacro %}
