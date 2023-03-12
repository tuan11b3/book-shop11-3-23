from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import myUser
from store.models import Staff


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = myUser
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', "user_permissions", "groups")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', "user_permissions", "groups")}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(myUser, CustomUserAdmin)

class CustomStaff(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'phone', 'cmnd', 'address', 'salary', 'date_joined')
    list_filter = ('date_joined', 'salary',)
    search_fields = ('fullname',)

    class Meta:
        model = Staff


admin.site.register(Staff, CustomStaff)

