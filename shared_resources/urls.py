from types import SimpleNamespace

_external = ({'pubmed': 'https://pubmed.ncbi.nlm.nih.gov', 
              'niagads': 'https://www.niagads.org', 
              'filer': 'https://tf.lisanwanglab.org/FILER'})
external = SimpleNamespace(**_external)