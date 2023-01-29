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
    priceMale = models.IntegerField(null=True, blank=True)
    priceFemale = models.IntegerField(null=True, blank=True)
    datetime = models.DateTimeField()
    minimumPlayersMale = models.IntegerField( null=True, blank=True)
    maximumPlayersMale = models.IntegerField( null=True, blank=True)
    minimumPlayersFemale = models.IntegerField( null=True, blank=True)
    maximumPlayersFemale = models.IntegerField( null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sport, self).save()

    def split_rules(self):
        print("splitting rules")
        return self.rules.split(';')
    
    def split_description(self):
        return self.description.split(';')

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    phone = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Payment(models.Model):

    tracking_id = models.CharField(max_length=20, null=True, blank=True)
    bank_ref_no = models.CharField(max_length=20, null=True, blank=True)
    order_status = models.CharField(max_length=20, null=True, blank=True)
    failure_message = models.CharField(max_length=255, null=True, blank=True)
    payment_mode = models.CharField(max_length=20, null=True, blank=True)
    card_name = models.CharField(max_length=20, null=True, blank=True)
    status_code = models.CharField(max_length=10, null=True, blank=True)
    status_message = models.CharField(max_length=20, null=True, blank=True)
    amount = models.CharField(max_length=20, null=True, blank=True)
    trans_date = models.DateTimeField(null=True, blank=True)

    # Billng details
    billing_name = models.CharField(max_length=50, null=True, blank=True)
    billing_address = models.CharField(max_length=255, null=True, blank=True)
    billing_city = models.CharField(max_length=50, null=True, blank=True)
    billing_state = models.CharField(max_length=20, null=True, blank=True)
    billing_zipcode = models.CharField(max_length=10, null=True, blank=True)
    billing_telephone = models.CharField(max_length=20, null=True, blank=True)
    billing_email = models.CharField(max_length=100, null=True, blank=True)
    

class Team(models.Model):

    name = models.CharField(max_length=200)
    need_accomodation = models.BooleanField(default=False)
    accomodation_preference = models.CharField(max_length=50, default="")
    institute_name = models.CharField(max_length=200)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    is_male_team = models.BooleanField(default=True)
    logo = models.FileField(upload_to='team_images', null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)
    sport_incharge_name = models.CharField(max_length=200)
    sport_incharge_number = models.CharField(max_length=200)
    sport_incharge_email_id = models.CharField(max_length=200)
    player_names = models.TextField(default="none")
    captain_name = models.CharField(max_length=200, default="none")
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    
    # TODO: make unique later
    order_id = models.CharField(max_length=255, null=True, blank=True)
    is_payment_successful = models.BooleanField(default=False)
    payment = models.OneToOneField(Payment, null=True, blank=True, on_delete=models.SET_NULL)

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

