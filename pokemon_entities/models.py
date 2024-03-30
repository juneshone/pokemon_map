from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name='название', max_length=200, null=True)
    title_en = models.CharField(
        verbose_name='название на английском', max_length=200, null=True
    )
    title_jp = models.CharField(verbose_name='название на японском', max_length=200, null=True)
    image = models.ImageField(verbose_name='изображение', upload_to='images', null=True)
    description = models.TextField(verbose_name='описание', null=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='из кого эмолюционировал'
    )


    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_entities',
        verbose_name='покемон'
    )
    lat = models.FloatField(verbose_name='широта',)
    lon = models.FloatField(verbose_name='долгота',)
    appeared_at = models.DateTimeField(verbose_name='появится в', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='исчез в', null=True, blank=True)
    level = models.IntegerField(verbose_name='уровень', null=True)
    health = models.IntegerField(verbose_name='здоровье', null=True)
    strength = models.IntegerField(verbose_name='атака', null=True)
    defence = models.IntegerField(verbose_name='защита', null=True)
    stamina = models.IntegerField(verbose_name='выносливость', null=True)
