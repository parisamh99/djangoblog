{% extends "mail_templated/base.tpl" %}

{% block subject %}
  user activation
{% endblock %}

{% block html %}
  http://0.0.0.0:8000/accounts/api/v1/activation/confirm/{{token}}
{% endblock %}