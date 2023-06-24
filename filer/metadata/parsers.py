from shared_resources.utils import is_number, is_non_numeric, is_null, to_snake_case


def metadata_parser(metadata):
    ''' iterate over list of one or more raw metadata 
    objects from FILER API and standardize'''
    return { FILERMetadataParser(m).parse() for m in metadata }


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
        self.metadata = self.parse(data)


    def __parse_assay(self, assay):
        return 1


    def __parse_name(self, trackName):
        return 1


    def __split_replicates(self, replicates):
        if is_null(replicates, True):
            return None
        
        if is_non_numeric(replicates) and ',' in replicates:
            return replicates.replace(' ', '').split(',')
        
        return [str(replicates)] # covert to list of 1 string


    def __parse_replicates(self):
        biological = self.__split_replicates(self.metadata['biological_replicates'])
        technical = self.__split_replicates(self.metadata['technical_replicate'])
        
        if biological is None: 
            if technical is None: return None
            return { "technical": technical}
        if technical is None:
            return { "biological": biological}
        
        return { "technical": technical, "biological": biological}


    def __parse_datasource(self):
        dsInfo = { 
                "name": self.metadata['data_source'],
                "url": self.metadata['link_out_url'],
                "experiment_id": self.metadata['encode_experiment_id'],
                }
    
        # project (strip from trackName)
        return dsInfo
    
    
    def __parse_file(self):
        return 1


    def __rename_key(self, key):
        match key:
            case 'antibody':
                return 'antibody_target'
            case 'tabix_file_url':
                return 'indexURL' # for IGV consistency
            case _:
                return key
            

    def __transform_key(self, key):
        # camel -> snake + lower case
        tValue = to_snake_case(key)
        tValue = tValue.replace(" ", "_")
        tValue = tValue.replace("(s)", "s")
        return self.__rename_key(tValue)
        
        
    def __transform_keys(self):
        return { self.__transform_key(key): value for key, value in self.metadata.items()}


    def parse(self):
        ''' parse the FILER metadata & transform/clean up 
        returns parsed / transformed metadata '''
        
        # standardize keys
        self.__transform_keys()
        
        # build data_source object
        
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
