# TODOs

## current

```log
2024-05-21 13:41:28,254 <module> CRITICAL ('Unable to parse FILER metadata, problem with line #: 1287', 'NGEN000019\tENCODE\tENCFF000KXP.bed.gz\t11045\t21296076238\tlong range chromatin interactions\thg19\tHCT116\tCell line\tEFO:0002824\tDigestive\tENCSR000BZX\t1\t1_1\tPOLR2A\tChIA-PET\tbed bed12\t369703\t/project/wang4/GADB/Annotationtracks/ENCODE/data/ChIA-PET/bed12/hg19\t6/4/18\t5/24/12\t8/10/18\thttps://lisanwanglab.org/GADB/Annotationtracks/ENCODE/data/ChIA-PET/bed12/hg19/ENCFF000KXP.bed.gz\te9b488214bc39d462c2c849be95d7e1f\twget https://lisanwanglab.org/GADB/Annotationtracks/ENCODE/data/ChIA-PET/bed12/hg19/ENCFF000KXP.bed.gz -P GADB/Annotationtracks/ENCODE/data/ChIA-PET/bed12/hg19/\twget https://lisanwanglab.org/GADB/Annotationtracks/ENCODE/data/ChIA-PET/bed12/hg19/ENCFF000KXP.bed.gz.tbi -P GADB/Annotationtracks/ENCODE/data/ChIA-PET/bed12/hg19/\thttps://www.encodeproject.org\thttps://www.encodeproject.org/files/ENCFF000KXP/@@download/ENCFF000KXP.bigBed\twget https://lisanwanglab.org/GADB/Annotationtracks/Downloads/ENCODE/ENCFF000KXP.bigBed -P GADB/Annotationtracks/Downloads/ENCODE/\te3cc44b0d9040afe5704913f563e1846\tChromatin Interactions\tChIA-PET protein long range chromatin interactions\tBiosample_summary=HCT116;Lab=Yijun Ruan, JAX;System=digestive system;Submitted_track_name=wgEncodeGisChiaPetHct116Pol2InteractionsRep1.bigBed\tDigestive\tUnknown', {'data_source': 'ENCODE', 'file_name': 'ENCFF000COA.bed.gz', 'number_of_intervals': 145304, 'bp_covered': 293501218, 'output_type': 'peaks', 'genome_build': 'GRCh37', 'biological_replicates': None, 'technical_replicates': None, 'antibody_target': 'H3K4me1', 'assay': 'Histone ChIP-seq', 'file_format': 'bed', 'file_size': 2413868, 'download_date': '06-04-2018', 'release_date': '02-10-2011', 'filer_release_date': '08-10-2018', 'md5sum': '3aaaa7e5c4d4449cc841947b0986fe2b', 'raw_file_url': 'https://tf.lisanwanglab.org/GADB/Annotationtracks/Downloads/ENCODE/ENCFF000COA.bigBed', 'raw_file_md5sum': '8fde6ce257ec96e03b9395d3587084ac', 'data_category': 'called peaks', 'classification': 'Histone ChIP-seq H3K4me1-histone-mark peaks', 'is_lifted': None, 'data_source_version': None, 'biosample_characteristics': {'biosample_term': 'Keratinocyte', 'biosample_term_id': 'CL:0000312', 'biosample_display': 'Keratinocyte', 'biosample_type': 'primary cell', 'tissue_category': 'Skin', 'system_category': 'Integumentary', 'biosample_summary': 'Keratinocyte female//Lab=Bradley Bernstein, Broad//System=integumental system//Submitted_track_name=wgEncodeBroadHistoneNhekH3k4me1StdPk.broadPeak.bigBed'}, 'url': 'https://tf.lisanwanglab.org/GADB/Annotationtracks/ENCODE/data/Histone_ChIP-seq/broadpeak/hg19/ENCFF000COA.bed.gz', 'download_url': 'https://www.encodeproject.org/files/ENCFF000COA/@@download/ENCFF000COA.bigBed', 'file_schema': 'broadPeak', 'experiment_id': 'ENCSR000ALI', 'experiment_info': 'Biosample_summary=Keratinocyte female//Lab=Bradley Bernstein, Broad//System=integumental system//Submitted_track_name=wgEncodeBroadHistoneNhekH3k4me1StdPk.broadPeak.bigBed', 'project': None, 'name': 'NGEN000018: ENCODE Keratinocyte H3K4me1 Histone ChIP-seq peaks', 'analysis': None, 'feature_type': 'histone modification', 'searchable_text': 'Keratinocyte//ENCSR000ALI//primary cell//Skin//Histone ChIP-seq H3K4me1-histone-mark peaks//NGEN000018 ENCODE Keratinocyte H3K4me1 Histone ChIP-seq peaks//called peaks//H3K4me1//ENCODE//CL0000312//Integumentary//peaks//NGEN000018//histone modification//GRCh37//Biosample_summary=Keratinocyte female//Lab=Bradley Bernstein Broad//System=integumental system//Submitted_track_name=wgEncodeBroadHistoneNhekH3k4me1StdPk.broadPeak.bigBed//Histone ChIP-seq//Keratinocyte female//Lab=Bradley Bernstein Broad//System=integumental system//Submitted_track_name=wgEncodeBroadHistoneNhekH3k4me1StdPk.broadPeak.bigBed', 'track_id': 'NGEN000018'}, AttributeError("'int' object has no attribute 'casefold'"))
Traceback (most recent call last):
  File "/home/allenem/projects/dockerized-api/docker-repo/niagads-api/scripts/initialize_filer_cache.py", line 126, in initialize_metadata_cache
    track = parser.parse()
  File "/home/allenem/projects/dockerized-api/venv/lib/python3.10/site-packages/niagads/filer/parser.py", line 616, in parse
    self.__parse_name()
  File "/home/allenem/projects/dockerized-api/venv/lib/python3.10/site-packages/niagads/filer/parser.py", line 395, in __parse_name
    bReps = str_utils.is_null(self._get_metadata('biological_replicates'), True)
  File "/home/allenem/projects/dockerized-api/venv/lib/python3.10/site-packages/niagads/utils/string.py", line 240, in is_null
    if naIsNull and string_in_list(value, ['NA', 'not reported', 'not applicable', '.', 'N/A', 'NULL'], ignoreCase=True):
  File "/home/allenem/projects/dockerized-api/venv/lib/python3.10/site-packages/niagads/utils/string.py", line 28, in string_in_list
    if value.casefold() in (s.casefold() for s in array):
AttributeError: 'int' object has no attribute 'casefold'
```

## Multiple Database Connections

* <https://stackoverflow.com/questions/70081977/multiple-database-connections-using-fastapi>

## Security and Sanitizing

* Very good + rate limiter: <https://escape.tech/blog/how-to-secure-fastapi-api/#validate-and-sanitize-user-input>
* Middleware for `bleaching`: https://github.com/tiangolo/fastapi/discussions/8354
* generic for Python APIs: https://dev.to/mrkanthaliya/validating-and-sanitizing-user-inputs-on-python-projects-rest-api-5a4

## Custom operators in query parameters

* <https://stackoverflow.com/questions/40618327/how-to-design-generic-filtering-operators-in-the-query-string-of-an-api>