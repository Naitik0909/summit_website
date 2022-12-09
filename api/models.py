from django.db import models
from django.template.defaultfilters import slugify



class Sport(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    image = models.ImageField(upload_to='sport_images')
    logo = models.FileField(upload_to='sport_images', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    venue = models.CharField(max_length=200)
    price = models.IntegerField()
    datetime = models.DateTimeField()
    minimumPlayers = models.IntegerField( null=True)
    maximumPlayers = models.IntegerField( null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sport, self).save()

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    phone = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Team(models.Model):

    name = models.CharField(max_length=200)
    need_accomodation = models.BooleanField(default=False)
    institute_name = models.CharField(max_length=200)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    logo = models.FileField(upload_to='team_images', null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)
    sport_incharge_name = models.CharField(max_length=200)
    sport_incharge_number = models.CharField(max_length=200)
    sport_incharge_email_id = models.CharField(max_length=200)
    player_names = models.TextField(default="none")
    captain_name = models.CharField(max_length=200, default="none")

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(primary_key=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    team = models.ManyToManyField(Team, related_name='players', null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name