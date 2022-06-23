---
title: "{{title}}"
date: {{date}}
slug: "/{{slug}}"
---
# {{title}}

https://{{url}}

-{% for annotation in annotations -%}--
{% if annotation.comment %}_{{annotation.comment}}_ {% endif %}{{annotation.body}}^{{annotation.id}}

-   
{%- endfor -%} 