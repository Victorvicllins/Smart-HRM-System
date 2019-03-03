# Files validator
def validate_extension(file):
	import os
	from django.core.exceptions import ValidationError
	ext = os.path.splitext(file.name)[1]
	valid_extensions = ['.pdf', '.doc', '.xlsx', '.xls', '.odt']
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'This file is not Allow.')
