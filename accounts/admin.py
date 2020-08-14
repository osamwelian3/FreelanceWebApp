from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm, WriterProfileForm
from .models import User, WriterProfile


# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = WriterProfile
    extra = 0


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_admin:
            return qs
        return qs.filter(id=request.user.id)

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_admin:
            return self.fieldsets2
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return False

    # The fields to be used in displaying the user model
    # These overrides the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = ('username', 'email', 'admin', )
    list_filter = ('admin', )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', )}),
        ('Personal info', {'fields': ()}),
        ('permissions', {'fields': ('admin', 'staff', )}),
    )
    fieldsets2 = (
        (None, {'fields': ('username', 'email', 'password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'email', 'password', 'password2')}
         ),
    )
    search_fields = ('username', 'email',)
    # inlines = [UserProfileInline, ]
    ordering = ('username', 'email', )
    filter_horizontal = ()


class WriterProfileAdmin(admin.ModelAdmin):
    form = WriterProfileForm
    add_form = WriterProfileForm

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('user', )
        return super(WriterProfileAdmin, self).add_view(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ('user',)
        return super(WriterProfileAdmin, self).change_view(request, object_id)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(WriterProfileAdmin, self).get_fieldsets(request, obj)

    def get_queryset(self, request):
        qs = super(WriterProfileAdmin, self).get_queryset(request)
        if request.user.is_admin:
            return qs
        return qs.filter(user=request.user)

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return False

    # overide save model
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    # The fields to be used in displaying the user model
    # These overrides the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = ('user', 'academic_level', 'user',)
    list_filter = ('user',)
    fieldsets = (
        ('Personal Details', {'fields': ('country', 'city', 'zip', 'phone', 'worked',)}),
        ('Citations and Disciplines', {'fields': ('styles', 'academic_disciplines',)}),
        ('CV Details', {'fields': ('native_language', 'academic_level', 'brief_cv', 'detailed_cv',)}),
        ('Certification and Govt ID/Passport', {'fields': ('government_id', 'certificate_title', 'certificate',)}),
        ('Sample Essays', {'fields': ('essay1_title', 'essay_one', 'essay2_title', 'essay_two',)}),
        ('Payment and Terms', {'fields': ('payment_method', 'terms',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Personal Details', {'fields': ('country', 'city', 'zip', 'phone', 'worked',)}),
        ('Citations and Disciplines', {'fields': ('styles', 'academic_disciplines',)}),
        ('CV Details', {'fields': ('native_language', 'academic_level', 'brief_cv', 'detailed_cv',)}),
        ('Certification and Govt ID/Passport', {'fields': ('government_id', 'certificate_title', 'certificate',)}),
        ('Sample Essays', {'fields': ('essay1_title', 'essay_one', 'essay2_title', 'essay_two',)}),
        ('Payment and Terms', {'fields': ('payment_method', 'terms',)}),
    )
    search_fields = ('title', 'paper_details', 'subject_area', 'course_level', 'paper_format',)
    ordering = ('id', )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(WriterProfile, WriterProfileAdmin)

# remove Group Model from admin. We're not going to use it
admin.site.unregister(Group)
