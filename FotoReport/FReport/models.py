from django.db import models


class Scr_res(models.Model):
    scr_res_1 = models.IntegerField(default=384, verbose_name='Разрешение видео')
    scr_res_2 = models.IntegerField(default=288, verbose_name='Разрешение видео')

    def __str__(self):
        return str(self.scr_res_1) + '*' + str(self.scr_res_2)

    class Meta:
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешение'


class Clips(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название ролика')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления ролика')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')
    # photo = models.ImageField(upload_to="ClipsPhotos/%Y/%m/%d/", blank=True,  verbose_name='Превью')
    scr_res_id = models.ForeignKey('Scr_res', on_delete=models.PROTECT, default=4, verbose_name='Разрешение видео')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Ролик'
        verbose_name_plural = 'Ролики'


class PhotoRep(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    Scr_id = models.ForeignKey('Scr', on_delete=models.PROTECT)
    Clips_id = models.ForeignKey('Clips', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Фото_отчеты'
        verbose_name_plural = 'Фото_отчет'

    def __str__(self):
        return str(self.created_at)


class Scr(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    nameb = models.IntegerField(verbose_name='Номер экрана')
    Dir = models.CharField(max_length=50, default='atv', verbose_name='Ресурс')
    ip_add = models.GenericIPAddressField(protocol='both', verbose_name='IP_адрес', default='10.10.0.1')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Фото экрана')
    Check = models.BooleanField(verbose_name='Активен', default=True)
    scr_res = models.ForeignKey('scr_res', on_delete=models.PROTECT, default=1, verbose_name='Разрешение видео')

    def __str__(self):
        return (self.ip_add + "..........." + str(self.scr_res) + '...........' + self.name)

    class Meta:
        verbose_name = 'Экран'
        verbose_name_plural = 'Экраны'
