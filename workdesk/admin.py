from django.contrib import admin
from .models import WorkProject, ProjectFile
from .forms import AddProject, UpdateProject


class ProjectFilesInline(admin.StackedInline):
    model = ProjectFile
    extra = 0


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = UpdateProject
    add_form = AddProject()

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('owner', 'status',)
        return super(ProjectAdmin, self).add_view(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ('owner',)
        return super(ProjectAdmin, self).change_view(request, object_id)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(ProjectAdmin, self).get_fieldsets(request, obj)

    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        if request.user.is_admin:
            return qs
        return qs.filter(owner=request.user)

    # overide save model
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
    # The fields to be used in displaying the user model
    # These overrides the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = ('title', 'subject_area', 'owner', )
    list_filter = ('owner', )
    fieldsets = (
        ('Project info', {'fields': ('title', 'subject_area', 'course_level', 'paper_format', )}),
        ('More Info', {'fields': ('deadline', 'pages', 'spacing', 'sources', )}),
        ('Details', {'fields': ('cost', 'paper_details', 'status', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Project info', {'fields': ('title', 'subject_area', 'course_level', 'paper_format',)}),
        ('More Info', {'fields': ('deadline', 'pages', 'spacing', 'sources',)}),
        ('Details', {'fields': ('cost', 'paper_details',)}),
    )
    search_fields = ('title', 'paper_details', 'subject_area', 'course_level', 'paper_format',)
    inlines = [ProjectFilesInline, ]
    ordering = ('id', 'date_posted', 'date_updated', )
    filter_horizontal = ()


admin.site.register(WorkProject, ProjectAdmin)
