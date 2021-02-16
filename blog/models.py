from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(
        verbose_name='Título',
        max_length=200,
    )
    author = models.ForeignKey(
        'auth.User',
        verbose_name='Autor',
        on_delete=models.CASCADE,
    )
    body = models.TextField(
        verbose_name='Cuerpo'
    )

    # Los siguientes metodos definen la dirección a la que se
    # dirigen cuando se actualiza cualquiera de las tablas de este modelo
    # en este caso, a la url 'post/<int.pk>'
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
