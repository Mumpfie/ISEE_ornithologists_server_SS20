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

    bird_cols = {
        'Taxon': 'taxon',
        'Genus': 'genus',
        'Order': 'order',
        'Family (Scientific)': 'family_scientific_name',
        'Species (Scientific)': 'species_scientific_name',
        'shape': 'shape',
        'Breeding Range': 'breeding',
        'Breeding Range-Subregion(s)': 'subregion',
        'picture_url': 'picture_url'
    }

    birds: pd.DataFrame = pd.read_csv(
        'server/eu_birds_with_pic_and_shape.csv',
        usecols = bird_cols.keys()
    )

    birds.rename(columns=bird_cols, inplace=True)

    # TODO: implement some kind of ARRAY(ENUM(Breeding)) to handle multiple regions for a bird
    birds = birds.assign(breeding='eu')

    birds.to_sql('bird', engine, if_exists='append', index_label='id')

