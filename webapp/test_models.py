from django.test import TestCase
from .models import Mech, TECH, ROLE, CLASSIFICATION, WEIGHTS, STATUS

class TestModels(TestCase):

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