
from typing import List

from api.models.response_model_properties import QueryDefinition

from ..models.feature_score import xQTL

class xQTLResult(QueryDefinition):
    name = 'xqtl-track-top-hits'
    query = """"""
    useIdCTE = False
    resultType = List[xQTL]
    bindParameters = ['id']
    fetchOne = False
    errorOnNull = "xQTL track not found in the NIAGADS Alzheimer's GenomicsDB"