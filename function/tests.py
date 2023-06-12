from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse,resolve
from .views import index, function, prepare
from .models import QuadFunction


class QuadFunctionTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username' : 'testuser',
            'password' : 'secret'}
        User.objects.create_user(**self.credentials)

    """
    Test sprawdza poprawność ścieżki dla url main.
    """
    def test_url_main(self):
        url = reverse('main')
        self.assertEquals(resolve(url).func, index)

    """
    Test sprawdza poprawność ścieżki dla url function.
    """
    def test_url_function(self):
        url = reverse('function')
        self.assertEquals(resolve(url).func, function)
    """
    Test sprawdza czy da się poprawnie wejść pod url main i sprawdza czy funkcja widoku zwraca poprawny template.
    """
    def test_view_main(self):
        client = Client()
        response = client.get(reverse('main'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'main.html')

    """
    Test sprawdza czy da się poprawnie wejść pod url function.
    Należy się najpierw zalogować, ponieważ ten url wymaga autoryzacji.
    """
    def test_view_function(self):
        client = Client()
        response = client.post(reverse('function'), self.credentials,follow=True)
        self.assertEquals(response.status_code, 200)

    """
    Test sprawdza czy stworzony rekord w Bazie danych nie jest pusty.
    """
    def test_model_not_empty_quad_function(self):
        user = User.objects.create_user(username='user')
        q_function = QuadFunction.objects.create(user=user, example='x^2+1', plot="test.jpg")
        self.assertNotEqual(q_function, None)

    """
        Test sprawdza czy funkcja, która przygotowuje dane z formularza zwraca poprawne wartości. 
    """
    def test_prepare(self):
        self.assertEquals(prepare("x^2"), ([1], False))
        self.assertEquals(prepare("x^2+1"), ([1, 1], False))
        self.assertEquals(prepare("x^2+x"), ([1, 1], True))
        self.assertEquals(prepare("x^2+x+1"), ([1, 1, 1], True))
