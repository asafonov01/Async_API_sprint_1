def transform(raw_data):
    for film in raw_data:
        film['_id'] = film['id']
        del film['modified']
        yield film
