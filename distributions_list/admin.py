from django.contrib import admin
from django.core.validators import get_available_image_extensions, FileExtensionValidator
from django import forms
from django.forms import ImageField as DjangoImageField
from .models import Distributions, Reviews

import sys
from io import BytesIO
from PIL import Image
import xml.etree.cElementTree as et

from django.core.exceptions import ValidationError

# Register your models here.

def validate_image_and_svg_file_extension(value):
	allowed_extensions = get_available_image_extensions() + ["svg"]
	return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)

class SVGAndImageFormField(DjangoImageField):
	default_validators = [validate_image_and_svg_file_extension]
	
	def to_python(self, data):
		test_file = super(DjangoImageField, self).to_python(data)
		if test_file is None:
			return None
		
		# We need to get a file object for Pillow. We might have a path or we might
		# have to read the data into memory.
		if hasattr(data, 'temporary_file_path'):
			ifile = data.temporary_file_path()
		else:
			if hasattr(data, 'read'):
				ifile = BytesIO(data.read())
			else:
				ifile = BytesIO(data['content'])
		
		try:
			# load() could spot a truncated JPEG, but it loads the entire
			# image in memory, which is a DoS vector. See #3848 and #18520.
			image = Image.open(ifile)
			# verify() must be called immediately after the constructor.
			image.verify()
		
			# Annotating so subclasses can reuse it for their own validation
			test_file.image = image
			test_file.content_type = Image.MIME[image.format]
		except Exception:
			# add a workaround to handle svg images
			if not self.is_svg(ifile):
				six.reraise(ValidationError, ValidationError(
					self.error_messages['invalid_image'],
					code='invalid_image',
				), sys.exc_info()[2])
		if hasattr(test_file, 'seek') and callable(test_file.seek):
			test_file.seek(0)
		return test_file
	
	def is_svg(self, f):
		f.seek(0)
		tag = None
		try:
			for event, el in et.iterparse(f, ('start',)):
				tag = el.tag
				break
		except et.ParseError:
			pass
		return tag == '{http://www.w3.org/2000/svg}svg'

class SVGImageModelForm(forms.ModelForm):
	class Meta:
		model = Distributions
		exclude = []
		field_classes = {
			'icon': SVGAndImageFormField,
		}

class SVGImageModelAdmin(admin.ModelAdmin):
	form = SVGImageModelForm

admin.site.register(Distributions, SVGImageModelAdmin)
admin.site.register(Reviews)
