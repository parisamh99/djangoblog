{% extends "mail_templated/base.tpl" %}

{% block subject %}
  user activation
{% endblock %}

{% block html %}
  {{token}}
{% endblock %}