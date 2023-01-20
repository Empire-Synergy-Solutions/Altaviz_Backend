from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models.customers import Customers
from django.utils.translation import gettext_lazy as _
from django.db import transaction
#from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from allauth.account.utils import user_username, user_email, user_field
#from multiupload.fields import MultiFileField

class CustomUserCreationForm(UserCreationForm):
    #email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    #url_facebook = forms.CharField(max_length=50, required=False, label=_(u'Facebook'))
    #url_twitter = forms.CharField(max_length=50, required=False, label=_(u'Twitter'))
    #url_instagram = forms.CharField(max_length=50, required=False, label=_(u'Instagram'))
    #url_custom = forms.CharField(max_length=50, required=False, label=_(u'Website'))

    class Meta(UserCreationForm.Meta):
        model = Customers
        fields = "__all__"
        #fields = UserCreationForm.Meta.fields  
        #('email', 'first_name', 'last_name','date_of_birth', 'phone_number', 
        #'location', 'address', 'current_workplace', 'age', 'url_facebook', 
        #'url_twitter','url_instagram', 'url_custom', 'is_oisalumni', 
        #'is_oisStaff', 'is_oisguardian', )


#class CustomUserCreationForm(SignupForm):
    #def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        #user = super(CustomUserCreationForm, self).save(request)
        # Add your own processing here.
        # You must return the original result.
        #user.is_oisAlumni = False
        #user.is_oisStaff = False
        #return user

#class SignupForm(forms.Form):
    #first_name = forms.CharField(max_length=30)
    #last_name = forms.CharField(max_length=30)
    #age = forms.IntegerField(max_value=100)

    #class Meta:
        #model = get_user_model() # use this function for swapping user model

    #def save(self, user):
        #user.first_name = self.cleaned_data['first_name']
        #user.last_name = self.cleaned_data['last_name']
        #user.age = self.cleaned_data['age']
        #user.save()



#class CustomUserCreationForm(SignupForm):

    #def signup(self, request, user):
        #user = super().save(commit=False)
        #user.is_oisalumni = True
        #user.first_name = self.cleaned_data['first_name']
        #user.last_name = self.cleaned_data['last_name']
        #user.save()
        #return user
    #def save(self, request):
        #user = super(CustomUserCreationForm, self).save(request)
        #return user
class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Do not persist the user yet so we pass commit=False
        # (last argument)
        user = super(CustomUserAccountAdapter, self).save_user(request, user, form, commit=False)
        #data = form.cleaned_data
        #user.age = form.cleaned_data.get('age')
        #user.date_of_birth = form.cleaned_data.get('date_of_birth')
        instance = models.customers.Customers
        #user = self.request.user
        #if user.user_type == 1:
        #if user.user_type == 'OIS Staff':
            #oisStaff = True 
        #if user.user_type == 'OIS Alumni':
            #oisAlumni = True 
        #if user.user_type == 'OIS Guardian':
            #oisGuardian = True
        
        #oisStaff = instance.is_oisStaff
        #oisAlumni = instance.is_oisalumni
        #oisGuardian = instance.is_oisguardian
        #if oisStaff :
        #    user_field(user, 'is_oisStaff', oisStaff)
        #if oisAlumni :
        #    user_field(user, 'is_oisalumni', oisAlumni)
        #if oisGuardian:
        #    user_field(user, 'is_oisguardian', oisGuardian)
        user.save()
        return user

#class SignupForm(forms.ModelForms):
    #first_name = forms.CharField(max_length=30, label='First Name')
    #last_name = forms.CharField(max_length=30, label='Last Name')

    #class Meta(UserCreationForm.Meta):
        #model = CustomUser
    #def save(self, request):
        #user = super().save(commit=False)
        #user.is_oisStaff = True
        #user.first_name = self.cleaned_data['first_name']
        #user.last_name = self.cleaned_data['last_name']
        #user.save()
        #user = super(CustomUserCreationForm, self).save(request)
        #return user
class CustomerWaitListForm(CustomUserCreationForm):
    #first_name = forms.CharField(max_length=30, label='First Name')
    #last_name = forms.CharField(max_length=30, label='Last Name')
    class Meta(UserCreationForm.Meta):
        model = Customers
        #fields = UserCreationForm.Meta.fields
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        #user.is_oisStaff = True
        #OisStaffProfile.objects.create(user=user)
        if commit:
            user.save()
        return user
