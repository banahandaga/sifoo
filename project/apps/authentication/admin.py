from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.admin import GroupAdmin as AuthGroupAdmin

from apps.authentication.models import Profile, GroupDetails


class UserProfileInline(admin.StackedInline):
    model           = Profile
    can_delete      = False


class GroupDetailsInline(admin.StackedInline):
    model           = GroupDetails
    can_delete      = False


class AccountsUserAdmin(AuthUserAdmin):
    list_display    = AuthUserAdmin.list_display + ('group_name',)
    ordering        = ('id',)
    

    def add_view(self, *arg, **kwargs):
        self.inlines = [UserProfileInline]
        return super(AccountsUserAdmin, self).add_view(*arg, **kwargs)


    def change_view(self, *arg, **kwargs):
        self.inlines = [UserProfileInline]
        return super(AccountsUserAdmin, self).change_view(*arg, **kwargs)


    def group_name(self, obj):
        queryset = obj.groups.values_list('name',flat=True)
        groups = []
        for group in queryset:
            groups.append(group)
        
        return ', '.join(groups)


class GroupDetailsAdmin(AuthGroupAdmin):
    list_display = AuthGroupAdmin.list_display + ('alias','description',)
    ordering = ('id',)

    def add_view(self, *arg, **kwargs):
        self.inlines = [GroupDetailsInline]
        return super(GroupDetailsAdmin, self).add_view(*arg, **kwargs)


    def change_view(self, *arg, **kwargs):
        self.inlines = [GroupDetailsInline]
        return super(GroupDetailsAdmin, self).change_view(*arg, **kwargs)


    def alias(self, obj):
        return obj.groupdetails.alias


    def description(self, obj):
        return obj.groupdetails.description
    

admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupDetailsAdmin)