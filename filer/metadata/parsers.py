import logging

from urllib.parse import unquote

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
        self.__metadata = data


    def _get_metadata(self, attribute=None):
        """ for debugging, to access private member & also to handle KeyErrors"""
        if attribute is None:
            return self.__metadata
        
        else: 
            return self.__metadata[attribute] \
                if attribute in self.__metadata else None
    

    def __parse_value(self, value):
        ''' catch numbers, booleans, and nulls '''
        if utils.is_null(value, naIsNull=True):
            return None
        
        if utils.is_number(value):
            return utils.to_numeric(value)
            
        return value
    
    
    # TODO map ontology terms to correct     
    # TODO validate ontology terms against GenomicsDB
    def __parse_biosamples(self):
        ''' "cell type": "Middle frontal area 46",
        "Biosample type": "Tissue",
        "Biosamples term id": "UBERON:0006483",            
        "Tissue category": "Brain",
        "Track Description": "Biosample_summary=With Cognitive impairment; middle frontal area 46 tissue female adult (81 years);Lab=Bradley Bernstein, Broad;System=central nervous system;Submitted_track_name=rep1-pr1_vs_rep1-pr2.idr0.05.bfilt.regionPeak.bb;Project=RUSH AD",
        "system category": "Nervous",
        "life stage": "Adult", '''
        # lifeStage = self._get_metadata("life_stage")
        
        biosample = self._get_metadata("cell_type")
        self.__metadata.update({
            "biosample_term": biosample,
            "biosample_term_id": self._get_metadata('biosamples_term_id'),
            "biosample_display": biosample,
            "biosample_type": self._get_metadata("biosample_type").lower()
        })
        
        
            
    def __assign_feature_by_assay(self):
        assay = self._get_metadata('assay')
        if assay is not None:
            if 'QTL' in assay:
                return assay
            if 'TF' in assay:
                return "transcription factor binding site"
            if 'Histone' in assay:
                return "histone modification"
            if assay in ["Small RNA-seq", "short total RNA-seq"]:
                return "small non-coding RNA"   
            if assay in ['FAIRE-seq', 'DNase-seq', 'ATAC-seq']:
                return "chromatin accessibility"
            if assay == 'PRO-seq':
                return "enhancer"
            if assay in ['eCLIP', 'iCLIP', 'RIP-seq']:
                return "protein-RNA crosslink or binding sites"
        
        return None
    
    
    def __assign_feature_by_analysis(self):
        analysis = self._get_metadata('analysis')
        if analysis is not None:
            if analysis == "annotation":
                # check output type
                if 'gene' in self._get_metadata("output_type").lower():
                    return "gene"
                
                # check track_description
                # e.g., All lncRNA annotations
                if 'annotation' in self._get_metadata("track_description"):
                    return utils.regex_extract("All (.+) annotation" , self._get_metadata("track_description"))
            if 'QTL' in analysis:
                return analysis
        
        return None
    
    
    def __assign_feature_by_output_type(self):
        outputType = self._get_metadata("output_type")
        if 'enhancer' in outputType.lower():
            return "enhancer"    
        
        if 'microrna target' in outputType.lower():
            return 'microRNA target'  
        if 'microRNA' in outputType: 
            return "microRNA"     
        if 'exon' in outputType:
            return "exon"        
        if 'transcription start sites' in outputType or 'TSS' in outputType:
            return "transcription start site"      
        if 'transcribed fragments' in outputType:
            return 'transcribed fragment'
        
        if outputType in ["footprints", "hotspots"]:
            # TODO: this may need to be updated, as it varies based on the assay type
            return outputType
        
        # should have been already handled, but just in case
        if outputType in ["clusters", "ChromHMM", "Genomic Partition"]: 
            return None 
        
        if outputType.startswith("Chromatin"): # standardize case
            return outputType.lower()
        
        # peaks are too generic
        # TODO: handle peaks & correctly map, for now
        # just return
        # but there are some "enhancer peaks", which is why
        # this test is 2nd
        if 'peaks' in outputType:
            return outputType  
        
        return outputType
    
    
    def __assign_feature_by_classification(self):
        classification = self._get_metadata('classification').lower()
        if 'histone-mark' in classification:
            return "histone modification"
        if 'chip-seq' in classification or 'chia-pet' in classification:
            if 'consolidated' in classification:
                return self._get_metadata('classification')
            if 'ctcf' in classification:
                return 'CTCF-biding site'
            if 'ctcfl' in classification:
                return 'CTCFL-binding site'
            if classification.startswith('tf '):
                return 'transcription factor binding site'
            
            # next options should have been  caught earier, but just in case
            assay = self._get_metadata('assay')
            if 'Histone' in assay:
                return 'histone modification'
            if 'TF' in assay:
                return 'transcription factor binding site'

        if classification == "rna-pet clusters":
            return "RNA-PET cluster"
        
        return None
    
        
    def __parse_feature_type(self): 
        feature = self.__assign_feature_by_assay()        
        if feature is None: feature = self.__assign_feature_by_analysis()
        if feature is None: feature = self.__assign_feature_by_classification() 
        if feature is None: feature = self.__assign_feature_by_output_type()

        if feature is None:
            raise ValueError("No feature type mapped for track: ", self.__metadata)
        self.__metadata.update({"feature_type": feature})
        
        
    def __parse_data_category(self):
        category = self._get_metadata('data_category')
        if category is not None:
            category = category.lower()
            if category == 'called peaks expression': 
                category = 'called peaks'
            if category == 'qtl':
                category = 'QTL'
            
            self.__metadata.update({"data_category":category})
        

    def __parse_assay(self):
        analysis = None
        assay = self._get_metadata('assay')
        assay = assay.replace('-Seq', '-seq') # consistency
        
        if assay == 'ChromHMM_enhancer':
            assay = 'ChromHMM'
            
        elif assay.lower() == 'annotation':
            assay = None
            analysis = "annotation"
        
        elif assay in ['ChromHMM', "eQTL", "sQTL"]:
            analysis = assay
            assay = None
            
        # TODO: need to check output type b/c assay type may need to be updated
        # e.g. DNASeq Footprinting if output_type == footprints
        elif 'DNase' in assay:
            return "DNase-seq"

        self.__metadata.update({"assay": assay, "analysis": analysis})


    def __parse_name(self):
        #     "trackName": "ENCODE Middle frontal area 46 (repl. 1) TF ChIP-seq CTCF IDR thresholded peaks (narrowPeak) 
        # [Experiment: ENCSR778NDP] [Orig: Biosample_summary=With Cognitive impairment; middle frontal area 46 tissue female adult (81 years);Lab=Bradley Bernstein, Broad;System=central nervous system;Submitted_track_name=rep1-pr1_vs_rep1-pr2.idr0.05.bfilt.regionPeak.bb;Project=RUSH AD] [Life stage: Adult]",
        nameInfo = [self._get_metadata('data_source')]
        
        if self._get_metadata('data_source_version'):
            nameInfo.append('(' + self._get_metadata('data_source_version') + ')')
        
        if self._get_metadata('cell_type'):    
            biosample = self._get_metadata('cell_type')
            if utils.is_number(biosample):
                logger.debug("Found numeric cell_type - " + str(biosample) + " - for track " + self._get_metadata('identifier'))
                biosample = unquote(self._get_metadata('file_name')).split('.')[0].replace(':',' - ')
                logger.debug("Updated to " + biosample + " from file name = " + self._get_metadata('file_name'))
            nameInfo.append(biosample)
            
        if self._get_metadata('antibody_target'):
            nameInfo.append(self._get_metadata('antibody_target'))
        
        if 'DASHR2' in self._get_metadata('output_type'):
            nameInfo.append(self._get_metadata('output_type').replace('DASHR2 ', ''))
        else:
            nameInfo.append(self._get_metadata('assay'))
            nameInfo.append(self._get_metadata('output_type'))
   
        name = self._get_metadata('identifier') + ': ' + ' '.join(nameInfo) 
        
        self.__metadata.update({"name": name})
        
    
    def __parse_experiment_info(self):
        # [Experiment: ENCSR778NDP] [Orig: Biosample_summary=With Cognitive impairment; middle frontal area 46 tissue female adult (81 years);Lab=Bradley Bernstein, Broad;System=central nervous system;Submitted_track_name=rep1-pr1_vs_rep1-pr2.idr0.05.bfilt.regionPeak.bb;Project=RUSH AD]",
        id = self._get_metadata('encode_experiment_id')
        info =  self._get_metadata('track_description')
        project = utils.regex_extract('Project=(.+);*', info) \
                if info is not None else None
        
        self.__metadata.update({
                "experiment_id": id,
                "experiment_info": info,
                "project": project
        })
        

    def __parse_data_source(self):
        dsInfo = self._get_metadata('data_source').split('_', 1)
        source = dsInfo[0]
        version = dsInfo[1] if len(dsInfo) > 1 else None
        if source == 'FANTOM5'and 'slide' in self._get_metadata('link_out_url'):
            version = version + '_SlideBase'
        if 'INFERNO' in source: # don't split on the _
            source = self._get_metadata('data_source')
        
        self.__metadata.update( {
                "data_source": source,
                "data_source_version": version
        })
    
    
    def __parse_file_format(self):
        formatInfo = self._get_metadata('file_format').split(' ')
        format = formatInfo[0]
        schema = formatInfo[1] if len(formatInfo) == 2 else formatInfo[1] + "|" + formatInfo[2]
        self.__metadata.update({"file_format": format[0], "file_schema": schema[1]})
    
    
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
        self.__metadata.update({
                "url": self.__parse_internal_url(self._get_metadata('processed_file_download_url')),
                "raw_file_url": self.__parse_internal_url(self._get_metadata('raw_file_download')),
                "download_url": self.__parse_generic_url(self._get_metadata('raw_file_url'))
        })
        
        
    def __parse_genome_build(self):
        genomeBuild = 'GRCh38' if 'hg38' in self._get_metadata('genome_build') else 'GRCh37'
        self.__metadata.update({"genome_build": genomeBuild})
    
    
    def __parse_is_lifted(self):
        lifted = None
        if 'lifted' in self._get_metadata('genome_build') \
                    or 'lifted' in self._get_metadata('data_source'):
            lifted = True
        self.__metadata.update({"is_lifted": lifted})


    def __rename_key(self, key):
        match key:
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
        self.__metadata = { self.__transform_key(key): self.__parse_value(value) for key, value in self.__metadata.items()}


    def __remove_internal_attributes(self):
        ''' remove internal attributes '''
        internalKeys = ['link_out_url', 'date_added_to_filer', 'processed_file_download_url', 
                'track_description', 'wget_command', 'tabix_index_download', 'encode_experiment_id',
                'cell_type', 'biosample_type', 'biosamples_term_id']
              
        [self.__metadata.pop(key) for key in internalKeys]
 
        
    def parse(self):
        ''' parse the FILER metadata & transform/clean up 
        returns parsed / transformed metadata '''
        
        # standardize keys & convert nulls & numbers from string
        self.__transform_key_values()
        
        # parse concatenated data points into separate attributes
        # standardize others (e.g., urls, data sources)
        # dropping description; allow use cases to piece together out of the other info
        self.__parse_is_lifted()
        self.__parse_genome_build()
        self.__parse_data_source()
        self.__parse_biosamples()
        self.__parse_urls()
        self.__parse_file_format()
        self.__parse_experiment_info()
        self.__parse_name()
        self.__parse_assay()
        self.__parse_data_category()
        self.__parse_feature_type()
        
        # remove private info
        self.__remove_internal_attributes()
        
        # return the 
        return self.__metadata



        

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
        "Track Description": "Biosample_summary=With Cognitive impairment; middle frontal area 46 tissue female adult (81 years);Lab=Bradley Bernstein, Broad;System=central nervous system;Submitted_track_name=rep1-pr1_vs_rep1-pr2.idr0.05.bfilt.regionPeak.bb;Project=RUSH AD",
        "system category": "Nervous",
        "life stage": "Adult",
        # "ENCODE Experiment id": "ENCSR778NDP",
        # "Biological replicate(s)": 1,
        #"Technical replicate": "1_1, 1_2",
        # "Antibody": "CTCF", --> antibody_target
        #"Assay": "TF ChIP-seq",
        #"File format": "bed narrowPeak",
        "File size": 666660,
        #"Downloaded date": "6/12/22",
        #"Release date": "7/23/21",
        #"Date added to FILER": "11/20/22",
        #"Processed File Download URL": "https://lisanwanglab.org/GADB/Annotationtracks/ENCODE/data/TF-ChIP-seq/narrowpeak/hg38/2/ENCFF883PFA.bed.gz",
        #"Processed file md5": "095d38425edff39dbbd099700e54c260",
        #"Link out URL": "https://www.encodeproject.org",
        "Data Category": "Called peaks",
        "classification": "TF ChIP-seq CTCF IDR thresholded peaks",
        "trackName": "ENCODE Middle frontal area 46 (repl. 1) TF ChIP-seq CTCF IDR thresholded peaks (narrowPeak) [Experiment: ENCSR778NDP] [Orig: Biosample_summary=With Cognitive impairment; middle frontal area 46 tissue female adult (81 years);Lab=Bradley Bernstein, Broad;System=central nervous system;Submitted_track_name=rep1-pr1_vs_rep1-pr2.idr0.05.bfilt.regionPeak.bb;Project=RUSH AD] [Life stage: Adult]",
        "tabixFileUrl": "https://lisanwanglab.org/GADB/Annotationtracks/ENCODE/data/TF-ChIP-seq/narrowpeak/hg38/2/ENCFF883PFA.bed.gz.tbi"
    }
    ]
