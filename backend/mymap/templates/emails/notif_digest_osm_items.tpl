{% extends "mail_templated/base.tpl" %}
{% load my_filters %}

{% block subject %}
    [Shareish] {{ digest }} for Shareish mutual aid platform ({{ n }} new public resource{% if n != 1 %}s{% endif %})
{% endblock %}

{% block body %}
    Dear {{ user.first_name }} {{ user.last_name }} (@{{ user.username }}),{{ text|linebreaks }}
    {{ text|linebreaks }}
    New public resource{% if n != 1 %}s{% endif %} are visible within your neighbourhood on Shareish mutual aid platform:{{ text|linebreaks }}
    {% for item in new_items %}
        {{ item.0 }} {{ item.1 }}  ({{ app_url }}/map/pos/{{ item.3 }}/{{ item.4 }}) at {{ item.2|floatformat:2 }} km
    {% endfor %}
    {{ text|linebreaks }}
    
    Please click on the above links or login on {{ app_url }} and zoom to view them.{{ text|linebreaks }}
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
    <p>New public resource{% if n != 1 %}s{% endif %} are visible within your neighbourhood on Shareish mutual aid platform:{{ text|linebreaks }}</p>
    <ul>
        {% for item in new_items %}
        <li> <a href='{{ app_url }}/map/pos/{{ item.3 }}/{{ item.4 }}'>{{ item.0 }} {{ item.1 }} </a> at {{ item.2|floatformat:2 }} km</li>
         {% endfor %}
    </ul>
    <p>Please click on the above links or login on <a href='{{ app_url }}'>{{ app_url }}</a> and zoom to view them.{{ text|linebreaks }}</p>
    <p>The Shareish team.</p>
    <p><small><i>These notifications can be configured or opt-out in the <a href='{{ app_url }}/settings/notifications'>settings tab</a>.</i></small></p>
{% endblock %}