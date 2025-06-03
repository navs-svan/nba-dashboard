{#
    This macro concatenates team and id to create a relationship
#}

{% macro create_id(team, date) %}

    CONCAT(
        CAST({{ team }} AS STRING),
        '_',
        FORMAT_DATE('%Y-%m-%d', {{ date }})
    )

{% endmacro %}
