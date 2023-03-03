from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()



class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class RegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=4,max_length=50)
    email = forms.EmailField(max_length=100,help_text='Required' ,error_messages={'required':'you needto input an email'})
    first_name=forms.CharField(max_length=200)
    last_name=forms.CharField(max_length=200)
    #delvery details
    phone=forms.CharField(max_length=150,help_text='Required',)
    
    
    password =forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label ='confirm password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'
        

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username =username)
        if r.count():
            raise forms.ValidationError('User already exits')
        return username 
    def clean_password2(self):
        cd =self.cleaned_data
        if cd['password'] != cd['password2']:
        
            raise forms.ValidationError('Password doesnot match')
        return cd['password2'] 


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email =email).exists():
       
            raise forms.ValidationError('please use another email this one is already taken')
        return email           
    
