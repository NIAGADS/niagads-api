''' GenomicsdB dataset (accession) data model '''
from db import genomicsdb as gdb

class Dataset(gdb.Model):
    __abstract__ = True
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads'}
    accession = gdb.Column(gdb.String, primary_key=True)
    id = gdb.synonym('accession')
    name = gdb.Column(gdb.String)
    description = gdb.Column(gdb.String)
    attribution = gdb.Column(gdb.String)
