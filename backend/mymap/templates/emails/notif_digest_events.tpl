{% extends "mail_templated/base.tpl" %}

{% block subject %}
    [Shareish] {{ digest }} for Shareish mutual aid platform ({{ n }} new event{% if n != 1 %}s{% endif %})
{% endblock %}

{% block text %}
    Dear {{ user.first_name }} {{ user.last_name }} ({{ user.username }}),{{ text|linebreaks }}
    {{ text|linebreaks }}
    There is new content within your neighbourhood on Shareish mutual aid platform.{{ text|linebreaks }}
    {{ text|linebreaks }}
    Last {% if n > to_show %}{{ to_show }}{% endif %} event{% if n != 1 %}s{% endif %} publised:{{ text|linebreaks }}
    {% for event in new_events %}
        - {{ event.name }}, in {{ event.delay }} days, at {{ event.distance.km|floatformat:2 }}km ({{ app_url }}/items/{{ event.id }}){{ text|linebreaks }}
    {% endfor %}
    {% if n > to_show %}
        {{ text|linebreaks }}
        There is {{ n|sub:to_show }} more event{% if n|sub:to_show != 1 %}s{% endif %} waiting for you on the website!{{ text|linebreaks }}
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
    </style>
    Dear {{ user.first_name }} {{ user.last_name }} ({{ user.username }}),<br /><br />

    There is new content within your neighbourhood on Shareish mutual aid platform.<br /><br />

    Last {% if n > to_show %}{{ to_show }}{% endif %} event{% if n != 1 %}s{% endif %} publised:<br />
    <ul>
        {% for event in new_events %}
            <li><a href='{{ app_url }}/items/{{ event.id }}'>{{ event.name }}</a>, in {{ event.delay }} days, at {{ event.distance.km|floatformat:2 }}km</li>
        {% endfor %}
    </ul>
    <br />
    {% if n > to_show %}
        There is {{ n|sub:to_show }} more event{% if n|sub:to_show != 1 %}s{% endif %} waiting for you on the website!<br /><br />
    {% endif %}

    Please login on <a href='{{ app_url }}'>{{ app_url }}</a> to view {% if n != 1 %}them{% else %}it{% endif %}.<br /><br />

    The Shareish team.<br /><br />

    <small><i>These notifications can be configured or opt-out in the <a href='{{ app_url }}/settings/notifications'>settings tab</a>.</i></small>
{% endblock %}