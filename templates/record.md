Title: {{ title }}
Breadcrumb: catalogue-entry

<table class="library">
	{% if type %}
	<tr>
		<th>Type</th>
		<td>{{ type }}</td>
	</tr>
	{% endif %}

	{% if author %}
	<tr>
		<th>By</th>
		<td>{{ author }}</td>
	</tr>
	{% endif %}

	{% if uniform_title %}
	<tr>
		<th>Uniform Title</th>
		<td>{{ uniform_title }}</td>
	</tr>
	{% endif %}

	{% if contributors %}
	<tr>
		<th>Contributors</th>
		<td>{{ contributors|join(' | ') }}</td>
	</tr>
	{% endif %}
	
	<tr>
		<th>Languages</th>
		<td>{{ languages|join(' | ') }}</td>
	</tr>
	{% if original_languages %}
	<tr>
		<th>Original Languages</th>
		<td>{{ original_languages|join(' | ') }}</td>
	</tr>
	{% endif %}
	
	{% if edition %}
	<tr>
		<th>Edition</th>
		<td>{{ edition }}</td>
	</tr>
	{% endif %}

	{% if publication %}
	<tr>
		<th>Publisher</th>
		<td>{{ publication }}</td>
	</tr>
	{% endif %}
	{% if copyright %}
	<tr>
		<th>Copyright</th>
		<td>{{ copyright }}</td>
	</tr>
	{% endif %}
	
	{% if physical_description %}
	<tr>
		<th>Physical Description</th>
		<td>{{ physical_description }}</td>
	</tr>
	{% endif %}
	
	{% if isbns %}
	<tr>
		<th>ISBN</th>
		<td>{{ isbns|join(' | ') }}</td>
	</tr>
	{% endif %}
	
	{% if subjects %}
	<tr>
		<th>Subjects</th>
		<td>{{ subjects|join(' | ') }}</td>
	</tr>
	{% endif %}


	{% if notes %}
	<tr>
		<th>Notes</th>
		<td>{% for note in notes %}<p>{{ note }}</p>{% endfor %}</td>
	</tr>
	{% endif %}

	{% if analytics %}
	<tr>
		<th>Analytics</th>
		<td><ul>{% for analytic in analytics %}<li>{{ analytic }}</li>{% endfor %}</ul></td>
	</tr>
	{% endif %}

	{% if holdings %}
	<tr>
		<th>Holdings</th>
		<td><ul>{% for holding in holdings %}<li>{{ holding }}</li>{% endfor %}</ul></td>
	</tr>
	{% endif %}
</table>
