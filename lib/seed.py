#!/usr/bin/env python3

# Script goes here!
from models import Dev, Company, Freebie, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine =create_engine('sqlite:///code.db')
Session = sessionmaker(bind=engine)
session = Session()


Base.metadata.create_all(engine)

#delete existing data to avoid duplicates
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()
session.commit()



#create companies
c1 = Company(name="Moringa", founding_year=2000)
c2 = Company(name="Wthree", founding_year=1995)
c3 = Company(name="Dengineering", founding_year=2010)

#create developers
d1 = Dev(name="Mercy")
d2 = Dev(name="Bob")
d3 = Dev(name="Bena")



# Add and commit to get IDs assigned
session.add_all([c1, c2, c3, d1, d2, d3])
session.commit()

# Create freebies (each links dev and company)
f1 = Freebie(item_name="Mug", value=10, dev_id=d1.id, company_id=c1.id)
f2 = Freebie(item_name="T-shirt", value=20, dev_id=d2.id, company_id=c2.id)
f3 = Freebie(item_name="Sticker", value=2, dev_id=d1.id, company_id=c3.id)
f4 = Freebie(item_name="USB Drive", value=15, dev_id=d3.id, company_id=c1.id)
f5 = Freebie(item_name="Notebook", value=8, dev_id=d2.id, company_id=c3.id)
f6 = Freebie(item_name="Pen", value=3, dev_id=d3.id, company_id=c2.id)

session.add_all([f1, f2, f3, f4, f5, f6])
session.commit()

print("Database seed done!")