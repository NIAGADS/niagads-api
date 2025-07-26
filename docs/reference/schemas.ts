export const API_SCHEMAS = {
	AbridgedGeneResponse: {
		properties: {
			data: {
				items: { $ref: "#/components/schemas/Gene" },
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "AbridgedGeneResponse",
	},
	AbridgedTrack: {
		properties: {
			id: { type: "string", title: "Track" },
			name: { type: "string", title: "Name" },
			description: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Description",
			},
			genome_build: {
				type: "string",
				title: "Genome Build",
			},
			feature_type: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Feature",
			},
			is_download_only: {
				anyOf: [{ type: "boolean" }, { type: "null" }],
				title: "Download Only",
				description:
					"File is available for download only; data cannot be queried using the NIAGADS Open Access API.",
				default: false,
			},
			data_source: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Data Source",
				description: "original data source for the track",
			},
			data_category: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Category",
				description: "data category; may be analysis type",
			},
			url: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Download URL",
				description: "URL for NIAGADS-standardized file",
			},
		},
		additionalProperties: true,
		type: "object",
		required: ["id", "name", "genome_build"],
		title: "AbridgedTrack",
	},
	AbridgedTrackResponse: {
		properties: {
			data: {
				items: {
					$ref: "#/components/schemas/AbridgedTrack",
				},
				type: "array",
				title: "Data",
				description:
					"Abridged metadata for each track meeting the query criteria.  Depending on query may include count of records matching query parameters.",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "AbridgedTrackResponse",
	},
	AbridgedVariantResponse: {
		properties: {
			data: {
				items: { $ref: "#/components/schemas/Variant" },
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "AbridgedVariantResponse",
	},
	AlleleFrequencies: {
		properties: {
			population: {
				$ref: "#/components/schemas/FrequencyPopulation",
				title: "Population",
				order: 1,
			},
			allele: {
				type: "string",
				title: "Allele",
				order: 3,
			},
			data_source: {
				type: "string",
				title: "Resource",
				description:
					"original data source for the frequency information",
				order: 2,
			},
			frequency: {
				type: "string",
				title: "Frequency",
				order: 4,
			},
		},
		type: "object",
		required: ["population", "allele", "data_source", "frequency"],
		title: "AlleleFrequencies",
	},
	AnnotatedGene: {
		properties: {
			id: {
				type: "string",
				title: "Ensembl ID",
				description: "Ensembl gene identifier",
			},
			symbol: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Gene Symbol",
				description: "official gene symbol",
			},
			type: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Type",
			},
			name: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Name",
			},
			synonyms: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Aliases",
				descriptions: "gene symbol synonyms or aliases",
			},
			location: {
				$ref: "#/components/schemas/GenomicRegion",
				title: "Location",
				description:
					"genomic location delimiting the footprint (span) of the gene",
			},
			cytogenic_location: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Cytogenic Location",
				description: "mapping the gene to a band of the chromosome",
			},
			nomenclature: {
				anyOf: [
					{
						additionalProperties: {
							anyOf: [{ type: "string" }, { type: "integer" }],
						},
						type: "object",
					},
					{ type: "null" },
				],
				title: "Nomenclature",
			},
			go_annotation: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/GOAnnotation",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Go Annotation",
			},
			pathway_membership: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/PathwayAnnotation",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Pathway Membership",
			},
		},
		type: "object",
		required: ["id", "location"],
		title: "AnnotatedGene",
	},
	AnnotatedGenomicRegion: {
		properties: {
			id: { type: "string", title: "Region ID" },
			location: {
				$ref: "#/components/schemas/GenomicRegion",
			},
			num_structural_variants: {
				type: "integer",
				title: "Num. Strucutral Variants",
				description:
					"number of SVs contained within or overlapping the region",
			},
			num_genes: {
				type: "integer",
				title: "Num. Genes",
				description:
					"number of genes contained within or overlapping the region",
			},
			num_small_variants: {
				anyOf: [{ type: "integer" }, { type: "string" }],
				title: "Num. Small Variants",
				description:
					"number of SNVs, MVNs, and short INDELs (<50bp) contained within or overlapping the region; for regions > 50,000bp this number is not calculated",
			},
		},
		type: "object",
		required: [
			"id",
			"location",
			"num_structural_variants",
			"num_genes",
			"num_small_variants",
		],
		title: "AnnotatedGenomicRegion",
	},
	AnnotatedVariant: {
		properties: {
			allele_string: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Allele String",
			},
			is_adsp_variant: {
				anyOf: [{ type: "boolean" }, { type: "null" }],
				title: "Is ADSP Variant?",
				description:
					"Variant present in ADSP samples and passed quality control checks; not an indicator of AD-risk.",
				default: false,
			},
			most_severe_consequence: {
				anyOf: [
					{
						$ref: "#/components/schemas/PredictedConsequenceSummary",
					},
					{ type: "null" },
				],
				title: "Predicted Consequence",
				description: "most severe consequence predicted by VEP",
			},
			id: { type: "string", title: "Variant", order: 1 },
			ref_snp_id: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Ref SNP ID",
				order: 1,
			},
			variant_class: {
				type: "string",
				title: "Variant Type",
			},
			location: {
				$ref: "#/components/schemas/GenomicRegion",
			},
			ref: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Ref",
			},
			alt: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Alt",
			},
			is_multi_allelic: {
				type: "boolean",
				title: "Is Multi-allelic?",
				description:
					"flag indicating whether the dbSNP refSNP is multi-allelic",
				default: false,
			},
			is_structural_variant: {
				type: "boolean",
				title: "Is SV?",
				description:
					"flag indicating whether the variant is a structural variant",
				default: false,
			},
			cadd_score: {
				anyOf: [
					{ $ref: "#/components/schemas/CADDScore" },
					{ type: "null" },
				],
				title: "CADD Score(s)",
				description: "score of the deleteriousness of a variant",
			},
			adsp_qc: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/QCStatus",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Adsp Qc",
			},
		},
		type: "object",
		required: ["id", "variant_class", "location"],
		title: "AnnotatedVariant",
	},
	AnnotatedVariantFeature: {
		properties: {
			allele_string: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Allele String",
			},
			is_adsp_variant: {
				anyOf: [{ type: "boolean" }, { type: "null" }],
				title: "Is ADSP Variant?",
				description:
					"Variant present in ADSP samples and passed quality control checks; not an indicator of AD-risk.",
				default: false,
			},
			most_severe_consequence: {
				anyOf: [
					{
						$ref: "#/components/schemas/PredictedConsequenceSummary",
					},
					{ type: "null" },
				],
				title: "Predicted Consequence",
				description: "most severe consequence predicted by VEP",
			},
			id: { type: "string", title: "Variant", order: 1 },
			ref_snp_id: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Ref SNP ID",
				order: 1,
			},
		},
		type: "object",
		required: ["id"],
		title: "AnnotatedVariantFeature",
	},
	AssociationSource: {
		type: "string",
		enum: ["GWAS", "CURATED", "ALL"],
		title: "AssociationSource",
	},
	AssociationTrait: {
		type: "string",
		enum: ["AD", "ADRD", "BIOMARKER", "ALL_AD", "ALL", "OTHER"],
		title: "AssociationTrait",
		description: "enum genetic association trait category",
	},
	BiosampleCharacteristics: {
		properties: {
			system: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Biosample: Anatomical System",
			},
			tissue: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Biosample: Tissue",
			},
			biomarker: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Biomarker",
			},
			biosample_type: {
				anyOf: [
					{ $ref: "#/components/schemas/BiosampleType" },
					{ type: "string" },
					{ type: "null" },
				],
				title: "Biosample Type",
			},
			biosample: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/OntologyTerm",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Biosample",
				description: "ontology term/id pairs describing the biosample",
			},
			life_stage: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Biosample: Life Stage",
				description: "donor or sample life stage",
			},
		},
		type: "object",
		title: "BiosampleCharacteristics",
	},
	BiosampleType: {
		enum: [
			{
				term: "experimentally modified cell in vitro",
				term_id: "CL_0000578",
			},
			{ term: "cell line", term_id: "CLO_0000031" },
			{
				term: "embryonic stem cell line cell",
				term_id: "CLO_0037279",
			},
			{
				term: "induced pluripotent stem cell line cell",
				term_id: "CLO_0037307",
			},
			{ term: "cell", term_id: "CL:0000000" },
			{ term: "primary cell", term_id: "EFO_0002660" },
			{ term: "stem cell", term_id: "CL_0000034" },
			{ term: "primary cell culture", term_id: "CL_0000001" },
			{ term: "tissue", term_id: "UBERON_0000479" },
			{ term: "organoid", term_id: "NCIT_C172259" },
		],
		title: "BiosampleType",
	},
	CADDScore: {
		properties: {
			phred: {
				type: "number",
				title: "CADD PHRED-scaled Score",
				description:
					"Normalized score representing rank of variant in genome-wide distribution; higher value suggests variant is more likely to be functionally significant. For SNVs, score of 20 or higher is in the top 1% of all potential causal variants",
			},
			raw: {
				type: "number",
				title: "CADD Raw Score",
				description:
					"initial, unscaled output from the CADD model; not directly comparable across experiments",
			},
		},
		type: "object",
		required: ["phred", "raw"],
		title: "CADDScore",
	},
	Collection: {
		properties: {
			id: {
				type: "string",
				title: "Collection ID",
				description:
					"Unique collection identifier; may be a NIAGADS Dataset Accession",
			},
			name: { type: "string", title: "Name" },
			description: { type: "string", title: "Description" },
			num_tracks: {
				type: "integer",
				title: "Number of Tracks",
				description: "number of data tracks in the collection",
			},
		},
		type: "object",
		required: ["id", "name", "description", "num_tracks"],
		title: "Collection",
	},
	CollectionResponse: {
		properties: {
			data: {
				items: { $ref: "#/components/schemas/Collection" },
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "CollectionResponse",
	},
	ColocatedVariants: {
		properties: {
			alternative_alleles: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Alternative Alleles",
			},
			colocated_variants: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Colocated Variants",
			},
		},
		type: "object",
		title: "ColocatedVariants",
	},
	ConsequenceImpact: {
		type: "string",
		enum: ["HIGH", "MODERATE", "LOW", "MODIFIER"],
		title: "ConsequenceImpact",
	},
	Entity: {
		type: "string",
		enum: ["gene", "variant", "region", "track", "collection"],
		title: "Entity",
	},
	ExperimentalDesign: {
		properties: {
			antibody_target: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Antibody Target",
			},
			assay: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Assay",
			},
			analysis: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Analysis",
			},
			classification: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Classification",
			},
			data_category: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Data Category",
			},
			output_type: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Output Type",
			},
			is_lifted: {
				anyOf: [{ type: "boolean" }, { type: "null" }],
				title: "Is Lifted?",
				description: "data are lifted from earlier genome build",
			},
			covariates: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Covariates",
			},
		},
		type: "object",
		title: "ExperimentalDesign",
	},
	FileProperties: {
		properties: {
			file_name: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "File Name",
			},
			url: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Url",
			},
			md5sum: {
				anyOf: [
					{
						type: "string",
						pattern: "^[a-fA-F0-9]{32}$",
					},
					{ type: "null" },
				],
				title: "Md5Sum",
			},
			bp_covered: {
				anyOf: [{ type: "integer" }, { type: "null" }],
				title: "Bp Covered",
			},
			num_intervals: {
				anyOf: [{ type: "integer" }, { type: "null" }],
				title: "Num Intervals",
			},
			file_size: {
				anyOf: [{ type: "integer" }, { type: "null" }],
				title: "File Size",
			},
			file_format: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "File Format",
			},
			file_schema: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "File Schema",
			},
		},
		type: "object",
		title: "FileProperties",
	},
	FrequencyPopulation: {
		properties: {
			abbreviation: { type: "string", title: "Population" },
			population: { type: "string", title: "Population" },
			description: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Description",
			},
		},
		type: "object",
		required: ["abbreviation", "population"],
		title: "FrequencyPopulation",
	},
	GOAnnotation: {
		properties: {
			go_term_id: { type: "string", title: "GO Term ID" },
			go_term: { type: "string", title: "Term" },
			ontology: { type: "string", title: "Ontology" },
			evidence: {
				items: { $ref: "#/components/schemas/GOEvidence" },
				type: "array",
				title: "Evidence Code",
				description:
					"GO Evidence Code. See https://geneontology.org/docs/guide-go-evidence-codes/.",
			},
		},
		type: "object",
		required: ["go_term_id", "go_term", "ontology", "evidence"],
		title: "GOAnnotation",
	},
	GOEvidence: {
		properties: {
			citation: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Citation",
				description:
					"PMID or GO Reference (non-PMID) used by the GO consortium.  See https://geneontology.org/gorefs.html.",
				examples: ["GO_REF:0000024"],
			},
			qualifier: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Qualifier",
				description: "context for interpreting the GO annotation",
				examples: ["involved_in"],
			},
			evidence_code: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "ECO ID",
				description:
					"term id in the Evidence and Conclusion Ontology.  See https://www.evidenceontology.org/.",
				examples: ["ECO:0000250"],
			},
			go_evidence_code: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Evidence Code",
				description:
					"GO Evidence Code. See https://geneontology.org/docs/guide-go-evidence-codes/.",
			},
			annotation_source: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Annotation Source",
				description: "annotator",
			},
		},
		type: "object",
		title: "GOEvidence",
	},
	GWASSumStatResponse: {
		properties: {
			data: {
				items: {
					$ref: "#/components/schemas/VariantPValueScore",
				},
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "GWASSumStatResponse",
	},
	Gene: {
		properties: {
			id: {
				type: "string",
				title: "Ensembl ID",
				description: "Ensembl gene identifier",
			},
			symbol: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Gene Symbol",
				description: "official gene symbol",
			},
			type: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Type",
			},
			name: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Name",
			},
			synonyms: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Aliases",
				descriptions: "gene symbol synonyms or aliases",
			},
			location: {
				$ref: "#/components/schemas/GenomicRegion",
				title: "Location",
				description:
					"genomic location delimiting the footprint (span) of the gene",
			},
			cytogenic_location: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Cytogenic Location",
				description: "mapping the gene to a band of the chromosome",
			},
		},
		type: "object",
		required: ["id", "location"],
		title: "Gene",
	},
	GeneAnnotationResponse: {
		properties: {
			data: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/GenePathwayMembership",
						},
						type: "array",
					},
					{
						items: {
							$ref: "#/components/schemas/GeneFunction",
						},
						type: "array",
					},
					{
						items: {
							$ref: "#/components/schemas/RowModel",
						},
						type: "array",
					},
				],
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "GeneAnnotationResponse",
	},
	GeneFeature: {
		properties: {
			id: {
				type: "string",
				title: "Ensembl ID",
				description: "Ensembl gene identifier",
			},
			symbol: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Gene Symbol",
				description: "official gene symbol",
			},
		},
		type: "object",
		required: ["id"],
		title: "GeneFeature",
	},
	GeneFunction: {
		properties: {
			go_term_id: { type: "string", title: "GO Term ID" },
			go_term: { type: "string", title: "Term" },
			ontology: { type: "string", title: "Ontology" },
			evidence: {
				items: { $ref: "#/components/schemas/GOEvidence" },
				type: "array",
				title: "Evidence Code",
				description:
					"GO Evidence Code. See https://geneontology.org/docs/guide-go-evidence-codes/.",
			},
		},
		type: "object",
		required: ["go_term_id", "go_term", "ontology", "evidence"],
		title: "GeneFunction",
	},
	GenePathwayMembership: {
		properties: {
			pathway: { type: "string", title: "Pathway" },
			pathway_id: { type: "string", title: "Pathway ID" },
			pathway_source: {
				type: "string",
				title: "Source",
				description: "data source for the pathway annotation",
			},
		},
		type: "object",
		required: ["pathway", "pathway_id", "pathway_source"],
		title: "GenePathwayMembership",
	},
	GeneResponse: {
		properties: {
			data: {
				items: {
					$ref: "#/components/schemas/AnnotatedGene",
				},
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "GeneResponse",
	},
	GeneVariantAssociation: {
		properties: {
			variant: {
				$ref: "#/components/schemas/AnnotatedVariantFeature",
				title: "Variant",
				order: 1,
			},
			test_allele: {
				type: "string",
				title: "Test Allele",
				order: 2,
			},
			p_value: {
				anyOf: [{ type: "number" }, { type: "string" }],
				title: "p-Value",
				order: 3,
			},
			trait: {
				$ref: "#/components/schemas/OntologyTerm",
				title: "Trait",
				description: "associated trait",
				order: 4,
			},
			trait_category: {
				type: "string",
				title: "Trait Category",
				description:
					"One of AD, ADRD, Biomarker (for AD/ADRD), or Other",
				order: 5,
			},
			track_id: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Track ID",
				order: 6,
			},
			study: {
				type: "string",
				title: "Study",
				description:
					"NIAGADS Data Track or published study curated from the literature or a GWAS Catalog",
				order: 7,
			},
			pubmed_id: {
				anyOf: [
					{
						items: {
							type: "string",
							pattern: "^([0-9]{8}|PMID:[0-9]{8})$",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Publication",
				order: 8,
			},
			neg_log10_pvalue: {
				type: "number",
				title: "-log10pValue",
			},
			relative_position: {
				type: "string",
				title: "Relative Position",
				description: "location relative to the gene footprint",
				order: 0,
			},
		},
		type: "object",
		required: [
			"variant",
			"test_allele",
			"p_value",
			"trait",
			"trait_category",
			"study",
			"neg_log10_pvalue",
			"relative_position",
		],
		title: "GeneVariantAssociation",
	},
	GeneticAssociationResponse: {
		properties: {
			data: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/VariantAssociation",
						},
						type: "array",
					},
					{
						items: {
							$ref: "#/components/schemas/GeneVariantAssociation",
						},
						type: "array",
					},
				],
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "GeneticAssociationResponse",
	},
	GenomicRegion: {
		properties: {
			start: { type: "integer", title: "Start" },
			end: {
				anyOf: [{ type: "integer" }, { type: "null" }],
				title: "End",
			},
			chr: {
				$ref: "#/components/schemas/Human",
				title: "Chromosome",
			},
			length: {
				anyOf: [{ type: "integer" }, { type: "null" }],
				title: "Length",
			},
			strand: {
				anyOf: [
					{ $ref: "#/components/schemas/Strand" },
					{ type: "null" },
				],
				title: "Strand",
				default: "+",
			},
		},
		type: "object",
		required: ["start", "chr"],
		title: "GenomicRegion",
	},
	HTTPValidationError: {
		properties: {
			detail: {
				items: {
					$ref: "#/components/schemas/ValidationError",
				},
				type: "array",
				title: "Detail",
			},
		},
		type: "object",
		title: "HTTPValidationError",
	},
	Human: {
		type: "string",
		enum: [
			"1",
			"2",
			"3",
			"4",
			"5",
			"6",
			"7",
			"8",
			"9",
			"10",
			"11",
			"12",
			"13",
			"14",
			"15",
			"16",
			"17",
			"18",
			"19",
			"20",
			"21",
			"22",
			"X",
			"Y",
			"M",
		],
		title: "Human",
	},
	MessageResponse: {
		properties: {
			data: {
				additionalProperties: true,
				type: "object",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["request"],
		title: "MessageResponse",
	},
	OntologyTerm: {
		properties: {
			term: {
				type: "string",
				title: "Ontology Term",
				description: "a term from a controlled vocabular or ontology",
			},
			term_id: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Ontology Term ID",
				description: "mapped ontology term ID",
			},
		},
		type: "object",
		required: ["term"],
		title: "OntologyTerm",
	},
	PaginationDataModel: {
		properties: {
			page: {
				type: "integer",
				title: "Page",
				description:
					"if result is paged, indicates the current page of the result; defaults to 1",
				default: 1,
			},
			total_num_pages: {
				type: "integer",
				title: "Total Num Pages",
				description:
					"if the result is paged, reports total number of pages in the full result set (response); defaults to 1",
				default: 1,
			},
			paged_num_records: {
				anyOf: [{ type: "integer" }, { type: "null" }],
				title: "Paged Num Records",
				description:
					"number of records in the current paged result set (response)",
			},
			total_num_records: {
				anyOf: [{ type: "integer" }, { type: "null" }],
				title: "Total Num Records",
				description:
					"total number of records in the full result set (response)",
			},
		},
		type: "object",
		title: "PaginationDataModel",
		description: "Captures pagination status.",
	},
	PathwayAnnotation: {
		properties: {
			pathway: { type: "string", title: "Pathway" },
			pathway_id: { type: "string", title: "Pathway ID" },
			pathway_source: {
				type: "string",
				title: "Source",
				description: "data source for the pathway annotation",
			},
		},
		type: "object",
		required: ["pathway", "pathway_id", "pathway_source"],
		title: "PathwayAnnotation",
	},
	Phenotype: {
		properties: {
			disease: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/OntologyTerm",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Disease",
			},
			ethnicity: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/OntologyTerm",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Ethnicity",
			},
			race: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/OntologyTerm",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Race",
			},
			neuropathology: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/OntologyTerm",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Neuropathology",
				description:
					"pathology or classification of the degree of pathology",
			},
			genotype: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/OntologyTerm",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "APOE Allele or Carrier Status",
			},
			biological_sex: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/OntologyTerm",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Biological Sex",
			},
			study_diagnosis: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/PhenotypeCount",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Study Diagnosis",
				description: "number of cases and controls",
			},
		},
		type: "object",
		title: "Phenotype",
	},
	PhenotypeCount: {
		properties: {
			phenotype: {
				anyOf: [
					{ $ref: "#/components/schemas/OntologyTerm" },
					{ type: "null" },
				],
			},
			num_cases: { type: "integer", title: "Num Cases" },
			num_controls: {
				anyOf: [{ type: "integer" }, { type: "null" }],
				title: "Num Controls",
			},
		},
		type: "object",
		required: ["num_cases"],
		title: "PhenotypeCount",
	},
	PredictedConsequenceSummary: {
		properties: {
			consequence_terms: {
				items: { type: "string" },
				type: "array",
				title: "Predicted Consequence(s)",
			},
			impact: {
				$ref: "#/components/schemas/ConsequenceImpact",
				title: "Impact",
			},
			is_coding: {
				anyOf: [{ type: "boolean" }, { type: "null" }],
				title: "Is Coding?",
				default: false,
			},
			impacted_gene: {
				anyOf: [
					{ $ref: "#/components/schemas/GeneFeature" },
					{ type: "null" },
				],
				title: "Impacted Gene",
			},
			impacted_transcript: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Impacted Transcript",
			},
			codon_change: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Codon Change",
			},
			amino_acid_change: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Amino Acid Change",
			},
		},
		type: "object",
		required: ["consequence_terms", "impact"],
		title: "PredictedConsequenceSummary",
	},
	Provenance: {
		properties: {
			data_source: {
				type: "string",
				title: "Data Source",
				description: "original file data source",
			},
			release_version: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Release Version",
			},
			release_date: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Release Date",
			},
			download_date: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Download Date",
			},
			study: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Study",
			},
			project: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Project",
			},
			accession: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Accession",
			},
			pubmed_id: {
				anyOf: [
					{
						items: {
							type: "string",
							pattern: "^([0-9]{8}|PMID:[0-9]{8})$",
						},
						type: "array",
						uniqueItems: true,
					},
					{ type: "null" },
				],
				title: "Pubmed Id",
			},
			doi: {
				anyOf: [
					{
						items: { type: "string" },
						type: "array",
						uniqueItems: true,
					},
					{ type: "null" },
				],
				title: "Doi",
			},
			consortium: {
				anyOf: [
					{
						items: { type: "string" },
						type: "array",
						uniqueItems: true,
					},
					{ type: "null" },
				],
				title: "Consortium",
			},
			attribution: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Attribution",
			},
			data_source_url: {
				type: "string",
				title: "Data Source Url",
				readOnly: true,
			},
		},
		type: "object",
		required: ["data_source", "data_source_url"],
		title: "Provenance",
	},
	QCStatus: {
		properties: {
			status_code: {
				type: "string",
				title: "QC Status Code",
				description:
					"specific QC status indicator; may vary with ADSP release",
			},
			passed: {
				type: "boolean",
				title: "QC Status",
				description: "flag indicating whether the variant passed QC",
			},
			release: { type: "string", title: "ADSP Release" },
			scores: {
				additionalProperties: true,
				type: "object",
				title: "QC Scores",
				description: "scores and annotations related to the QC testing",
			},
		},
		type: "object",
		required: ["status_code", "passed", "release", "scores"],
		title: "QCStatus",
	},
	QTL: {
		properties: {
			variant: { $ref: "#/components/schemas/Variant" },
			test_allele: { type: "string", title: "Test Allele" },
			track_id: { type: "string", title: "Track" },
			chromosome: {
				$ref: "#/components/schemas/Human",
				title: "Chromosome",
			},
			position: { type: "integer", title: "Position" },
			p_value: {
				anyOf: [{ type: "number" }, { type: "string" }],
				title: "p-Value",
			},
			neg_log10_pvalue: {
				type: "number",
				title: "-log10pValue",
			},
			trait: { type: "string", title: "Trait" },
			z_score: {
				anyOf: [{ type: "number" }, { type: "null" }],
				title: "Z Score",
			},
			dist_to_target: {
				anyOf: [{ type: "number" }, { type: "null" }],
				title: "Dist To Target",
			},
			target: { $ref: "#/components/schemas/GeneFeature" },
			target_ensembl_id: {
				type: "string",
				title: "Target Ensembl Id",
			},
		},
		type: "object",
		required: [
			"variant",
			"test_allele",
			"track_id",
			"chromosome",
			"position",
			"p_value",
			"neg_log10_pvalue",
			"trait",
			"target",
			"target_ensembl_id",
		],
		title: "QTL",
	},
	QTLResponse: {
		properties: {
			data: {
				items: { $ref: "#/components/schemas/QTL" },
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "QTLResponse",
	},
	RV: {
		properties: {
			id: { type: "string", title: "Variant", order: 1 },
			ref_snp_id: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Ref SNP ID",
				order: 1,
			},
			variant_class: {
				type: "string",
				title: "Variant Type",
			},
			location: {
				$ref: "#/components/schemas/GenomicRegion",
			},
			ref: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Ref",
			},
			alt: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Alt",
			},
			most_severe_consequence: {
				anyOf: [
					{
						$ref: "#/components/schemas/PredictedConsequenceSummary",
					},
					{ type: "null" },
				],
				title: "Predicted Consequence",
				description: "most severe consequence predicted by VEP",
			},
		},
		type: "object",
		required: ["id", "variant_class", "location"],
		title: "RV",
	},
	RecordResponse: {
		properties: {
			data: {
				items: { $ref: "#/components/schemas/RowModel" },
				type: "array",
				title: "Data",
				description: "query result",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "RecordResponse",
	},
	RecordSearchResult: {
		properties: {
			id: {
				type: "string",
				title: "Record ID",
				description: "unique record identifier",
			},
			description: { type: "string", title: "Description" },
			display: { type: "string", title: "Display ID" },
			record_type: {
				$ref: "#/components/schemas/Entity",
				title: "Record Type",
			},
			matched_term: {
				type: "string",
				title: "Matched",
				description: "matched term or phrase",
			},
			match_rank: { type: "integer", title: "Match Rank" },
		},
		type: "object",
		required: [
			"id",
			"description",
			"display",
			"record_type",
			"matched_term",
			"match_rank",
		],
		title: "RecordSearchResult",
	},
	RegionAnnotationResponse: {
		properties: {
			data: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/RegionVariant",
						},
						type: "array",
					},
					{
						items: {
							$ref: "#/components/schemas/RegionGene",
						},
						type: "array",
					},
				],
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "RegionAnnotationResponse",
	},
	RegionGene: {
		properties: {
			gene: {
				$ref: "#/components/schemas/GeneFeature",
				title: "Gene",
			},
			gene_type: { type: "string", title: "Gene Type" },
			location: {
				$ref: "#/components/schemas/GenomicRegion",
			},
			range_relation: {
				type: "string",
				title: "Range Relation",
				description:
					"indicates location of gene relative to the queries region",
			},
		},
		type: "object",
		required: ["gene", "gene_type", "location", "range_relation"],
		title: "RegionGene",
	},
	RegionResponse: {
		properties: {
			data: {
				items: {
					$ref: "#/components/schemas/AnnotatedGenomicRegion",
				},
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "RegionResponse",
	},
	RegionVariant: {
		properties: {
			variant: {
				$ref: "#/components/schemas/RV",
				title: "Variant",
			},
			variant_type: {
				type: "string",
				title: "Variant Type",
				description: "structural or smal variant",
			},
			location: {
				$ref: "#/components/schemas/GenomicRegion",
			},
			range_relation: {
				type: "string",
				title: "Range Relation",
				description:
					"indicates location of gene relative to the queries region",
			},
		},
		type: "object",
		required: ["variant", "variant_type", "location", "range_relation"],
		title: "RegionVariant",
	},
	RequestDataModel: {
		properties: {
			request_id: {
				type: "string",
				title: "Request Id",
				description: "unique request identifier",
			},
			endpoint: {
				type: "string",
				title: "Endpoint",
				description: "queried endpoint",
			},
			parameters: {
				additionalProperties: {
					anyOf: [
						{ type: "integer" },
						{ type: "string" },
						{ type: "boolean" },
					],
				},
				type: "object",
				title: "Parameters",
				description:
					"request path and query parameters, includes unspecified defaults",
			},
		},
		type: "object",
		required: ["request_id", "endpoint", "parameters"],
		title: "RequestDataModel",
		description:
			"Captures cleaned user-centric information about the origining request.",
	},
	RowModel: {
		properties: {},
		type: "object",
		title: "RowModel",
		description:
			"The RowModel base class defines class methods\nexpected for these objects to generate standardized API responses\nand adds member functions for generating table responses",
	},
	SearchType: {
		type: "string",
		enum: ["GENE", "VARIANT", "FEATURE", "TRACK", "GLOBAL"],
		title: "SearchType",
	},
	Strand: {
		type: "string",
		enum: ["+", "-"],
		title: "Strand",
	},
	Table: {
		properties: {
			data: {
				items: { $ref: "#/components/schemas/TableRow" },
				type: "array",
				title: "Data",
			},
			columns: {
				items: { $ref: "#/components/schemas/TableColumn" },
				type: "array",
				title: "Columns",
			},
			id: { type: "string", title: "Id" },
			title: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Title",
			},
		},
		type: "object",
		required: ["data", "columns", "id"],
		title: "Table",
	},
	TableCell: {
		properties: {
			value: {
				anyOf: [
					{ type: "string" },
					{ type: "integer" },
					{ type: "number" },
					{ type: "boolean" },
					{ type: "null" },
				],
				title: "Value",
			},
			url: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Url",
			},
			info: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Info",
			},
		},
		type: "object",
		title: "TableCell",
	},
	TableCellType: {
		type: "string",
		enum: ["boolean", "abstract", "float", "integer", "text"],
		title: "TableCellType",
	},
	TableColumn: {
		properties: {
			header: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Header",
			},
			id: { type: "string", title: "Id" },
			description: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Description",
			},
			type: {
				anyOf: [
					{ $ref: "#/components/schemas/TableCellType" },
					{ type: "null" },
				],
				default: "abstract",
			},
		},
		type: "object",
		required: ["id"],
		title: "TableColumn",
	},
	TableRow: {
		properties: {},
		additionalProperties: {
			anyOf: [
				{ $ref: "#/components/schemas/TableCell" },
				{ type: "string" },
				{ type: "integer" },
				{ type: "number" },
				{ type: "boolean" },
				{ type: "null" },
			],
		},
		type: "object",
		title: "TableRow",
	},
	TableViewResponse: {
		properties: {
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description:
					"details about the originating request that generated the response",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination details, if the result is paged",
			},
			table: {
				anyOf: [
					{ $ref: "#/components/schemas/Table" },
					{ additionalProperties: true, type: "object" },
				],
				title: "Table",
			},
		},
		type: "object",
		required: ["request", "pagination", "table"],
		title: "TableViewResponse",
	},
	Track: {
		properties: {
			id: { type: "string", title: "Track" },
			name: { type: "string", title: "Name" },
			description: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Description",
			},
			genome_build: {
				type: "string",
				title: "Genome Build",
			},
			feature_type: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Feature",
			},
			is_download_only: {
				anyOf: [{ type: "boolean" }, { type: "null" }],
				title: "Download Only",
				description:
					"File is available for download only; data cannot be queried using the NIAGADS Open Access API.",
			},
			cohorts: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Cohorts",
			},
			biosample_characteristics: {
				anyOf: [
					{
						$ref: "#/components/schemas/BiosampleCharacteristics",
					},
					{ type: "null" },
				],
			},
			subject_phenotypes: {
				anyOf: [
					{ $ref: "#/components/schemas/Phenotype" },
					{ type: "null" },
				],
			},
			experimental_design: {
				anyOf: [
					{
						$ref: "#/components/schemas/ExperimentalDesign",
					},
					{ type: "null" },
				],
			},
			provenance: {
				anyOf: [
					{ $ref: "#/components/schemas/Provenance" },
					{ type: "null" },
				],
			},
			file_properties: {
				anyOf: [
					{ $ref: "#/components/schemas/FileProperties" },
					{ type: "null" },
				],
			},
		},
		type: "object",
		required: [
			"id",
			"name",
			"genome_build",
			"is_download_only",
			"cohorts",
			"biosample_characteristics",
			"subject_phenotypes",
			"experimental_design",
			"provenance",
			"file_properties",
		],
		title: "Track",
	},
	TrackResponse: {
		properties: {
			data: {
				items: { $ref: "#/components/schemas/Track" },
				type: "array",
				title: "Data",
				description:
					"Full metadata for each track meeting the query criteria.",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "TrackResponse",
	},
	ValidationError: {
		properties: {
			loc: {
				items: {
					anyOf: [{ type: "string" }, { type: "integer" }],
				},
				type: "array",
				title: "Location",
			},
			msg: { type: "string", title: "Message" },
			type: { type: "string", title: "Error Type" },
		},
		type: "object",
		required: ["loc", "msg", "type"],
		title: "ValidationError",
	},
	Variant: {
		properties: {
			id: { type: "string", title: "Variant", order: 1 },
			ref_snp_id: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Ref SNP ID",
				order: 1,
			},
			variant_class: {
				type: "string",
				title: "Variant Type",
			},
			location: {
				$ref: "#/components/schemas/GenomicRegion",
			},
			ref: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Ref",
			},
			alt: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Alt",
			},
		},
		type: "object",
		required: ["id", "variant_class", "location"],
		title: "Variant",
	},
	VariantAnnotationResponse: {
		properties: {
			data: {
				anyOf: [
					{
						items: {
							$ref: "#/components/schemas/ColocatedVariants",
						},
						type: "array",
					},
					{
						items: {
							$ref: "#/components/schemas/VariantFunction",
						},
						type: "array",
					},
					{
						items: {
							$ref: "#/components/schemas/AlleleFrequencies",
						},
						type: "array",
					},
					{
						items: {
							$ref: "#/components/schemas/RowModel",
						},
						type: "array",
					},
				],
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "VariantAnnotationResponse",
	},
	VariantAssociation: {
		properties: {
			variant: {
				$ref: "#/components/schemas/AnnotatedVariantFeature",
				title: "Variant",
				order: 1,
			},
			test_allele: {
				type: "string",
				title: "Test Allele",
				order: 2,
			},
			p_value: {
				anyOf: [{ type: "number" }, { type: "string" }],
				title: "p-Value",
				order: 3,
			},
			trait: {
				$ref: "#/components/schemas/OntologyTerm",
				title: "Trait",
				description: "associated trait",
				order: 4,
			},
			trait_category: {
				type: "string",
				title: "Trait Category",
				description:
					"One of AD, ADRD, Biomarker (for AD/ADRD), or Other",
				order: 5,
			},
			track_id: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Track ID",
				order: 6,
			},
			study: {
				type: "string",
				title: "Study",
				description:
					"NIAGADS Data Track or published study curated from the literature or a GWAS Catalog",
				order: 7,
			},
			pubmed_id: {
				anyOf: [
					{
						items: {
							type: "string",
							pattern: "^([0-9]{8}|PMID:[0-9]{8})$",
						},
						type: "array",
					},
					{ type: "null" },
				],
				title: "Publication",
				order: 8,
			},
			neg_log10_pvalue: {
				type: "number",
				title: "-log10pValue",
			},
		},
		type: "object",
		required: [
			"variant",
			"test_allele",
			"p_value",
			"trait",
			"trait_category",
			"study",
			"neg_log10_pvalue",
		],
		title: "VariantAssociation",
	},
	VariantFunction: {
		properties: {},
		type: "object",
		title: "VariantFunction",
		description: "ranked consequences",
	},
	VariantPValueScore: {
		properties: {
			variant: { $ref: "#/components/schemas/Variant" },
			test_allele: { type: "string", title: "Test Allele" },
			track_id: { type: "string", title: "Track" },
			chromosome: {
				$ref: "#/components/schemas/Human",
				title: "Chromosome",
			},
			position: { type: "integer", title: "Position" },
			p_value: {
				anyOf: [{ type: "number" }, { type: "string" }],
				title: "p-Value",
			},
			neg_log10_pvalue: {
				type: "number",
				title: "-log10pValue",
			},
			trait: { type: "string", title: "Trait" },
		},
		type: "object",
		required: [
			"variant",
			"test_allele",
			"track_id",
			"chromosome",
			"position",
			"p_value",
			"neg_log10_pvalue",
			"trait",
		],
		title: "VariantPValueScore",
	},
	VariantResponse: {
		properties: {
			data: {
				items: {
					$ref: "#/components/schemas/AnnotatedVariant",
				},
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "VariantResponse",
	},
	Assembly: {
		type: "string",
		enum: ["GRCh37", "GRCh38"],
		title: "Assembly",
		description: "enum for genome builds",
	},
	BEDFeature: {
		properties: {
			chrom: {
				type: "string",
				title: "Chromosome",
				description: "name of the chromosome or scaffold",
			},
			chromStart: {
				type: "integer",
				title: "Start",
				description:
					"starting position of the feature in the chromosomse. 0-based",
			},
			chromEnd: {
				type: "integer",
				title: "End",
				description:
					"ending position of the feature; not included in the display",
			},
			name: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Name",
				description: "display label for the feature",
				default: ".",
			},
			score: {
				anyOf: [
					{ type: "string" },
					{ type: "integer" },
					{ type: "number" },
					{ type: "null" },
				],
				title: "Score",
				description: "a score between 0 and 1000",
				default: ".",
			},
			strand: {
				anyOf: [{ type: "string" }, { type: "null" }],
				title: "Strand",
				description: "forward (+) or reverse (-) direction",
				default: ".",
			},
		},
		additionalProperties: true,
		type: "object",
		required: ["chrom", "chromStart", "chromEnd"],
		title: "BEDFeature",
	},
	BEDResponse: {
		properties: {
			data: {
				items: { $ref: "#/components/schemas/BEDFeature" },
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "BEDResponse",
	},
	IGVBrowserTrackConfig: {
		properties: {
			id: { type: "string", title: "Id" },
			name: { type: "string", title: "Name" },
			url: { type: "string", title: "Url" },
			description: { type: "string", title: "Description" },
			infoURL: {
				type: "string",
				title: "Infourl",
				default: "/record",
			},
			format: {
				type: "string",
				title: "Format",
				description: "extract file schema from file format",
				readOnly: true,
			},
			type: {
				type: "string",
				title: "Type",
				description: "extract track type from file schema",
				readOnly: true,
			},
			indexURL: {
				type: "string",
				title: "Indexurl",
				readOnly: true,
			},
			autoscale: {
				type: "boolean",
				title: "Autoscale",
				readOnly: true,
			},
		},
		type: "object",
		required: [
			"id",
			"name",
			"url",
			"description",
			"format",
			"type",
			"indexURL",
			"autoscale",
		],
		title: "IGVBrowserTrackConfig",
	},
	ListResponse: {
		properties: {
			data: {
				items: {
					anyOf: [
						{ type: "string" },
						{ type: "integer" },
						{ type: "number" },
					],
				},
				type: "array",
				title: "Data",
			},
			request: {
				$ref: "#/components/schemas/RequestDataModel",
				description: "details about the originating request",
			},
			pagination: {
				anyOf: [
					{
						$ref: "#/components/schemas/PaginationDataModel",
					},
					{ type: "null" },
				],
				description: "pagination status, if the result is paged",
			},
			message: {
				anyOf: [
					{ items: { type: "string" }, type: "array" },
					{ type: "null" },
				],
				title: "Message",
				description:
					"warning or info message(s) qualifying the response",
			},
		},
		type: "object",
		required: ["data", "request"],
		title: "ListResponse",
	},
};
