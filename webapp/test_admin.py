from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from .models import Mech
from .admin import MechAdmin


class MockRequest(object):
    pass

request = MockRequest()


class TestAdmin(TestCase):

    def setUp(self):
        self.mech_admin = MechAdmin(Mech, AdminSite())

    def test_approve_mech_approves(self):
        mech = Mech.objects.create(
            name='Test Mech',
            status=0
            )
        queryset = Mech.objects.filter(name='Test Mech')
        self.mech_admin.approve_mech(request, queryset)
        self.assertEqual(Mech.objects.get(name='Test Mech').status, 1)

    def test_revoke_mech_revokes(self):
        mech = Mech.objects.create(
            name='Test Mech',
            status=1
            )
        queryset = Mech.objects.filter(name='Test Mech')
        self.mech_admin.revoke_mech(request, queryset)
        self.assertEqual(Mech.objects.get(name='Test Mech').status, 0)