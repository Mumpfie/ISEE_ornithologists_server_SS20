import pandas as pd

from app.config.config import engine
from app.model import models

if __name__ == "__main__":

    models.Base.metadata.create_all(bind=engine)

    # Birds

    bird_cols = {
        'Taxon': 'taxon',
        'Genus': 'genus',
        'Order': 'order',
        'shape': 'shape',
        'Breeding Range': 'breeding',
        'Breeding Range-Subregion(s)': 'subregion',
        'picture_url': 'picture_url',
        'Family (Scientific)': 'family_name_scientific',
        'Family (English)': 'family_name_english',
        'Species (Scientific)': 'species_name_scientific',
        'Species (English)': 'species_name_english'
    }

    birds: pd.DataFrame = pd.read_csv(
        'eu_birds_with_pic_and_shape.csv',
        usecols = bird_cols.keys()
    )

    birds.rename(columns=bird_cols, inplace=True)

    # TODO: implement some kind of ARRAY(ENUM(Breeding)) to handle multiple regions for a bird
    birds = birds.assign(breeding='eu')

    birds.to_sql('bird', engine, if_exists='append', index_label='id')

