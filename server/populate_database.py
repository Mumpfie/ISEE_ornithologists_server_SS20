import pandas as pd
from sqlalchemy import Integer, String, Enum

from server.database import engine
from server import models
from server.queryClasses import Shape, Breeding

if __name__ == "__main__":

    models.Base.metadata.create_all(bind=engine)

    # Families

    families: pd.DataFrame = pd.read_csv(
        'server/eu_birds_with_pic_and_shape.csv',
        usecols=[
            'Family (Scientific)',
            'Family (English)'
        ]
    )

    families.columns = [
        'name_scientific',
        'name_english'
    ]

    families.drop_duplicates(['name_scientific'], inplace=True)


    families.to_sql('family', engine, if_exists='append', index=False)


    # Species

    species: pd.DataFrame = pd.read_csv(
        'server/eu_birds_with_pic_and_shape.csv',
        usecols=[
            'Species (Scientific)',
            'Species (English)'
        ]
    )

    species.columns = [
        'name_scientific',
        'name_english'
    ]

    species.drop_duplicates(['name_scientific'], inplace=True)

    species.to_sql('species', engine, if_exists='append', index=False)

    # Birds

    birds: pd.DataFrame = pd.read_csv(
        'server/eu_birds_with_pic_and_shape.csv',
        usecols = [
            'Taxon',
            'Genus',
            'Order',
            'Family (Scientific)',
            'Species (Scientific)',
            'shape',
            'Breeding Range',
            'Breeding Range-Subregion(s)',
            'picture_url',
        ]
    )

    birds.columns = [
        'taxon',
        'genus',
        'order',
        'family_scientific_name',
        'species_scientific_name',
        'shape',
        'breeding',
        'subregion',
        'picture_url'
    ]

    types= {
        'taxon': String,
        'genus': String,
        'order': String,
        'family_scientific_name': String,
        'species_scientific_name': String,
        'shape': Shape,
        'breeding': Breeding,
        'subregion': String,
        'picture_url': String
    }

    birds.to_sql('bird', engine, if_exists='append', index_label='id') # TODO:, dtype=types)

