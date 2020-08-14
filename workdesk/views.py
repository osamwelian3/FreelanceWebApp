from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import WorkProject, ProjectFile


# Create your views here.
@login_required
def dashboard(request, template_name="workdesk/dashboard.html"):
    projects = WorkProject.objects.all()
    page_title = 'Dashboard'
    return render(request, template_name, locals())


@login_required
def approved(request, template_name="workdesk/approved.html"):
    page_title = 'Approved'
    return render(request, template_name, locals())


@login_required
def assigned(request, template_name="workdesk/assigned.html"):
    page_title = 'Assigned/Confirm'
    return render(request, template_name, locals())


@login_required
def bids(request, template_name="workdesk/bids.html"):
    page_title = 'Bids/Applications'
    return render(request, template_name, locals())


@login_required
def completed(request, template_name="workdesk/completed.html"):
    page_title = 'Completed'
    return render(request, template_name, locals())


@login_required
def current(request, template_name="workdesk/current.html"):
    page_title = 'Current'
    return render(request, template_name, locals())


@login_required
def dispute(request, template_name="workdesk/dispute.html"):
    page_title = 'Dispute'
    return render(request, template_name, locals())


@login_required
def editing(request, template_name="workdesk/editing.html"):
    page_title = 'Editing'
    return render(request, template_name, locals())


@login_required
def financial_overview(request, template_name="workdesk/financial_overview.html"):
    page_title = 'Financial Overview'
    return render(request, template_name, locals())


@login_required
def paid(request, template_name="workdesk/paid.html"):
    page_title = 'Paid'
    return render(request, template_name, locals())


@login_required
def rejected(request, template_name="workdesk/rejected.html"):
    page_title = 'Rejected'
    return render(request, template_name, locals())


@login_required
def revision(request, template_name="workdesk/revision.html"):
    page_title = 'Revision'
    return render(request, template_name, locals())


@login_required
def orders(request, order_id, template_name="workdesk/order.html"):
    page_title = 'Order'
    order = WorkProject.objects.get(id=order_id)
    files = ProjectFile.objects.filter(project=order)
    return render(request, template_name, locals())








