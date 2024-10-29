from typing import Any, List, Optional, Union

from niagads.utils.string import dict_to_info_string

from ..common.formatters import id2title
from .base_models import GenericDataModel, PagedResponseModel, RowModel

class BEDFeature(GenericDataModel):
    chrom: str
    chromStart: int
    chromEnd: int
    name: Optional[str] = '.'
    score: Optional[Union[str, int, float]] = '.'
    strand: Optional[str] = '.'
    
    def to_view_data(self, view, **kwargs):
        if kwargs['collapseExtras']:
            data: dict = { k:v for k, v in self.model_dump().items() if k in list(self.model_fields.keys())}
            extraData =  { k:v for k, v in self.model_dump().items() if k in list(self.model_extra.keys()) and k != 'track_id'}
            data.update({'track_id': self.track_id, 'additional_fields': dict_to_info_string(extraData)})
            return data
        else:
            return self.model_dump()

    def get_view_config(self, view, **kwargs):
        """ get configuration object required by the view """
        match view:
            case view.TABLE:
                return self.__build_table_config(kwargs['collapseExtras'])
            case _:
                raise NotImplementedError(f'View `{view.value}` not yet supported for this response type')
        
    def __build_table_config(self, collapseExtras:bool):
        """ Return a column and options object for niagads-viz-js/Table """
        fields = list(self.model_fields.keys()) + ['track_id']
        if len(self.model_extra) > 0:
            if collapseExtras: 
                fields = fields + ['additional_fields']
            else:
                fields += [k for k in self.model_extra.keys() if k != 'track_id']
                
        columns: List[dict] = [ {'id': f, 'header': id2title(f)} for f in fields]
        return {'columns': columns, 
            'options': { 'disableColumnFilters': True}}
    

class BEDResponse(PagedResponseModel):
    response: List[BEDFeature]
    
    def to_view(self, view, **kwargs):
        # need to override here b/c each row may have different fields
        extras = set()
        dynamicExtras = False
        row: BEDFeature
        for row in self.response:
            if row.has_extras():
                if len(extras) == 0:
                    extras = set(row.model_extra.keys())
                else:
                    dynamicExtras = extras != set(row.model_extra.keys())
                    if dynamicExtras: break
        
        return super().to_view(view, collapseExtras=dynamicExtras)
