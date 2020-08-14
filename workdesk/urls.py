from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path, re_path
from . import views

urlpatterns = [
    re_path(r'^dashboard/$', views.dashboard, name='dashboard'),
    re_path(r'^approved/$', views.approved, name='approved'),
    re_path(r'^assigned/$', views.assigned, name='assigned'),
    re_path(r'^bids/$', views.bids, name='bids'),
    re_path(r'^completed/$', views.completed, name='completed'),
    re_path(r'^current/$', views.current, name='current'),
    re_path(r'^dispute/$', views.dispute, name='dispute'),
    re_path(r'^editing/$', views.editing, name='editing'),
    re_path(r'^financial_overview/$', views.financial_overview, name='financial'),
    re_path(r'^paid/$', views.paid, name='paid'),
    re_path(r'^rejected/$', views.rejected, name='rejected'),
    re_path(r'^revision/$', views.revision, name='revision'),
    re_path(r'^order/(?P<order_id>[-\w]+)/$', views.orders, name='order'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
