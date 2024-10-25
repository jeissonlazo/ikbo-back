from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://shopping_cart_owner:DPyCA59TOQhu@ep-long-pine-a4ah2n1q-pooler.us-east-1.aws.neon.tech/shopping_cart?sslmode=require'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()