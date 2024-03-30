import folium

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_image_url(request, pokemon):
    if pokemon.image:
        return request.build_absolute_uri(pokemon.image.url)
    return DEFAULT_IMAGE_URL


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
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            get_image_url(request, pokemon_entity.pokemon)
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_image_url(request, pokemon),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_object = get_object_or_404(Pokemon, id=int(pokemon_id))

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    local_time = localtime()
    active_pokemon_entities = pokemon_object.entities.filter(
        appeared_at__lte=local_time,
        disappeared_at__gte=local_time
    )

    img_url = get_image_url(request, pokemon_object)
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
        pokemon["previous_evolution"] = {
            "title_ru": pokemon_object.previous_evolution.title,
            "pokemon_id": pokemon_object.previous_evolution.id,
            "img_url": get_image_url(request, pokemon_previous_evolution)
        }

    pokemon_next_evolution = pokemon_object.next_evolutions.first()
    if pokemon_next_evolution:
        pokemon["next_evolution"] = {
            "title_ru": pokemon_next_evolution.title,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": get_image_url(request, pokemon_next_evolution)
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
