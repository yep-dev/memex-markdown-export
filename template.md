---
title: "{{title}}"
date: {{date}}
slug: "/{{slug}}"
tags:{% for tag in tags %}
  - {{tag}}{% endfor %}
---
# {{title}}

https://{{url}}

-{% for annotation in annotations -%}--
{% if annotation.comment %}_{{annotation.comment}}_ {% endif %}{{annotation.body}}^{{annotation.id}}

-   
{%- endfor -%} 