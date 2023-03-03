from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm,UserAdminChangeForm
class UserModelAdmin(BaseUserAdmin):
  
  form = UserAdminChangeForm
  add_form = UserAdminCreationForm
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'username','admin')
  list_filter = ('admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('first_name','last_name')}),
      ('Permissions', {'fields': ('admin','staff','active')}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email','username', 'password1', 'password2'),
      }),
  )
  search_fields = ['email','first_name','last_name']
  ordering = ['email']
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)