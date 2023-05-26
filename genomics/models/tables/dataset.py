''' GenomicsdB dataset (accession) data model '''
from db import genomicsdb as gdb

class Dataset(gdb.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads'}
    accession = gdb.Column(gdb.String, primary_key=True)
    id = gdb.synonym('accession')
    name = gdb.Column(gdb.String)
    description = gdb.Column(gdb.String)
    attribution = gdb.Column(gdb.String)

class Dataset_GRCh37(gdb.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads'}
    accession = gdb.Column(gdb.String, primary_key=True)
    id = gdb.synonym('accession')
    name = gdb.Column(gdb.String)
    description = gdb.Column(gdb.String)
    attribution = gdb.Column(gdb.String)
