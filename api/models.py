from django.db import models
from django.template.defaultfilters import slugify

class Sport(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    image = models.ImageField(upload_to='sport_images')
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    venue = models.CharField(max_length=200)
    price = models.IntegerField()
    datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sport, self).save()

    def __str__(self):
        return self.name