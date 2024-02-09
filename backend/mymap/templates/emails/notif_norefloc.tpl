{% extends "mail_templated/base.tpl" %}
{% load my_filters %}

{% block subject %}
    [Shareish] Invitation to configure your profile & notifications
{% endblock %}

{% block body %}
    (en français ci-dessous)
    
    Dear {{ user.first_name }} {{ user.last_name }} (@{{ user.username }}),

    We would like to kindly invite you to configure your profile on Shareish, especially your notification settings on {{ app_url }}/settings/notifications.
    
    This message is sent by an automated procedure which has detected you currently do not have a reference address set in your profile.
    
    Reference address is a unique Shareish feature which allows you to set an address which is used by the platform to detect if new items/events are created in your neighboorhood based on a configurable notification distance radius. We believe this is a very useful feature that allows you to focus on data relevant to you !
    For example, let's say you mention your street name and a distance of 20km, the system will notify you when new items/events are published within 20 km around the reference address e.g. a free event (Repair Café, ...) or a gift (a field where it is possible to glean vegetables, ...), a request for help from a citizen in your area, ... Similarly, you can activate notifications for public resources in your area (such as public bookcases, food banks, ...). You can choose, instant, daily, weekly, monthly, or no notification at all. 

    In order to respect your privacy (see our privacy policy {{ app_url }}/#terms_conditions), you are free to set a precise or unprecise address, e.g. streetnumber and streetname in your city, only a street or area name, or only your city name. Please also note your address will not be shared with other users, our internal system will only use it to sort data and for notifications.
    Furthermore, all notifications can be configured or opt-out in the settings page.
    Shareish offers you to decide how frequently/precisely/distantly you want to be notified !
   
    Please log on {{ app_url }} and go to My Account > Settings then Notification Settings page or directly here: {{ app_url }}/settings/notifications.
    If you don't want to receive future messages about general Shareish information such as this one, you can desactivate this feature in "General info". 

    The Shareish team.

    -------------------------------------------------------------------

    Cher/Chère {{ user.first_name }} {{ user.last_name }} (@{{ user.username }}),

    Nous aimerions vous inviter à configurer votre profil Shareish, en particulier les paramètres de notifications sur {{ app_url }}/settings/notifications.

    Ce message vous est envoyé par une procédure automatique qui a détecté que vous n'aviez pas configuré votre adresse de référence dans votre profil.

    L'adresse de référence est une fonctionnalité unique de Shareish qui vous permet de définir une adresse de référence utilisée par la plateforme pour détecter si de nouveaux éléments/événements sont créés dans votre quartier en fonction d'un rayon (en km) configurable. Nous pensons qu'il s'agit d'une fonctionnalité très utile qui vous permet de vous concentrer sur les données qui vous concernent ! Par exemple, si vous mentionnez le nom de votre rue et une distance de 20 km, le système vous avertira lorsque de nouveaux articles/événements seront publiés dans un rayon de 20 km autour de votre adresse de référence, par exemple un Repair café, une donnerie, un lieu où il est possible de glâner des légumes, une demande d'aide d'un voisin, ... De manière similaire, vous pouvez activer les notifications pour les ressources publiques (boîtes à livres/dons, épicerie solidaire, ...). Vous pouvez choisir une notification instantanée, quotidienne, hebdomadaire, mensuelle, ou désactiver les notifications.

     Afin de respecter votre vie privée (voir la Politique de confidentialité de la plateforme {{ app_url }}/#terms_conditions), vous êtes bien sûr libres de définir une adresse précise ou imprécise, par ex. un numéro de rue et le nom de rue dans votre ville, ou bien uniquement un nom de rue ou de quartier, ou uniquement le nom de votre ville. 
     Veuillez aussi noter que votre adresse ne sera pas partagée avec d'autres utilisateurs, notre système interne ne l'utilisera que pour trier les données et les notifications.
     De plus, toutes les notifications peuvent être configurées ou désactivées dans la page des paramètres.
     Shareish vous propose de décider vous-même à quelle fréquence, distance, et précision vous souhaitez être averti.e.s !
   
     N'attendez plus et connectez-vous sur {{ app_url }} et allez dans Mon compte > Paramètres puis à la page Paramètres de notification ou directement ici: {{ app_url }}/settings/notifications.
     Si vous ne voulez plus recevoir des messages d'information générale de la plateforme Shareish comme celui-ci, vous pouvez également les désactiver dans la section "Informations générales".

     L'équipe Shareish.
    
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



<p>(<a href="#fr">en français ci-dessous</a>)</p>
<p> Dear {{ user.first_name }} {{ user.last_name }} (@{{ user.username }}),</p>

<p>We would like to kindly invite you to configure your profile on Shareish, especially your <b><a href='{{ app_url }}/settings/notifications'>notification settings</a></b>.</p>

<p>This message is sent by an automated procedure which has detected you currently do not have a <b>reference address</b> set in your profile.</p>
    
<p><b>Reference address</b> is a unique Shareish feature which allows you to set an address which is used by the platform to detect if new items/events are created in your neighboorhood based on a configurable distance radius.  We believe this is a very useful feature that allows you to focus on data relevant to you ! <br>
For example, let's say you mention your street name and a distance of 20km, the system will notify you when new items/events are published within 20 km around the reference address e.g. a free event (Repair Café, ...) or a gift (a field where it is possible to glean vegetables, ...), a request for help from a citizen in your area, ... Similarly, you can activate notifications for public resources in your area (such as public bookcases, food banks, ...). You can choose, instant, daily, weekly, monthly, or no notification at all. </p>

<p>In order to respect your privacy (see our <a href="{{ app_url }}/#terms_conditions">Platform privacy policy</a>), you are free to set a precise or unprecise address, e.g. streetnumber and streetname in your city, only a street or area name, or only your city name. Please also note your address will not be shared with other users, our internal system will only use it to sort data and for notifications. Furthermore, all notifications can be configured or opt-out in the settings page.<br>
Shareish offers you to decide how frequently/precisely/distantly you want to be notified !</p>


<p><p>Please log on <a href='{{ app_url }}'>{{ app_url }}</a> and go to My Account > Settings then <a href='{{ app_url }}/settings/notifications'<b>notification settings</b></a> page. <br>If you don't want to receive future messages about general Shareish information such as this one, you can desactivate this feature in "General info". 
</p>

<p>The Shareish team.</p>

<hr>

<p><a name="fr"></a>Cher/Chère {{ user.first_name }} {{ user.last_name }} (@{{ user.username }}),</p>


<p>Nous aimerions vous inviter à configurer votre profil Shareish, en particulier les <b><a href='{{ app_url }}/settings/notifications'>paramètres de notifications</a></b>.</p>

<p>Ce message vous est envoyé par une procédure automatique qui a détecté que vous n'aviez pas configuré votre <b>adresse de référence</b> dans votre profil.</p>

<p><b>L'adresse de référence</b> est une fonctionnalité unique de Shareish qui vous permet de définir une adresse de référence utilisée par la plateforme pour détecter si de nouveaux éléments/événements sont créés dans votre quartier en fonction d'un rayon (en km) configurable. Nous pensons qu'il s'agit d'une fonctionnalité très utile qui vous permet de vous concentrer sur les données qui vous concernent ! Par exemple, si vous mentionnez le nom de votre rue et une distance de 20 km, le système vous avertira lorsque de nouveaux articles/événements seront publiés dans un rayon de 50 km autour de votre adresse de référence, par exemple un Repair café, une donnerie, un lieu où il est possible de glâner des légumes, une demande d'aide d'un voisin, ... De manière similaire, vous pouvez activer les notifications pour les ressources publiques (boîtes à livres/dons, épicerie solidaire, ...). Vous pouvez choisir une notification instantanée, quotidienne, hebdomadaire, mensuelle, ou désactiver les notifications.</p>


<p>Afin de respecter votre vie privée (voir la <a href="{{ app_url }}/#terms_conditions">Politique de confidentialité de la plateforme</a>), vous êtes bien sûr libres de définir une adresse précise ou imprécise, par ex. un numéro de rue et le nom de rue dans votre ville, ou bien uniquement un nom de rue ou de quartier, ou uniquement le nom de votre ville. Veuillez aussi noter que votre adresse ne sera pas partagée avec d'autres utilisateurs, notre système interne ne l'utilisera que pour trier les données et les notifications. De plus, toutes les notifications peuvent être configurées ou désactivées dans la page des paramètres.<br>
Shareish vous propose de décider vous-même à quelle fréquence, distance et précision vous souhaitez être averti.e.s !</p>

<p>N'attendez plus et connectez-vous sur <a href='{{ app_url }}'>{{ app_url}}</a> et allez dans Mon compte > Paramètres puis à la page Paramètres de notification ou directement ici: <a href='{{ app_url }}/settings/notifications'><b>Adresse de référence et notifications E-mail</b></a>. <br>Si vous ne voulez plus recevoir des messages d'information générale de la plateforme Shareish comme celui-ci, vous pouvez également les désactiver dans la section "Informations générales".</p>

<p>L'équipe Shareish.</p>

{% endblock %}
