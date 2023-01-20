from django.contrib import admin
from .models.administrator import Administrator
from .models.moderator import Moderator
from .models.attendants import Attendants
from .models.customers import Customers
from .models.managers import Managers
from .models.vendors import Vendors


admin.site.register(Administrator)
admin.site.register(Moderator)
admin.site.register(Managers)
admin.site.register(Customers)
admin.site.register(Attendants)
admin.site.register(Vendors)
