from django.db import models

class IntegerRangeField(models.IntegerField):
	def __init__(self, verbose_name=None, name=None, min_value=0, max_value=5, **kwargs):
		self.min_value, self.max_value = min_value, max_value
		models.IntegerField.__init__(self, verbose_name, name, **kwargs)
	
	def formfield(self, **kwargs):
		defaults = {'min_value': self.min_value, 'max_value':self.max_value}
		defaults.update(kwargs)
		return super(IntegerRangeField, self).formfield(**defaults)

# Create your models here.

class Distributions(models.Model):
	name = models.CharField('Название', max_length=50)
	short_info = models.CharField('Кратко', max_length=250)
	full_info = models.TextField('Информация')
	image = models.ImageField('Изображение')
	#date = models.DateTimeField('Дата')
	popularity = IntegerRangeField('Популярность')
	society_support = IntegerRangeField('Поддерживаемость сообществом')
	stability = IntegerRangeField('Надёжность и стабильность')
	user_friendly = IntegerRangeField('Простота в использовании')
	programs_update_frequency = IntegerRangeField('Частота обновлений программ')
	customizability = IntegerRangeField('Настраиваемость')
	consumption = IntegerRangeField('Потребление')
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = 'Дистрибутив'
		verbose_name_plural = 'Дистрибутивы'

class Reviews(models.Model):
	user_id = models.IntegerField('ID пользователя')
	dist_id = models.IntegerField('ID дистрибутива')
	text = models.TextField('Отзыв')
	rate = models.IntegerField('Оценка')
	date = models.DateTimeField('Дата')
	
	def __str__(self):
		return self.user_id
	
	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы'
