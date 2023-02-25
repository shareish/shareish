{% extends "mail_templated/base.tpl" %}

{% block subject %}
    [Shareish] {{ digest }} for Shareish mutual aid platform ({{ n }} new item{% if n != 1 %}s{% endif %})
{% endblock %}

{% block text %}
    Dear {{ user.first_name }} {{ user.last_name }} ({{ user.username }}),{{ text|linebreaks }}
    {{ text|linebreaks }}
    There is new content within your neighbourhood on Shareish mutual aid platform.{{ text|linebreaks }}
    {{ text|linebreaks }}
    Last {% if n > to_show %}{{ to_show }}{% endif %} item{% if n != 1 %}s{% endif %} publised:{{ text|linebreaks }}
    {% for item in new_items %}
        - {{ item_types|get_item:item.item_type }}: {{ item.name }}, at {{ item.distance.km|floatformat:2 }}km ({{ app_url }}/items/{{ item.id }}){{ text|linebreaks }}
    {% endfor %}
    {% if n > to_show %}
        {{ text|linebreaks }}
        There is {{ n|sub:to_show }} more item{% if n|sub:to_show != 1 %}s{% endif %} waiting for you on the website!{{ text|linebreaks }}
    {% endif %}
    {{ text|linebreaks }}
    Please login on {{ app_url }} to view {% if n != 1 %}them{% else %}it{% endif %}.{{ text|linebreaks }}
    {{ text|linebreaks }}
    The Shareish team.{{ text|linebreaks }}
    {{ text|linebreaks }}
    These notifications can be configured or opt-out in the settings tab ({{ app_url }}/settings/notifications).
{% endblock %}

{% block html %}
    <style>
    ul li {
        margin-top: 5px;
    }

    ul li:first-child {
        margin-top: 0;
    }

    .type {
        display: inline-block;
        padding: 2px 5px;
        vertical-align: middle;
        background-color: darkgreen;
        color: white;
        border-radius: 5px;
        margin-right: 4px;
        font-size: 0.8em;
    }
    </style>
    Dear {{ user.first_name }} {{ user.last_name }} ({{ user.username }}),<br /><br />

    There is new content within your neighbourhood on Shareish mutual aid platform.<br /><br />

    Last {% if n > to_show %}{{ to_show }}{% endif %} item{% if n != 1 %}s{% endif %} publised:<br />
    <ul>
        {% for item in new_items %}
            <li><span class="type">{{ item_types|get_item:item.item_type }}</span><a href='{{ app_url }}/items/{{ item.id }}'>{{ item.name }}</a>, at {{ item.distance.km|floatformat:2 }}km</li>
        {% endfor %}
    </ul>
    <br />
    {% if n > to_show %}
        There is {{ n|sub:to_show }} more item{% if n|sub:to_show != 1 %}s{% endif %} waiting for you on the website!<br /><br />
    {% endif %}

    Please login on <a href='{{ app_url }}'>{{ app_url }}</a> to view {% if n != 1 %}them{% else %}it{% endif %}.<br /><br />

    The Shareish team.<br /><br />

    <small><i>These notifications can be configured or opt-out in the <a href='{{ app_url }}/settings/notifications'>settings tab</a>.</i></small>
{% endblock %}