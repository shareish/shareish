{% extends "mail_templated/base.tpl" %}
{% load my_filters %}

{% block subject %}
    [Shareish] A new event just got published on Shareish mutual aid platform!
{% endblock %}

{% block text %}
    Dear {{ user.first_name }} {{ user.last_name }} (@{{ user.username }}),{{ text|linebreaks }}
    {{ text|linebreaks }}
    A new event just got published within your neighbourhood on Shareish mutual aid platform.{{ text|linebreaks }}
    {{ text|linebreaks }}
    - {{ event.name }}, at {{ user.distance_from_event.km|floatformat:2 }}km ({{ app_url }}/items/{{ event.id }}){{ text|linebreaks }}
    {{ text|linebreaks }}
    Please login on {{ app_url }} to view it.{{ text|linebreaks }}
    {{ text|linebreaks }}
    The Shareish team.{{ text|linebreaks }}
    {{ text|linebreaks }}
    These notifications can be configured or opt-out in the settings tab ({{ app_url }}/settings/notifications).
{% endblock %}

{% block html %}
    <style>
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
    <p>A new event just got published within your neighbourhood on Shareish mutual aid platform.</p>
    <ul>
        <li><a href='{{ app_url }}/items/{{ event.id }}'>{{ event.name }}</a>, at {{ user.distance_from_event.km|floatformat:2 }}km</li>
    </ul>
    <p>Please login on <a href='{{ app_url }}'>{{ app_url }}</a> to view it.</p>
    <p>The Shareish team.</p>
    <p><small><i>These notifications can be configured or opt-out in the <a href='{{ app_url }}/settings/notifications'>settings tab</a>.</i></small></p>
{% endblock %}
