import datetime
import random
import uuid
from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from simple_history.models import HistoricalRecords
from company.descriptions import CITY_LIST, STATE_LIST
def autoKey():
	sample = uuid.uuid4()
	key = hex(int(sample.time_low))[1:]
	return key

def upload_file_path(instance, filename):
	new_filename = random.randint(1,3910209312)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "files/{new_filename}/{final_filename}".format(
			new_filename=new_filename, 
			final_filename=final_filename,
			)	

class CompanyProfile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    company_url     = models.UUIDField(default=uuid.uuid4(), editable=False)
    full_name       = models.CharField(max_length=255, help_text="Company's Name..")
    shortname       = models.CharField(max_length=120, null=True, blank=True, help_text="Company's Short-name..")
    address         = models.CharField(max_length=255, blank=True)
    vision          = models.CharField(max_length=255, help_text="Company's Vision..")
    file            = models.FileField(upload_to=upload_file_path, null=True, blank=True)
    mission         = models.CharField(max_length=255, default="Company's Mission.")
    country         = models.CharField(max_length=200, default='Federal Republic Of Nigeria.')
    state           = models.CharField(max_length=120, choices=STATE_LIST) # choices=ADDRESS_TYPES)
    city            = models.CharField(max_length=120, choices=CITY_LIST)
    employees       = models.PositiveIntegerField(default=1)
    cac_code        = models.CharField(max_length=120)
    timestamp       = models.DateTimeField(auto_now_add=True)
    history         = HistoricalRecords()

    def __str__(self):
        return '%s/%s' %(self.full_name, self.shortname)

    def get_absolute_url(self):
        return reverse("address-update", kwargs={"pk": self.pk})

    def get_company_email(self):
        return self.company_email

    def get_short_address(self):
        for_name = self.full_name 
        if self.shortname:
            for_name = "{} | {},".format( self.shortname, for_name)
        return "{for_name} {line1}, {city}".format(
                for_name = for_name or "",
                line1 = self.address,
                city = self.city
            ) 

    def get_address(self):
        return "{for_name}\n{line1}\n{city}\n{state}, {cac_code}\n{country}".format(
                for_name = self.full_name or "",
                line1 = self.address,
                city = self.city,
                state = self.state,
                cac_code= self.cac_code,
                country = self.country
            )
