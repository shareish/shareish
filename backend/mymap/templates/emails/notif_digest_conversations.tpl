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
    Please login on {{ app_url }} to view them.{{ text|linebreaks }}
    {{ text|linebreaks }}
    The Shareish team.{{ text|linebreaks }}
    {{ text|linebreaks }}
    These notifications can be configured or opt-out in the settings tab ({{ app_url }}/settings/notifications).
{% endblock %}

{% block html %}
    Dear {{ user.first_name }} {{ user.last_name }} ({{ user.username }}),<br /><br />

    Some people are waiting for your answer on Shareish mutual aid platform.<br /><br />

    You have {{ n }} unread message{% if n != 1 %}s{% endif %} available in the <a href='{{ app_url }}/conversations'>conversations tab</a>.<br /><br />

    Please login on <a href='{{ app_url }}'>{{ app_url }}</a> to view them.<br /><br />

    The Shareish team.<br /><br />

    <small><i>These notifications can be configured or opt-out in the <a href='{{ app_url }}/settings/notifications'>settings tab</a>.</i></small>
{% endblock %}