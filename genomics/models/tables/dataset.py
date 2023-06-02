''' GenomicsdB dataset (accession) data model '''
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import synonym

from db import Base

class Dataset(Base):
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads'}
    
    accession = Column(String, primary_key=True)
    id = synonym('accession')
    name = Column(String)
    description = Column(String)
    attribution = Column(String)
