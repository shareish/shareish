{% extends "mail_templated/base.tpl" %}
{% load my_filters %}

{% block subject %}
    [Shareish] New message received on Shareish mutual aid platform!
{% endblock %}

{% block text %}
    Dear {{ receiver.first_name }} {{ receiver.last_name }} ({{ receiver.username }}),{{ text|linebreaks }}
    {{ text|linebreaks }}
    Someone just sent you a message and is waiting for your answer on Shareish mutual aid platform.{{ text|linebreaks }}
    {{ text|linebreaks }}
    ({{ conversation.slug }}): {{ message_content|ellipsis:80 }} @ {{ app_url }}/conversations/{{ conversation.id }}{{ text|linebreaks }}
    {{ text|linebreaks }}
    Please login on {{ app_url }} to view it.{{ text|linebreaks }}
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
    <p>Dear {{ receiver.first_name }} {{ receiver.last_name }} ({{ receiver.username }}),</p>
    <p>Someone just sent you a message and is waiting for your answer on Shareish mutual aid platform.</p>
    <ul>
        <li>
            <a href='{{ app_url }}/conversations/{{ conversation.id }}'>{{ conversation.slug }}</a><br />
            {{ message_content|ellipsis:80 }}
        </li>
    </ul>
    <p>Please login on <a href='{{ app_url }}'>{{ app_url }}</a> to view it.</p>
    <p>The Shareish team.</p>
    <p><small><i>These notifications can be configured or opt-out in the <a href='{{ app_url }}/settings/notifications'>settings tab</a>.</i></small></p>
{% endblock %}