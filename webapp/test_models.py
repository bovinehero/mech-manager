""" Contains the testcases for models.py """
# django imports occur at runtime, so fail linter
# pylint:disable=import-error
from django.test import TestCase
# pylint:enable=import-error
from .models import Mech


class TestModels(TestCase):
    """ Class used to manage admin test cases """

    def test_mech_defaults(self):
        """ Test to check new Mech Defaults are set correctly """
        mech = Mech.objects.create(
            name='Test Mech',
            )
        self.assertEqual(mech.status, 0)
        self.assertEqual(mech.category, 0)
        self.assertEqual(mech.weight, 0)
        self.assertEqual(mech.tech_level, 0)
        self.assertEqual(mech.role, 0)
        self.assertEqual(mech.description, '')
        self.assertEqual(mech.record_sheet, 'custom')
        self.assertEqual(mech.battle_value, 9999)
        self.assertEqual(mech.status, 0)

    def test_mech_string_method_returns_name(self):
        """ Test to check new Mech id is set to name """
        mech = Mech.objects.create(
            name='Test Mech',
            )
        self.assertEqual(str(mech), 'Test Mech')
