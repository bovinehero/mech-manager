from . import views
from django.urls import path

# this is needed for class based views as an include in the core app

# in the index.html there is a control statement {% url 'post_detail' post.slug %}
# NOTE that the post_detail matches the name= value for the slug path converter <slug:slug> <pathconverter:keyword> below

urlpatterns = [
    path('', views.CardList.as_view(), name='home'), #TODO change this to landing page
    path('mechs/', views.MechList.as_view(), name='mechs'),
    path('mechs/create/', views.CreateMechView.as_view(), name="mech_create"),
    path('mechs/<slug:slug>/update/', views.UpdateMechView.as_view(), name="mech_update"),
    path('mechs/<slug:slug>/toggle/', views.toggle_mech_status, name="mech_toggle"),
    path('mechs/<slug:slug>/delete/', views.DeleteMechView.as_view(), name="mech_delete"),
    path('mechs/<slug:slug>', views.MechDetail.as_view(), name='mech_detail')
]