# TODOs

## current

```log
2024-05-29 01:15:12,961 <module> CRITICAL ('Unable to parse FILER metadata, problem with line #: 60574', 'NGFTB01079\tFactorbook_v1_UCSC\tA-Box.pfm\tNot applicable\tNot applicable\tPWMs\tNot applicable\tNot applicable\tNot applicable\tNot applicable\tNot applicable\tNot applicable\tNot applicable\tNot applicable\tNot applicable\tNot applicable\tPFM\t770\t/project/wang4/GADB/Annotationtracks/Factorbook_v1_UCSC/frequency-matrix/pfm\t4/1/24\t8/16/13\t4/15/24\thttps://tf.lisanwanglab.org/GADB/Annotationtracks/Factorbook_v1_UCSC/frequency-matrix/pfm/A-Box.pfm\t6810b502c6814e8c7491ccc2286d4b3c\twget https://tf.lisanwanglab.org/GADB/Annotationtracks/Factorbook_v1_UCSC/frequency-matrix/pfm/A-Box.pfm -P GADB/Annotationtracks/Factorbook_v1_UCSC/frequency-matrix/pfm/\tNot applicable\thttps://genome.ucsc.edu/cgi-bin/hgTrackUi?hgsid=2057466232_cZzcnxdDVYXVhETfI6CnhaQ9isID&c=chr1&g=wgEncodeRegTfbsClusteredV3\thttps://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/factorbookMotifPwm.txt.gz\twget https://tf.lisanwanglab.org/GADB/Annotationtracks/Downloads/Factorbook_v1_UCSC/hg19/factorbookMotifPwm.txt -P GADB/Annotationtracks/Downloads/Factorbook_v1_UCSC/hg19/\t40658f9296beeb96238cc1129b353ae0\tPosition weighted matrix\tPWMs\tNot applicable\tNot applicable\tNot applicable', {'data_source': 'Factorbook', 'file_name': 'ZZZ3_HeLa-S3_FILER_wgEncodeRegTfbsClusteredV3.withMotif.bed.gz', 'number_of_intervals': 1433, 'bp_covered': 19690, 'output_type': 'Motif ovelap', 'genome_build': 'GRCh37', 'biological_replicates': None, 'technical_replicates': None, 'antibody_target': 'ZZZ3', 'assay': 'ChIP-seq', 'file_format': 'bed', 'file_size': 24398, 'download_date': '04-01-2024', 'release_date': '08-16-2013', 'filer_release_date': '04-15-2024', 'md5sum': '1dc7ee22538e9ee614cc5f1ac87eb58a', 'raw_file_url': 'https://tf.lisanwanglab.org/GADB/Annotationtracks/Downloads/Factorbook_v1_UCSC/hg19/factorbookMotifPos.txt.gz', 'raw_file_md5sum': '60c9dc26b657aa552fef326d694d74c7', 'data_category': 'transcription factor binding site', 'classification': 'ChIP-seq Motif ovelap', 'is_lifted': False, 'data_source_version': 'v1_UCSC', 'biosample_characteristics': {'biosample_term': 'HeLa-S3', 'biosample_display': 'HeLa-S3', 'biosample_type': 'cell line', 'tissue_category': 'Female Reproductive', 'system_category': 'Reproductive'}, 'url': 'https://tf.lisanwanglab.org/GADB/Annotationtracks/Factorbook_v1_UCSC/ChIP-seq/motif-overlap/bed9/hg19/ZZZ3_HeLa-S3_FILER_wgEncodeRegTfbsClusteredV3.withMotif.bed.gz', 'download_url': 'https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/factorbookMotifPos.txt.gz', 'file_schema': 'bed3+6|FactorbookMotifs', 'experiment_id': None, 'experiment_info': 'HeLa-S3;treatment=None;lab=Harvard', 'project': None, 'name': 'NGFTB01078: Factorbook (v1_UCSC) HeLa-S3 ZZZ3 ChIP-seq Motif ovelap', 'analysis': None, 'feature_type': 'Motif ovelap', 'searchable_text': 'cell line;Factorbook;v1_UCSC;Reproductive;Motif ovelap;ChIP-seq Motif ovelap;transcription factor binding site;Female Reproductive;HeLa-S3treatment=Nonelab=Harvard;NGFTB01078;NGFTB01078 Factorbook (v1_UCSC) HeLa-S3 ZZZ3 ChIP-seq Motif ovelap;ChIP-seq;GRCh37;HeLa-S3;ZZZ3', 'track_id': 'NGFTB01078'}, TypeError('sequence item 2: expected str instance, NoneType found'))
Traceback (most recent call last):
  File "/home/allenem/projects/docker-api/docker-repo/niagads-api/scripts/initialize_filer_cache.py", line 126, in initialize_metadata_cache
    track = parser.parse()
  File "/home/allenem/projects/docker-api/venv/lib/python3.10/site-packages/niagads/filer/parser.py", line 633, in parse
    self.__parse_name()
  File "/home/allenem/projects/docker-api/venv/lib/python3.10/site-packages/niagads/filer/parser.py", line 408, in __parse_name
    name = self._get_metadata('identifier') + ': ' + ' '.join(nameInfo)
TypeError: sequence item 2: expected str instance, NoneType found

```

## Multiple Database Connections

* <https://stackoverflow.com/questions/70081977/multiple-database-connections-using-fastapi>

## Security and Sanitizing

* Very good + rate limiter: <https://escape.tech/blog/how-to-secure-fastapi-api/#validate-and-sanitize-user-input>
* Middleware for `bleaching`: https://github.com/tiangolo/fastapi/discussions/8354
* generic for Python APIs: https://dev.to/mrkanthaliya/validating-and-sanitizing-user-inputs-on-python-projects-rest-api-5a4

## Custom operators in query parameters

* <https://stackoverflow.com/questions/40618327/how-to-design-generic-filtering-operators-in-the-query-string-of-an-api>