import logging
from shared_resources import utils
from shared_resources.constants import URLS

logger = logging.getLogger(__name__)

def metadata_parser(metadata):
    ''' iterate over list of one or more raw metadata 
    objects from FILER API and standardize'''
    return { FILERMetadataParser(m).parse() for m in metadata }

def split_replicates(replicates):
    if utils.is_null(replicates, True):
        return None
    
    if utils.is_non_numeric(replicates) and ',' in replicates:
        return replicates.replace(' ', '').split(',')
    
    return [str(replicates)] # covert to list of 1 string


class FILERMetadataParser:
    ''' parser for FILER metadata:
    standardizes keys, extracts non-name info from name, cleans up
    
      keys:
            -- replace spaces with _
            -- lower case
            -- camelCase to snake_case
            -- rename fields, e.g., antibody -> antibody_target
            -- remove (s)
        
        values:
            -- genome build: hg38 -> GRCh38, hg19 -> GRCh37
            -- build biosample object
            -- build file info object
            -- build data source object
            -- extract [] fields from trackName
            -- original trackName --> description
            -- add feature type
            -- remove TF etc from assay
    
    '''
    
    def __init__(self, data):
        self.metadata = data


    def __parse_value(self, value):
        ''' catch numbers, booleans, and nulls '''
        if utils.is_null(value, naIsNull=True):
            return None
        
        if utils.is_number(value):
            return utils.to_numeric(value)
            
        return value


    def __parse_feature_type(self):
        featureType = self.metadata['assay'].split(" ")[0]
        return 1

    def __parse_assay(self):
        assayInfo = self.metadata['assay'].split(" ")
        return 1


    def __parse_name(self):
        return 1


    def __parse_data_source(self):
        source, version = self.metadata('data_source').split('_', 1)
        if source == 'FANTOM5'and 'slide' in self.metadata['link_out_url']:
            version = version + '_SlideBase'
        if 'INFERNO' in source: # don't split on the _
            source = self.metadata['data_source']
        
        self.metadata.update( {
                "data_source": source,
                "data_source_version": version
        })
    
    
    def __parse_file(self):
        return 1
    
    
    def __parse_generic_url(self, url):
        ''' handle common fixes to all URL fields '''
        if 'wget' in url:
            url = url.split(' ')[1]
            
        return url
    
    
    def __parse_internal_url(self, url):
        ''' correct domain and other formatting issues
        ''' 
        url = self.__parse_generic_url(url)           
        return utils.regex_replace('^[^GADB]*', URLS.filer_downloads, url)
    
    
    def __parse_urls(self):
        self.metadata.update({
                "url": self.__parse_internal_url(self.metadata['processed_file_download_url']),
                "raw_file_url": self.__parse_internal_url(self.metadata['raw_file_download']),
                "download_url": self.__parse_generic_url(self.metadata['raw_file_url'])
        })
        
        
    def __parse_genome_build(self):
        if 'hg38' in self.metadata['genome_build']:
            self.metadata['genome_build'] = 'GRCh38'
        else:
            self.metadata['genome_build'] = 'GRCh37'
    
    
    def __parse_is_lifted(self):
        lifted = None
        if 'lifted' in self.metadata['genome_build'] or 'lifted' in self.metadata['data_source']:
            lifted = True
        self.metadata.update({"is_lifted": lifted})


    def __rename_key(self, key):
        match key:
            case 'track_description':
                return 'description'
            case 'antibody':
                return 'antibody_target'
            case 'downloaded_date':
                return 'download_date'
            case 'processed_file_md5':
                return 'md5sum'
            case 'raw_file_md5':
                return 'raw_file_md5sum'
            case 'technical_replicate': # for consistency
                return 'technical_replicates'
            case _:
                return key
            

    def __transform_key(self, key):
        # camel -> snake + lower case
        tValue = utils.to_snake_case(key)
        tValue = tValue.replace(" ", "_")
        tValue = tValue.replace("(s)", "s")
        return self.__rename_key(tValue)
        
        
    def __transform_key_values(self):
        ''' transform keys and since iterating over 
            the metadata anyway, catch nulls, numbers and convert from string
        '''
        self.metadata = { self.__transform_key(key): self.__parse_value(value) for key, value in self.metadata.items()}


    def __remove_internal_attributes(self):
        ''' remove internal attributes '''
        internalKeys = ['link_out_url', 'date_added_to_filer', 'processed_file_download_url', 
                'wget_command', 'tabix_index_download']
        [self.metadata.pop(key) for key in internalKeys]
 
        
    def parse(self):
        ''' parse the FILER metadata & transform/clean up 
        returns parsed / transformed metadata '''
        
        # standardize keys & convert nulls & numbers from string
        self.__transform_key_values()
        
        # parse concatenated data points into separate attributes
        # standardize others (e.g., urls, data sources)
        self.__parse_is_lifted()
        self.__parse_genome_build()
        self.__parse_data_source()
        self.__parse_urls()
          
        # remove private info
        self.__remove_internal_attributes()
        
        
        # return the 
        return self.metadata



        

    example = [
    {
        "Identifier": "NGEN060616",
        # "Data Source": "ENCODE",
        "File name": "ENCFF883PFA.bed.gz",
        "Number of intervals": 38312,
        "bp covered": 13276246,
        "Output type": "IDR thresholded peaks",
        "Genome build": "hg38",
        "cell type": "Middle frontal area 46",
        "Biosample type": "Tissue",
        "Biosamples term id": "UBERON:0006483",
        "Tissue category": "Brain",
        # "ENCODE Experiment id": "ENCSR778NDP",
        # "Biological replicate(s)": 1,
        #"Technical replicate": "1_1, 1_2",
        # "Antibody": "CTCF", --> antibody_target
        "Assay": "TF ChIP-seq",
        "File format": "bed narrowPeak",
        "File size": 666660,
        "Downloaded date": "6/12/22",
        "Release date": "7/23/21",
        "Date added to FILER": "11/20/22",
        "Processed File Download URL": "https://lisanwanglab.org/GADB/Annotationtracks/ENCODE/data/TF-ChIP-seq/narrowpeak/hg38/2/ENCFF883PFA.bed.gz",
        "Processed file md5": "095d38425edff39dbbd099700e54c260",
        "Link out URL": "https://www.encodeproject.org",
        "Data Category": "Called peaks",
        "classification": "TF ChIP-seq CTCF IDR thresholded peaks",
        "Track Description": "Biosample_summary=With Cognitive impairment; middle frontal area 46 tissue female adult (81 years);Lab=Bradley Bernstein, Broad;System=central nervous system;Submitted_track_name=rep1-pr1_vs_rep1-pr2.idr0.05.bfilt.regionPeak.bb;Project=RUSH AD",
        "system category": "Nervous",
        "life stage": "Adult",
        "trackName": "ENCODE Middle frontal area 46 (repl. 1) TF ChIP-seq CTCF IDR thresholded peaks (narrowPeak) [Experiment: ENCSR778NDP] [Orig: Biosample_summary=With Cognitive impairment; middle frontal area 46 tissue female adult (81 years);Lab=Bradley Bernstein, Broad;System=central nervous system;Submitted_track_name=rep1-pr1_vs_rep1-pr2.idr0.05.bfilt.regionPeak.bb;Project=RUSH AD] [Life stage: Adult]",
        "tabixFileUrl": "https://lisanwanglab.org/GADB/Annotationtracks/ENCODE/data/TF-ChIP-seq/narrowpeak/hg38/2/ENCFF883PFA.bed.gz.tbi"
    }
    ]
    
# https://lisanwanglab.org/GADB/Annotationtracks/DASHRv2/Small_RNA-Seq/hg19/DASHR1_GEO_hg19/adipose1_GSE45159_peaks_annot_hg19.bed.gz.tbi
# https://lisanwanglab.org/GADB/Annotationtracks/DASHRv2/Small_RNA-Seq/hg19/DASHR1_GEO_hg19/adipose1_GSE45159_peaks_annot_hg19.bed.gz
