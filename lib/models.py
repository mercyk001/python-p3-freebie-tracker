from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)



from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///code.db')
Session = sessionmaker(bind=engine)
session = Session()


#COMPANY CLASS

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    
    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='freebies', back_populates='companies', viewonly=True)

    def __repr__(self):
        return f'<Company {self.name}>'
    
    
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, dev_id=dev.id, company_id=self.id)
        session.add(new_freebie)
        session.commit()
        
        
    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()    
        
        



##DEV CLASS

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs', viewonly=True)


    def __repr__(self):
        return f'<Dev {self.name}>'


    def received_one(self, item_name):
        return any(f.item_name == item_name for f in self.freebies)
    
    
    def give_away(self, session, other_dev, freebie):
     if freebie.dev_id == self.id:
        freebie.dev_id = other_dev.id
        session.add(freebie)
        session.commit()



##FREEBIE CLASS

class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))
    
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')
    
    
    def __repr__(self):
        return f'<Freebie {self.item_name}>'
    
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
    