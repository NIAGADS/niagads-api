import re
from shared_resources.utils import is_number, is_non_numeric, is_null


def parse_assay(assay):
    return 1

def parse_name(trackName):
    return 1


def split_replicates(replicates):
    if is_null(replicates):
        return None
    
    if is_non_numeric(replicates) and ',' in replicates:
        return replicates.replace(' ', '').split(',')
    
    return [str(replicates)] # covert to list of strings


def parse_replicates(metadata):
    biological = split_replicates(metadata['biological_replicates'])
    technical = split_replicates(metadata['technical_replicate'])
    
    if biological is None: 
        if technical is None: return None
        return { "technical": technical}
    if technical is None:
        return { "biological": biological}
    
    return { "technical": technical, "biological": biological}

def parse_datasource(metadata):
    dsInfo = { 
            "name": metadata['data_source'],
            "url": metadata['link_out_url'],
            "experiment_id": metadata['encode_experiment_id'],
            }
 
    # project (strip from trackName)
    return dsInfo
 
 
def parse_file(metadata):
    return 1
 
def rename_key(key):
    match key:
        case 'antibody':
            return 'antibody_target'
        case 'tabix_file_url':
            return 'indexURL' # for IGV consistency
        case _:
            return key
        

def to_snake_case(key):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', key).lower()

def transform_key(key):
    # camel -> snake + lower case
    tValue = to_snake_case(key)
    tValue = tValue.replace(" ", "_")
    tValue = tValue.replace("(s)", "s")
    return rename_key(tValue)
    
    
def transform_keys(metadata):
    return { transform_key(key): value for key, value in metadata.items()}

def metadata_parser():
    ''' parse the FILER metadata & transform/clean up
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
    metadata = transform_keys(metadata)
    # build data_source object
    

    

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
