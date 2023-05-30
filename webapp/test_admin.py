""" Contains the testcases for admin.py """
# django imports occur at runtime, so fail linter
# pylint:disable=import-error
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
# pylint:enable=import-error
from .models import Mech
from .admin import MechAdmin


class MockRequest(object):
    """ Empty request used to simulate a web call """
    pass


request = MockRequest()


class TestAdmin(TestCase):
    """ Class used to manage admin test cases """

    def __init__(self, *args, **kwargs):
        """ used in tests to set up session for calls to admin """
        super(TestAdmin, self).__init__(*args, **kwargs)
        self.mech_admin = MechAdmin(Mech, AdminSite())

    def test_approve_mech_approves(self):
        """ Check availability changes from 0 to 1 """
        Mech.objects.create(
            name='Test Mech',
            status=0
            )
        queryset = Mech.objects.filter(name='Test Mech')
        self.mech_admin.approve_mech(request, queryset)
        self.assertEqual(Mech.objects.get(name='Test Mech').status, 1)

    def test_revoke_mech_revokes(self):
        """ Check availability changes from 0 to 1 """
        Mech.objects.create(
            name='Test Mech',
            status=1
            )
        queryset = Mech.objects.filter(name='Test Mech')
        self.mech_admin.revoke_mech(request, queryset)
        self.assertEqual(Mech.objects.get(name='Test Mech').status, 0)
