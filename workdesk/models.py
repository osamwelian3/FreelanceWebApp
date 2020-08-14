import os

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.urls import reverse

from accounts.models import User


# Create your models here.
from writershub import settings

STATUS = (
    ('open', 'OPEN'),
    ('assigned', 'ASSIGNED'),
    ('dispute', 'DISPUTE'),
    ('editing', 'EDITING'),
    ('rejected', 'REJECTED'),
    ('revision', 'REVISION'),
    ('in_progress', 'IN_PROGRESS'),
    ('complete', 'COMPLETE'),
    ('approved', 'APPROVED'),
)


class WorkProject(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Project Title", null=False, blank=False)
    subject_area = models.CharField(max_length=255)
    course_level = models.CharField(max_length=255)
    paper_format = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(verbose_name='Deadline')
    pages = models.CharField(max_length=4, verbose_name='Number of pages', blank=True, null=True)
    spacing = models.CharField(max_length=255, verbose_name='Spacing e.g. Double Spacing', blank=True, null=True)
    cost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    sources = models.IntegerField(verbose_name='Number of allowed source references', blank=True, null=True)
    paper_details = models.TextField(verbose_name='Detailed instruction to writer')
    status = models.CharField(max_length=255, choices=STATUS, default='OPEN')

    def __str__(self):
        return "Project #" + str(self.id)

    def get_absolute_url(self):
        return reverse('order', args=[str(self.id)])


def file_rename(instance, filename):
    ext = filename.split('.')[-1]
    pid = WorkProject.objects.all().count() + 1
    try:
        id = WorkProject.objects.latest().id + 1
    except Exception:
        id = 1
    if ProjectFile.objects.filter(file_title=instance.file_title):
        p = ProjectFile.objects.get(file_title=instance.file_title)
        pimage = p.files.url
        pid = pimage.rsplit('_', 1)[1].rsplit('.', 1)[0]
        id = pimage.rsplit('_', 2)[1]
        p.delete()
    print(pid)
    filename = "%s_%s_%s.%s" % (instance.file_title, id, pid, ext)
    fullname = os.path.join(settings.MEDIA_ROOT + 'Project/Files', filename)
    print(fullname)
    if os.path.exists(fullname):
        print("Yes")
        os.remove(fullname)
    return os.path.join('Project/Files', filename)


class ProjectFile(models.Model):
    project = models.ForeignKey(WorkProject, on_delete=models.CASCADE)
    file_title = models.CharField(max_length=255)
    files = models.FileField(upload_to=file_rename, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            return self.project.title
        except ObjectDoesNotExist:
            return "No image yet"

    def delete(self, using=None, keep_parents=False):
        self.files.storage.delete(self.files.name)
        super().delete()
