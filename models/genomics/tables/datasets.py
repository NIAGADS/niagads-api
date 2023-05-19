''' GenomicsdB dataset (accession) data model '''
from db import genomicsdb as gdb
# from sqlalchemy import Table, Column, Integer, String, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base


class Dataset(gdb.Model):
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads'}
    accession = gdb.Column(gdb.String, primary_key=True)
    name = gdb.Column(gdb.String)
    description = gdb.Column(gdb.String)
    attribution = gdb.Column(gdb.String)

    def json(self):
        return {'name': self.name, 
                'description': self.description, 
                'data_source': 'NIAGADS',
                'id': self.accession, 
                'attribution': self.attribution.split('|')[0],
                'publication': self.attribution.split('|')[1] if '|' in self.attribution else None
                }


# select accession as id, name, description, attribution from niagads.datasetattributes where accession like 'NG0%';
