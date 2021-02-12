from django.contrib.auth import get_user_model # Para referenciar usuario activo
from django.test import TestCase, Client # Para simular llamadas GET & POST
# siempre que se esté probando vistas se usará `Client()`
from django.urls import reverse
from .models import Post


class BlogTests(TestCase):

    # se añade una entrada de blog de muestra para probar y luego se confirma
    # que tanto la representación de la cadena como el contenido son correctos
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body content')

    # para confirmar que la página de inicio devuelve un código de estado *HTTP 200*,
    # contiene el texto del cuerpo y usa la plantilla `home.html` correcta
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')

    # comprueba que la página de detalles funciona como se espera y que una
    # página incorrecta devuelve un *404*
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_get_absolute_url(self):  # new
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_post_create_view(self):  # new
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_post_update_view(self):  # new
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):  # new
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)
