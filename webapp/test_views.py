from django.test import TestCase, Client, RequestFactory
from django.http import HttpResponseServerError
from django.core.exceptions import PermissionDenied, ViewDoesNotExist
from django.urls import reverse
from webapp import urls
from .views import error_403, error_404, error_500
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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