from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, null=True)
    title_en = models.CharField(max_length=200, null=True)
    title_jp = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='images', null=True)
    description = models.TextField(null=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions'
    )


    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_entities')
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)
