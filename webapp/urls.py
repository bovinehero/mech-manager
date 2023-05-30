""" webapp URL Configuration """
# django imports occur at runtime, so fail linter
# pylint:disable=import-error
from django.urls import path
# pylint:enable=import-error

from . import views

urlpatterns = [
    path('', views.CardList.as_view(), name='home'),
    path('mechs/', views.MechList.as_view(), name='mechs'),
    path('mechs/create/', views.CreateMechView.as_view(), name="mech_create"),
    path(
        'mechs/<slug:slug>/update/',
        views.UpdateMechView.as_view(),
        name="mech_update"
    ),
    path(
        'mechs/<slug:slug>/toggle/',
        views.toggle_mech_status,
        name="mech_toggle"
    ),
    path(
        'mechs/<slug:slug>/delete/',
        views.DeleteMechView.as_view(),
        name="mech_delete"
    ),
    path('mechs/<slug:slug>', views.MechDetail.as_view(), name='mech_detail')
]
