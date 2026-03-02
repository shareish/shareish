{% extends "mail_templated/base.tpl" %}
{% load i18n %}

{% block subject %}{% trans "[Shareish] Recover your account" %}{% endblock %}

{% block text %}
{% blocktrans with name=user.first_name %}Dear {{ name }},{% endblocktrans %}

{% trans "We have received a request to recover your account. If you made this request, please click the link below to recover your account:" %}

{{ recover_account_token_url }}

{% trans "If you did not make this request, you can safely ignore this email. Your account is safe and secure, and no unauthorized parties have gained access to your account or password." %}

{% trans "Best regards," %}
{% trans "The Shareish team." %}
{% endblock %}

{% block html %}
    <style>
        body { font-family: Arial, sans-serif; font-size: 16px; line-height: 1.5; color: #333; }
        a { color: #3eaf7c; text-decoration: none; font-weight: bold; }
        p { margin-bottom: 15px; }
    </style>
    
    <p>{% blocktrans with name=user.first_name %}Dear {{ name }},{% endblocktrans %}</p>
    
    <p>{% trans "We have received a request to recover your account. If you made this request, please click the link below to recover your account:" %}</p>
    
    <p><a href="{{ recover_account_token_url }}">{{ recover_account_token_url }}</a></p>
    
    <p>{% trans "If you did not make this request, you can safely ignore this email. Your account is safe and secure, and no unauthorized parties have gained access to your account or password." %}</p>
    
    <p>
        {% trans "Best regards," %}<br>
        <strong>{% trans "The Shareish team." %}</strong>
    </p>
{% endblock %}