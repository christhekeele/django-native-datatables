# EXAMPLE MODEL

# from django.db import models
# from django.contrib.localflavor.us.models import PhoneNumberField
# 
# from django.db.models import Manager
# from company.tables import CompanyDatatable
# 
# from datetime import datetime
# 
# class Company(models.Model):
#     # datatable is secretly a manager, so we have to set the default first.
#     objects = Manager()
#     datatable = CompanyDatatable()
#     
#     name = models.CharField(max_length=150)
#     parent = models.ForeignKey('self', related_name="children", null=True, blank=True);
#     
#     website = models.URLField(null=True, blank=True)
#     email = models.EmailField()
#     phone = PhoneNumberField()
#     extension = models.PositiveIntegerField(null=True, blank=True)
#     fax = PhoneNumberField(null=True, blank=True)
#     
#     active = models.BooleanField()
#     priority = models.CharField(max_length=2, choices=(('H', 'High'),('M', 'Medium'),('L', 'Low'),), default='L')
#     
#     acquired_on = models.DateField(default=datetime.now().date())
#     
#     def __unicode__(self):
#         return u"%s" % (self.name)
#         
#     class Meta:
#         ordering = ['name']