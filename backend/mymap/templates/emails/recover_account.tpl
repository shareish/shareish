{% extends "mail_templated/base.tpl" %}
{% load my_filters %}
{% load i18n %}  {# 1. Always load the internationalization library #}

{% block subject %}
    {# 2. Use trans for static strings #}
    {% trans "[Shareish] Recover your account" %}
{% endblock %}

{% block text %}
    {% trans "Dear" %} {{ user.first_name }},{{ text|linebreaks }}
    {{ text|linebreaks }}
    {% trans "We have received a request to recover your account. If you made this request, please click the link below to recover your account:" %}{{ text|linebreaks }}
    {{ text|linebreaks }}
    {{ recover_account_token_url }}{{ text|linebreaks }}
    {{ text|linebreaks }}
    {% trans "If you did not make this request, you can safely ignore this email. Your account is safe and secure, and no unauthorized parties have gained access to your account or password." %}{{ text|linebreaks }}
    {{ text|linebreaks }}
    {% trans "Best regards," %}{{ text|linebreaks }}
    {% trans "The Shareish team." %}
{% endblock %}

{% block html %}
    <style>
        body { font-family: Arial, sans-serif; font-size: 16px; }
        a { color: #3eaf7c; text-decoration: none; }
        a:hover { text-decoration: underline; }
        p { margin-bottom: 10px; }
    </style>
    
    <p>{% trans "Dear" %} {{ user.first_name }},</p>
    
    <p>{% trans "We have received a request to recover your account. If you made this request, please click the link below to recover your account:" %}</p>
    
    <p><a href="{{ recover_account_token_url }}">{{ recover_account_token_url }}</a></p>
    
    <p>{% trans "If you did not make this request, you can safely ignore this email. Your account is safe and secure, and no unauthorized parties have gained access to your account or password." %}</p>
    
    <p>
        {% trans "Best regards," %}<br>
        {% trans "The Shareish team." %}
    </p>
{% endblock %}