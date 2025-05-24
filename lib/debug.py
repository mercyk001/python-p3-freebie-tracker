#!/usr/bin/env python3
    
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///code.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Fetch first entries
    company = session.query(Company).first()
    dev = session.query(Dev).first()
    freebie = session.query(Freebie).first()

    print("== Basic Relationships ==")
    print("First company:", company)
    if company:
        print("Company's freebies:", company.freebies)
        print("Company's devs:", company.devs)

    print("First dev:", dev)
    if dev:
        print("Dev's freebies:", dev.freebies)
        print("Dev's companies:", dev.companies)

    print("First freebie:", freebie)
    if freebie:
        print("Freebie's dev:", freebie.dev)
        print("Freebie's company:", freebie.company)

    print("\n== Freebie.print_details() ==")
    if freebie:
        print(freebie.print_details())  # e.g., "Alice owns a Mug from TechCorp"

    print("\n== Company.give_freebie(dev, item_name, value) ==")
    if company and dev:
        print(f"Giving {dev.name} a Hoodie from {company.name}")
        company.give_freebie(dev, "Hoodie", 30)

    print("\n== Company.oldest_company() ==")
    oldest = Company.oldest_company()
    print("Oldest company:", oldest)

    print("\n== Dev.received_one(item_name) ==")
    print(f"Has {dev.name} received a Hoodie? {dev.received_one('Hoodie')}")
    print(f"Has {dev.name} received a Laptop? {dev.received_one('Laptop')}")

    print("\n== Dev.give_away(dev, freebie) ==")
    owned_freebie = dev.freebies[0]
    another_dev = session.query(Dev).filter(Dev.id != dev.id).first()
    if owned_freebie and another_dev:
       print(f"{dev.name} is giving away {owned_freebie.item_name} to {another_dev.name}")
       dev.give_away(session, another_dev, owned_freebie)
       print(f"New owner of {owned_freebie.item_name}: {owned_freebie.dev.name}")

       
    else:
        print("Not enough data to test give_away.")
