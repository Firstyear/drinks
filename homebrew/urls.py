from django.conf.urls import patterns, url
#from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

#import .views as views
from homebrew import views

urlpatterns = patterns('',
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    #url(r'^batch/$', views.IndexView.as_view(), name='batch_list'),
    url(r'^batch/create/$', login_required(views.BatchCreateView.as_view()), name='batch_create'),
    url(r'^batch/$', login_required(views.BatchListView.as_view()), name='batch_list'),
    url(r'^batch/(?P<pk>\d+)/$', login_required(views.BatchDetailView.as_view()), name='batch_detail'),
    url(r'^batch/(?P<pk>\d+)/update/$', login_required(views.BatchUpdateView.as_view()), name='batch_update'),
    url(r'^batch/(?P<pk>\d+)/label\.pdf$', login_required(views.batch_label), name='batch_label'),
    url(r'^ingredient/$', login_required(views.IngredientView.as_view()), name='ingredient_view'),
    url(r'^sourceingredient/create/$', login_required(views.SourceIngredientCreateView.as_view()), name='sourceingredient_create'),
    url(r'^sourceingredient/(?P<pk>\d+)/$', login_required(views.SourceIngredientDetailView.as_view()), name='sourceingredient_detail'),
    url(r'^sourceingredient/(?P<pk>\d+)/update/$', login_required(views.SourceIngredientUpdateView.as_view()), name='sourceingredient_update'),
    url(r'^box/create/$', login_required(views.BoxCreateView.as_view()), name='box_create'),
    url(r'^box/(?P<pk>\d+)/$', login_required(views.BoxDetailView.as_view()), name='box_detail'),
    url(r'^box/(?P<pk>\d+)/update/$', login_required(views.BoxUpdateView.as_view()), name='box_update'),
    url(r'^box/(?P<pk>\d+)/delete/$', login_required(views.BoxDeleteView.as_view()), name='box_delete'),
    url(r'label/$', login_required(views.LabelListView.as_view()), name='label_list'),
    url(r'label/create/$', login_required(views.LabelCreateView.as_view()), name='label_create'),
    url(r'label/(?P<pk>\d+)/$', login_required(views.LabelDetailView.as_view()), name='label_detail'),
    url(r'label/(?P<pk>\d+)/update/$', login_required(views.LabelUpdateView.as_view()), name='label_update'),
    url(r'label/(?P<pk>\d+)/delete/$', login_required(views.LabelUpdateView.as_view()), name='label_delete'),
    url(r'sugar/create/$', login_required(views.SugarCreateView.as_view()), name='sugar_create'),
    url(r'sugar/(?P<pk>\d+)/update/$', login_required(views.SugarUpdateView.as_view()), name='sugar_update'),
    url(r'yeast/create/$', login_required(views.YeastCreateView.as_view()), name='yeast_create'),
    url(r'yeast/(?P<pk>\d+)/update/$', login_required(views.YeastUpdateView.as_view()), name='yeast_update'),
    ##### These don't need auth ....
    ### Fix this view!!!!! With the success_url
    url(r'^comment/$', views.CommentCreateView.as_view(), name='comment_create_anon'),
    url(r'^comment/(?P<pk>\d+)/$', views.CommentCreateView.as_view(), name='comment_create_long'),
    url(r'^c/(?P<pk>\d+)/$', views.CommentCreateView.as_view(), name='comment_create'),
    url(r'^comment/thanks/$', views.CommentThanksView.as_view(), name='comment_thanks'),
)
