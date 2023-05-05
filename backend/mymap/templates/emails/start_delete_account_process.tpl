{% extends "mail_templated/base.tpl" %}
{% load my_filters %}

{% block subject %}
    [Shareish] Start the deletion process of your account
{% endblock %}

{% block text %}
	Dear {{ user.first_name }},{{ text|linebreaks }}
    {{ text|linebreaks }}
	We have received your request to delete your account. If you made this request, please click the link below to confirm your account deletion:{{ text|linebreaks }}
    {{ text|linebreaks }}
	<a href="{{ delete_account_token_url }}">{{ delete_account_token_url }}</a>{{ text|linebreaks }}
    {{ text|linebreaks }}
	If you did not make this request, please consider improve your account security by changing your password. As of now, your account will not be deleted.{{ text|linebreaks }}
    {{ text|linebreaks }}
	Best regards,{{ text|linebreaks }}
    The Shareish Team.
{% endblock %}

{% block html %}
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 16px;
        }
        a {
            color: #3eaf7c;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        p {
            margin-bottom: 10px;
        }
    </style>
	<p>Dear {{ user.first_name }},</p>
	<p>We have received your request to delete your account. If you made this request, please click the link below to start the deletion process of your account:</p>
	<p><a href="{{ delete_account_token_url }}">{{ delete_account_token_url }}</a></p>
	<p>If you did not make this request, please consider improve your account security by changing your password. As of now, your account will not be deleted.</p>
	<p>Best regards,<br>The Shareish Team.</p>
{% endblock %}