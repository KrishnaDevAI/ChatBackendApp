from django.conf import settings
from django.db import models


class Profile(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='profile',
	)
	image = models.FileField(upload_to='profile_images/', blank=True, null=True)
	address = models.TextField(blank=True)

	def __str__(self):
		return f'{self.user.username} profile'
