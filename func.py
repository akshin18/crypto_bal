import pandas as pd
from db import crud, schemas



def add_address_to_db(csv_name, db):
    df = pd.read_csv(csv_name)
    for i,zi in df.iterrows():
        crud.add_address_db(db,schemas.Address(address=zi.iloc[0]) )
