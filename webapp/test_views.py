from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.http import HttpResponseServerError
from django.core.exceptions import PermissionDenied, ViewDoesNotExist
from django.urls import reverse
from webapp import urls, models
from .views import (
    error_403, error_404, error_500,
    CardList, CreateMechForm, UpdateMechForm, UpdateMechView
)


class TestHandlerViews(TestCase):

    def test_500_error(self):
        factory = RequestFactory()
        request = factory.get('/')
        response = error_500(request)
        self.assertEqual(response.status_code, 500)

    def test_404_error(self):
        factory = RequestFactory()
        request = factory.get('/')
        response = error_404(request,  exception=ViewDoesNotExist())
        self.assertEqual(response.status_code, 404)

    def test_403_error(self):
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
        checks mechlist
        redirects if not logged in arenders if logged in
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        response = self.client.get('/mechs/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'mechs.html')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get('/mechs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mechs.html')

    def test_get_mech_detail(self):
        """
        checks mech detail
        redirects if not logged in renders if logged in
        """
        self.user = User.objects.create_user(
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
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/mechs/{queryset[0].slug}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mech_detail.html')

    def test_toggle_mech_status(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.admin = User.objects.create_superuser(
            username='testadmin', password='12345'
        )
        mech = models.Mech.objects.create(
            name='testm',
            slug='testm',
            status='1'
        )
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/mechs/{mech.slug}/toggle/')
        self.assertEqual(response.status_code, 403)
        login2 = self.client.login(username='testadmin', password='12345')
        response = self.client.get(f'/mechs/{mech.slug}/toggle/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/mechs/')
        updated_mech = models.Mech.objects.get(name=mech.name)
        self.assertEquals(updated_mech.status, 0)
        response = self.client.get(f'/mechs/{updated_mech.slug}/toggle/')
        updated_mech_again = models.Mech.objects.get(name=mech.name)
        self.assertEquals(updated_mech_again.status, 1)

    def test_is_the_create_form_is_valid(self):
        # creating new test user
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.admin = User.objects.create_superuser(
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
        login = self.client.login(username='testuser', password='12345')
        response = self.client.post('/mechs/create/')
        self.assertEqual(response.status_code, 403)
        login2 = self.client.login(username='testadmin', password='12345')
        # creating the mech
        response = self.client.post('/mechs/create/', data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        # checking is the mech created
        self.assertTrue(models.Mech.objects.filter(
             name=data['name']).exists())

    def test_is_the_update_form_is_valid(self):
        # creating new test user
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.admin = User.objects.create_superuser(
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
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/mechs/{mech.slug}/update/')
        self.assertEqual(response.status_code, 403)
        login2 = self.client.login(username='testadmin', password='12345')
        # creating the mech
        response = self.client.post(
            f'/mechs/{mech.slug}/update/', data=data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        # checking is the mech created
        self.assertTrue(models.Mech.objects.filter(
             name=data['name']).exists())

    def test_is_the_delete_form_is_valid(self):
        # creating new test user
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.admin = User.objects.create_superuser(
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
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/mechs/{mech.slug}/delete/')
        self.assertEqual(response.status_code, 403)
        login2 = self.client.login(username='testadmin', password='12345')
        # creating the mech
        response = self.client.post(
            f'/mechs/{mech.slug}/delete/', data=data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        # checking is the mech created
        self.assertFalse(models.Mech.objects.filter(
             name=data['name']).exists())
