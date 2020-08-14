import os
from writershub import settings


def cv_rename(instance, filename):
    from .models import WriterProfile
    file_id = ''
    file_name = 'cv'
    file = ''
    if len(file_name) > 0:
        if file_name == 'essay_1':
            file = 'essay'
            file_id = '1'
        if file_name == 'essay_2':
            file = 'essay'
            file_id = '2'
        file = '/' + file_name + ''
    ext = filename.split('.')[-1]
    pid = WriterProfile.objects.all().count() + 1
    try:
        id = WriterProfile.objects.latest('id').id + 1
    except Exception:
        id = 1
    if WriterProfile.objects.filter(id=instance.id):
        p = WriterProfile.objects.get(id=instance.id)
        pimage = p.image.url
        pid = pimage.rsplit('_', 1)[1].rsplit('.', 1)[0]
        id = instance.id
    print(instance)
    filename = "%s_%s_%s %s.%s" % (file_name, id, pid, file_id, ext)
    fullname = os.path.join(settings.MEDIA_ROOT + 'Accounts/Registration' + file + '', filename)
    print(fullname)
    if os.path.exists(fullname):
        os.remove(fullname)
    return os.path.join('Accounts/Registration' + file + '', filename)


def id_rename(instance, filename):
    from .models import WriterProfile
    file_id = ''
    file_name = 'id'
    file = ''
    if len(file_name) > 0:
        if file_name == 'essay_1':
            file = 'essay'
            file_id = '1'
        if file_name == 'essay_2':
            file = 'essay'
            file_id = '2'
        file = '/' + file_name + ''
    ext = filename.split('.')[-1]
    pid = WriterProfile.objects.all().count() + 1
    try:
        id = WriterProfile.objects.latest('id').id + 1
    except Exception:
        id = 1
    if WriterProfile.objects.filter(id=instance.id):
        p = WriterProfile.objects.get(id=instance.id)
        pimage = p.image.url
        pid = pimage.rsplit('_', 1)[1].rsplit('.', 1)[0]
        id = instance.id
    print(instance)
    filename = "%s_%s_%s %s.%s" % (file_name, id, pid, file_id, ext)
    fullname = os.path.join(settings.MEDIA_ROOT + 'Accounts/Registration' + file + '', filename)
    print(fullname)
    if os.path.exists(fullname):
        os.remove(fullname)
    return os.path.join('Accounts/Registration' + file + '', filename)


def cert_rename(instance, filename):
    from .models import WriterProfile
    file_id = ''
    file_name = 'cert'
    file = ''
    if len(file_name) > 0:
        if file_name == 'essay_1':
            file = 'essay'
            file_id = '1'
        if file_name == 'essay_2':
            file = 'essay'
            file_id = '2'
        file = '/' + file_name + ''
    ext = filename.split('.')[-1]
    pid = WriterProfile.objects.all().count() + 1
    try:
        id = WriterProfile.objects.latest('id').id + 1
    except Exception:
        id = 1
    if WriterProfile.objects.filter(id=instance.id):
        p = WriterProfile.objects.get(id=instance.id)
        pimage = p.image.url
        pid = pimage.rsplit('_', 1)[1].rsplit('.', 1)[0]
        id = instance.id
    print(instance)
    filename = "%s_%s_%s %s.%s" % (file_name, id, pid, file_id, ext)
    fullname = os.path.join(settings.MEDIA_ROOT + 'Accounts/Registration' + file + '', filename)
    print(fullname)
    if os.path.exists(fullname):
        os.remove(fullname)
    return os.path.join('Accounts/Registration' + file + '', filename)


def essay1_rename(instance, filename):
    from .models import WriterProfile
    file_id = ''
    file_name = 'essay_1'
    file = ''
    if len(file_name) > 0:
        if file_name == 'essay_1':
            file_name = 'essay'
            file_id = '1'
        if file_name == 'essay_2':
            file_name = 'essay'
            file_id = '2'
        file = '/' + file_name + ''
    ext = filename.split('.')[-1]
    pid = WriterProfile.objects.all().count() + 1
    try:
        id = WriterProfile.objects.latest('id').id + 1
    except Exception:
        id = 1
    if WriterProfile.objects.filter(id=instance.id):
        p = WriterProfile.objects.get(id=instance.id)
        pimage = p.image.url
        pid = pimage.rsplit('_', 1)[1].rsplit('.', 1)[0]
        id = instance.id
    print(instance)
    filename = "%s_%s_%s %s.%s" % (file_name, id, pid, file_id, ext)
    fullname = os.path.join(settings.MEDIA_ROOT + 'Accounts/Registration' + file + '', filename)
    print(fullname)
    if os.path.exists(fullname):
        os.remove(fullname)
    return os.path.join('Accounts/Registration' + file + '', filename)


def essay2_rename(instance, filename):
    from .models import WriterProfile
    file_id = ''
    file_name = 'essay_2'
    file = ''
    if len(file_name) > 0:
        if file_name == 'essay_1':
            file_name = 'essay'
            file_id = '1'
        if file_name == 'essay_2':
            file_name = 'essay'
            file_id = '2'
        file = '/' + file_name + ''
    ext = filename.split('.')[-1]
    pid = WriterProfile.objects.all().count() + 1
    try:
        id = WriterProfile.objects.latest('id').id + 1
    except Exception:
        id = 1
    if WriterProfile.objects.filter(id=instance.id):
        p = WriterProfile.objects.get(id=instance.id)
        pimage = p.image.url
        pid = pimage.rsplit('_', 1)[1].rsplit('.', 1)[0]
        id = instance.id
    print(instance)
    filename = "%s_%s_%s %s.%s" % (file_name, id, pid, file_id, ext)
    fullname = os.path.join(settings.MEDIA_ROOT + 'Accounts/Registration' + file + '', filename)
    print(fullname)
    if os.path.exists(fullname):
        os.remove(fullname)
    return os.path.join('Accounts/Registration' + file + '', filename)