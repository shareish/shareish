{% extends "mail_templated/base.tpl" %}
{% load my_filters %}

{% block subject %}
    [Shareish] {{ digest }} for Shareish mutual aid platform ({{ n }} new item{% if n != 1 %}s{% endif %})
{% endblock %}

{% block text %}
    Dear {{ user.first_name }} {{ user.last_name }} (@{{ user.username }}),{{ text|linebreaks }}
    {{ text|linebreaks }}
    There is new content within your neighbourhood on Shareish mutual aid platform.{{ text|linebreaks }}
    {{ text|linebreaks }}
    Last {% if n > to_show %}{{ to_show }}{% endif %} item{% if n != 1 %}s{% endif %} published:{{ text|linebreaks }}
    {% for item in new_items %}
        - {{ item_types|get_key:item.item_type }}: {{ item.name }}, at {{ item.distance.km|floatformat:2 }}km ({{ app_url }}/items/{{ item.id }}){{ text|linebreaks }}
    {% endfor %}
    {% if n > to_show %}
        {{ text|linebreaks }}
        There is {{ n|sub:to_show }} more item{% if n|sub:to_show != 1 %}s{% endif %} waiting for you on the website!{{ text|linebreaks }}
    {% endif %}
    {{ text|linebreaks }}
    Please login on {{ app_url }} to view {% if n != 1 %}{% if n > to_show %}all of {% endif %}them{% else %}it{% endif %}.{{ text|linebreaks }}
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

    p {
        display: block;
        margin-top: 1em;
        margin-bottom: 1em;
        margin-left: 0;
        margin-right: 0;
    }
    </style>
    <p>Dear {{ user.first_name }} {{ user.last_name }} (@{{ user.username }}),</p>
    <p>There is new content within your neighbourhood on Shareish mutual aid platform.</p>
    <p>Last {% if n > to_show %}{{ to_show }}{% endif %} item{% if n != 1 %}s{% endif %} published:</p>
    <ul>
        {% for item in new_items %}
            <li><span class="type">{{ item_types|get_item:item.item_type }}</span><a href='{{ app_url }}/items/{{ item.id }}'>{{ item.name }}</a>, at {{ item.distance.km|floatformat:2 }}km</li>
        {% endfor %}
    </ul>
    {% if n > to_show %}
        <p>There is {{ n|sub:to_show }} more item{% if n|sub:to_show != 1 %}s{% endif %} waiting for you on the website!</p>
    {% endif %}
    <p>Please login on <a href='{{ app_url }}'>{{ app_url }}</a> to view {% if n != 1 %}{% if n > to_show %}all of {% endif %}them{% else %}it{% endif %}.</p>
    <p>The Shareish team.</p>
    <p><small><i>These notifications can be configured or opt-out in the <a href='{{ app_url }}/settings/notifications'>settings tab</a>.</i></small></p>
{% endblock %}