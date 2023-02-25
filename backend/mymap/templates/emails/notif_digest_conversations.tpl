{% extends "mail_templated/base.tpl" %}

{% block subject %}
    [Shareish] {{ digest }} for Shareish mutual aid platform ({{ n }} new item{% if n != 1 %}s{% endif %}
{% endblock %}

{% block text %}
    Dear {{ user.first_name }} {{ user.last_name }} ({{ user.username }}),{{ text|linebreaks }}
    {{ text|linebreaks }}
    Some people are waiting for your answer on Shareish mutual aid platform.{{ text|linebreaks }}
    {{ text|linebreaks }}
    You have {{ n }} unread message{% if n != 1 %}s{% endif %} available in the conversations tab ({{ app_url }}/conversations).
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

    p {
        display: block;
        margin-top: 1em;
        margin-bottom: 1em;
        margin-left: 0;
        margin-right: 0;
    }
    </style>
    <p>Dear {{ user.first_name }} {{ user.last_name }} ({{ user.username }}),</p>
    <p>Some people are waiting for your answer on Shareish mutual aid platform.</p>
    <p>You have {{ n }} unread message{% if n != 1 %}s{% endif %} available in the <a href='{{ app_url }}/conversations'>conversations tab</a>.</p>
    <ul>
        {% for message in unread_messages %}
            <li>
                <a href='{{ app_url }}/conversations/{{ message.conversation.id }}'>{{ message.conversation.slug }}</a><br />
                {{ message.content|ellipsis:80 }}
            </li>
        {% endfor %}
    </ul>
    {% if n > to_show %}
        <p>You have {{ n|sub:to_show }} more message{% if n|sub:to_show != 1 %}s{% endif %} to check on the website!</p>
    {% endif %}
    <p>Please login on <a href='{{ app_url }}'>{{ app_url }}</a> to view {% if n != 1 %}{% if n > to_show %}all of {% endif %}them{% else %}it{% endif %}.</p>
    <p>The Shareish team.</p>
    <p><small><i>These notifications can be configured or opt-out in the <a href='{{ app_url }}/settings/notifications'>settings tab</a>.</i></small></p>
{% endblock %}