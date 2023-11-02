from django.contrib import admin
from  .models import Destination
from .models import Detailed_desc
from .models import pessanger_detail
from .models import Cards
from .models import NetBanking
from .models import Transactions

# Register your models here.

admin.site.register(Destination)
admin.site.register(Detailed_desc)
admin.site.register(pessanger_detail)
admin.site.register(Cards)
admin.site.register(NetBanking)
admin.site.register(Transactions)



