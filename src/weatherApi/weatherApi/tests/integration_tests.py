import pytest

@pytest.mark.django_db
def test_weather(api_client) -> None:
    response_with_existing_city = api_client.get('/api/v1/weather/Hennef')
    assert response_with_existing_city.status_code == 200
    assert response_with_existing_city.data['city_name'] == "Hennef (Sieg)"
    assert response_with_existing_city.data['city_longitude'] == 7.2847945
    assert response_with_existing_city.data['city_latitude'] == 50.7754417
    assert response_with_existing_city.data['wind_direction'] in ['North','South','East','West']

    response_with_existing_city_german = api_client.get('/api/v1/weather/Cologne', headers={'Accept-Language': 'de'})
    assert response_with_existing_city_german.status_code == 200
    assert response_with_existing_city_german.data['city_name'] == "Köln"
    assert response_with_existing_city_german.data['city_longitude'] == 6.959974
    assert response_with_existing_city_german.data['city_latitude'] == 50.938361
    assert response_with_existing_city_german.data['wind_direction'] in ['Nord', 'Süd', 'Ost', 'West']

    response_with_existing_city_finish = api_client.get('/api/v1/weather/London', headers={'Accept-Language': 'fi'})
    assert response_with_existing_city_finish.status_code == 200
    assert response_with_existing_city_finish.data['city_name'] == "Lontoo"
    assert response_with_existing_city_finish.data['city_longitude'] == -0.1276474
    assert response_with_existing_city_finish.data['city_latitude'] == 51.5073219
    assert response_with_existing_city_finish.data['wind_direction'] in ['Pohjoinen', 'Etelä', 'Itä', 'Länsi']

    response_with_fake_city = api_client.get('/api/v1/weather/City17')
    assert response_with_fake_city.status_code == 404
    assert response_with_fake_city.data['detail'] == "Not found."

    response_with_fake_city_german = api_client.get('/api/v1/weather/City17', headers={'Accept-Language': 'de'})
    assert response_with_fake_city_german.status_code == 404
    assert response_with_fake_city_german.data['detail'] == "Nicht gefunden."

    response_with_fake_city_finish = api_client.get('/api/v1/weather/City17', headers={'Accept-Language': 'fi'})
    assert response_with_fake_city_finish.status_code == 404
    assert response_with_fake_city_finish.data['detail'] == "Ei löydy."