""" Contains the testcases for models.py """
# django imports occur at runtime, so fail linter
# pylint:disable=import-error
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
# from django.http import HttpResponseServerError
from django.core.exceptions import PermissionDenied, ViewDoesNotExist
# pylint:enable=import-error
from webapp import models
from .views import error_403, error_404, error_500


class TestViews(TestCase):
    """ Class used to manage view test cases """

    def test_500_error(self):
        """ tests a 500 error returns correctly """
        factory = RequestFactory()
        request = factory.get('/')
        response = error_500(request)
        self.assertEqual(response.status_code, 500)

    def test_404_error(self):
        """ tests a 404 error returns correctly """
        factory = RequestFactory()
        request = factory.get('/')
        response = error_404(request,  exception=ViewDoesNotExist())
        self.assertEqual(response.status_code, 404)

    def test_403_error(self):
        """ tests a 403 error returns correctly """
        factory = RequestFactory()
        request = factory.get('/')
        response = error_403(request, exception=PermissionDenied())
        self.assertEqual(response.status_code, 403)

    def test_get_index_page(self):
        """ checks index page loads correct page """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_mech_list(self):
        """
        Test checks mechlist
        test redirect if not logged in and
        creates user and then correctly renders logged in
        """
        User.objects.create_user(
            username='testuser', password='12345'
        )
        response = self.client.get('/mechs/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'mechs.html')
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/mechs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mechs.html')

    def test_get_mech_detail(self):
        """
        Test checks mech detail
        test redirect if not logged in and
        creates user and then correctly renders logged in
        """
        User.objects.create_user(
            username='testuser', password='12345'
        )
        mech = models.Mech.objects.create(
            name='testor',
            slug='testor',
            status='1'
        )
        queryset = models.Mech.objects.filter(name=mech.name)
        self.assertEqual(queryset[0].name, mech.name)
        response = self.client.get(f'/mechs/{queryset[0].slug}')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'mech_detail.html')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/mechs/{queryset[0].slug}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mech_detail.html')

    def test_toggle_mech_status(self):
        """
        Test toggle availability
        creates regular user and tests permissions
        creates admin user, tests permissions and toggle both ways
        """
        User.objects.create_user(
            username='testuser', password='12345'
        )
        User.objects.create_superuser(
            username='testadmin', password='12345'
        )
        mech = models.Mech.objects.create(
            name='testm',
            slug='testm',
            status='1'
        )
        self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/mechs/{mech.slug}/toggle/')
        self.assertEqual(response.status_code, 403)
        self.client.login(username='testadmin', password='12345')
        response = self.client.get(f'/mechs/{mech.slug}/toggle/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/mechs/')
        updated_mech = models.Mech.objects.get(name=mech.name)
        self.assertEquals(updated_mech.status, 0)
        response = self.client.get(f'/mechs/{updated_mech.slug}/toggle/')
        updated_mech_again = models.Mech.objects.get(name=mech.name)
        self.assertEquals(updated_mech_again.status, 1)

    def test_is_the_create_form_is_valid(self):
        """
        Tests Create a new Mech
        creates regular and admin users
        logs in and checks permissions for regular user
        logs in and checks permissions for admin user
        creates admin user, tests permissions and toggle both ways
        creates a new mech and validates
        """
        User.objects.create_user(
            username='testuser', password='12345'
        )
        User.objects.create_superuser(
            username='testadmin', password='12345'
        )
        data = {
            'name': 'testm',
            'category': 0,
            'weight': 0,
            'slug': 'testm',
            'status': 0,
            'tech_level': 0,
            'role': 0,
            'description': 'Test description',
            'record_sheet': 'custom',
            'battle_value': 9999

        }
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/mechs/create/')
        self.assertEqual(response.status_code, 403)
        self.client.login(username='testadmin', password='12345')
        response = self.client.post('/mechs/create/', data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Mech.objects.filter(
             name=data['name']).exists())

    def test_is_the_update_form_is_valid(self):
        """
        Tests Edit an existing Mech
        creates regular and admin users
        logs in and checks permissions for regular user
        logs in and checks permissions for admin user
        creates a new mech and validates
        performs an update and validates changes
        """
        User.objects.create_user(
            username='testuser', password='12345'
        )
        User.objects.create_superuser(
            username='testadmin', password='12345'
        )
        mech = models.Mech.objects.create(
            name='testm',
            slug='testm',
            status='1'
        )
        data = {
            'name': 'testm',
            'category': 0,
            'weight': 0,
            'slug': 'testm',
            'status': 0,
            'tech_level': 0,
            'role': 0,
            'description': 'Test description',
            'record_sheet': 'custom',
            'battle_value': 9999
        }
        data_edit = {
            'name': 'testo',
            'category': 1,
            'weight': 1,
            'slug': 'testo',
            'status': 1,
            'tech_level': 1,
            'role': 1,
            'description': 'Test description new',
            'record_sheet': 'locust',
            'battle_value': 9998
        }
        self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/mechs/{mech.slug}/update/')
        self.assertEqual(response.status_code, 403)
        self.client.login(username='testadmin', password='12345')
        response = self.client.post('/mechs/create/', data=data, follow=True)
        self.assertTrue(models.Mech.objects.filter(
             name=data['name']).exists())
        response = self.client.post(
            f'/mechs/{mech.slug}/update/', data=data_edit, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Mech.objects.filter(
             name=data_edit['name']).exists())

    def test_is_the_delete_form_is_valid(self):
        """
        Tests Delete an existing Mech
        creates regular and admin users
        logs in and checks permissions for regular user
        logs in and checks permissions for admin user
        creates a new mech and validates
        performs an delete and validates change
        """
        User.objects.create_user(
            username='testuser', password='12345'
        )
        User.objects.create_superuser(
            username='testadmin', password='12345'
        )
        mech = models.Mech.objects.create(
            name='testm',
            slug='testm',
            status='1'
        )
        data = {
            'name': 'testm',
            'category': 0,
            'weight': 0,
            'slug': 'testm',
            'status': 0,
            'tech_level': 0,
            'role': 0,
            'description': 'Test description',
            'record_sheet': 'custom',
            'battle_value': 9999

        }
        self.assertTrue(models.Mech.objects.filter(
             name=data['name']).exists())
        self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/mechs/{mech.slug}/delete/')
        self.assertEqual(response.status_code, 403)
        self.client.login(username='testadmin', password='12345')
        # creating the mech
        response = self.client.post(
            f'/mechs/{mech.slug}/delete/', data=data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        # checking is the mech created
        self.assertFalse(models.Mech.objects.filter(
             name=data['name']).exists())
