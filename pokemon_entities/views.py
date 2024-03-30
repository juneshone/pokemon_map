import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    local_time = localtime()
    active_pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=local_time,
        disappeared_at__gte=local_time
    )
    for pokemon_entity in active_pokemon_entities:
        if pokemon_entity.pokemon.image:
            img_url = request.build_absolute_uri(
                pokemon_entity.pokemon.image.url
            )
        else:
            img_url = DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)
        else:
            img_url = DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon_object = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    local_time = localtime()
    active_pokemon_entities = pokemon_object.entities.filter(
        appeared_at__lte=local_time,
        disappeared_at__gte=local_time
    )

    if pokemon_object.image:
        img_url = request.build_absolute_uri(pokemon_object.image.url)
    else:
        img_url = DEFAULT_IMAGE_URL

    for pokemon_entity in active_pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    pokemon = {
        "pokemon_id": pokemon_object.id,
        "title_ru": pokemon_object.title,
        "title_en": pokemon_object.title_en,
        "title_jp": pokemon_object.title_jp,
        "description": pokemon_object.description,
        "img_url": img_url,
    }

    pokemon_previous_evolution = pokemon_object.previous_evolution
    if pokemon_previous_evolution:
        if pokemon_previous_evolution.image:
            previous_evolution_img_url = request.build_absolute_uri(
                pokemon_previous_evolution.image.url
            )
        else:
            previous_evolution_img_url = DEFAULT_IMAGE_URL
        pokemon["previous_evolution"] = {
            "title_ru": pokemon_object.previous_evolution.title,
            "pokemon_id": pokemon_object.previous_evolution.id,
            "img_url": previous_evolution_img_url
        }

    pokemon_next_evolution = pokemon_object.next_evolutions.first()
    if pokemon_next_evolution:
        if pokemon_next_evolution.image:
            next_evolution_img_url = request.build_absolute_uri(
                pokemon_next_evolution.image.url
            )
        else:
            next_evolution_img_url = DEFAULT_IMAGE_URL
        pokemon["next_evolution"] = {
            "title_ru": pokemon_next_evolution.title,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": next_evolution_img_url
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
