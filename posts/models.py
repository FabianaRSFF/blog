import os
from categorias.models import Categoria
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image


class Post(models.Model):
    titulo_post = models.CharField(max_length=255, verbose_name='Título')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   verbose_name='Autor')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='Data')
    conteudo_post = models.TextField(verbose_name='Conteúdo')
    excerto_post = models.TextField(verbose_name='Excerto')
    categoria_post = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING,
                                       blank=True, null=True,
                                       verbose_name='Categoria')
    img_post = models.ImageField(upload_to='post_img/%Y/%m', blank=True,
                                 null=True, verbose_name='Imagem')
    publicado_post = models.BooleanField(default=False,
                                         verbose_name='Publicado')

    def __str__(self):
        return self.titulo_post

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.img_post:
            self.resize_img(self.img_post.name, 800)

    @staticmethod
    def resize_img(img_name, new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size
        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return

        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(
            img_path,
            optimize=True,
            quality=60,
        )
        new_img.close()
