Title: Catalogue
Breadcrumb: library

{% for key, value in listing.items() %}
- <a href="/library/records/{{ key }}">{{ value }}</a>
{% endfor %}
