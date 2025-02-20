
from typing import List, Optional, TypeVar, Union

from niagads.reference.chromosomes import Human
from pydantic import field_serializer

from api.models.base_response_models import PagedResponseModel
from api.models.base_row_models import RowModel
from api.models.genome import Gene, GenomicRegion
from api.routers.genomics.models.variant import Variant

# TODO: NHGRI GWAS Catalog/ADVP data -> maybe just make VariantScore a `GenericDataModel`

class VariantScore(RowModel):
    variant: Variant
    test_allele: str
    track_id: str
    chromosome: Human
    position: int
    
    @field_serializer("chromosome")
    def serialize_group(self, chromosome: Human, _info):
        return str(chromosome)


T_VariantScore = TypeVar('T_VariantScore', bound=VariantScore)


class VariantPValueScore(VariantScore):
    p_value: Union[float, str]
    neg_log10_pvalue: float
    
    
class QTL(VariantPValueScore):
    z_score: Optional[float] = None
    dist_to_target: Optional[float] = None
    target: Gene

class GWASSumStatResponse(PagedResponseModel):
    response: List[VariantPValueScore]
    
class QTLResponse(PagedResponseModel):
    response: List[QTL]
    
