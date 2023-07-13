
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import UserProfile

# Register your models here.

# Register your models here.
class UserProfileAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = UserProfile
    list_display = ( "email", "first_name", "last_name","username",
    "phone_number", "country", "date_joined", "is_active")
    list_editable = ["is_active"]
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name',
         'last_name',"phone_number", "country", "date_joined")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password',  'first_name', 'last_name', 'is_staff',
             'is_active',"phone_number", "country", "date_joined",)}
        ),
    )
    search_fields = ('email',)
    ordering = ('date_joined',)

admin.site.register(UserProfile,UserProfileAdmin)