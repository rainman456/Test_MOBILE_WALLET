from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

class UserCreationForm(UserCreationForm):

# If you want to give superuser privileges to the staff users, override the save method 
    def save(self, commit=True):
        user = self.instance
        if user.is_staff:   
            user.is_superuser = True
        return super().save(commit=True)

    class Meta:
        model = UserProfile
        fields = ('last_name', 'email', 'first_name', 'password', 'country', 'phone_number')

class UserChangeForm(UserChangeForm):
   class Meta:
        model = UserProfile
        fields = ('last_name', 'email', 'first_name', 'password', 'country', 'phone_number')