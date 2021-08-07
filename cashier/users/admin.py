from django.contrib import admin

# Register your models here.
from cashier.households.models import HouseholdProfile
from cashier.payments.models import PaymentsAdmin, IndividualPayment
from cashier.profiles.models import UserProfile
from cashier.users.models import cashierUser

class CashierUserAdmin(admin.ModelAdmin):
    exclude = ('password','username')

class UserProfileAdmin(admin.ModelAdmin):
    exclude = ('user',)

admin.site.register(cashierUser, CashierUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(HouseholdProfile)
admin.site.register(PaymentsAdmin)
admin.site.register(IndividualPayment)