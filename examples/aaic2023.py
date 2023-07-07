import requests
import json
from urllib.parse import urlencode

REQUEST_URI = "https://api.niagads.org/alpha"

def pretty_print(obj):
    ''' pretty print a dict obj'''
    if isinstance(obj, dict):
        print(json.dumps(obj, sort_keys=True, indent=4))
    else:
        print(obj)
    
    
def make_request(endpoint, params):
    ''' wrapper to build and make a request '''
    requestUrl = REQUEST_URI + "/" + endpoint 
    if params is not None:
        requestUrl += '?' + urlencode(params)

    try:
        response = requests.get(requestUrl)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("HTTP Error: " + err.args[0])

    return response.json()

# let's find an interesting variant by getting the top result from the 
# lifted over Kunkle et al. 2019 IGAP Rare Variants dataset
# https://api.niagads.org/<version>/genomics/track/<trackId>/hits
trackId = 'NG00075_GRCh38_STAGE1'
hits = make_request("genomics/track/" + trackId + "/hits", None)

# the results are sorted, so the top hit will be the first one
# let's get it's dbSNP refSNP ID
topVariant = hits[0]['ref_snp_id']

# let's learn a bit more about this variant
# can look up a variant by its refSNP ID or 
# chr:pos:ref:alt (position & allelic identifier)
# https://api.niagads.org/<version>/genomics/variant/<variantId>

# this API call will return basic variant info 
# and the most severe predicted consequence, if any
# to get the full variant annotation, add the `full` 
# flag to the request parameters
# e.g., pass {"full": True} for the parameter argument, instead of None
variantInfo = make_request("genomics/variant/" + topVariant, None)

# let's find out if there is an potentially impacted gene
# by extracting it from the most severe predicted consequence, 
# which is returned in the variant 'annotation' object
geneId = variantInfo['annotation']['most_severe_consequence']['gene_id']

# let's learn more about this gene
# can look up a gene by its Ensembl ID, NCBI Gene (Entrez) ID, 
# https://api.niagads.org/<version>/genomics/gene/<geneId>
# or official gene symbol (case sensitive, exact match)
geneInfo = make_request("genomics/gene/" + geneId, None )

# Next, we can query the NIAGADS FILER (functional genomics) 
# repository to find out  if there are any regulatory elements 
# that overlap this gene that could potentially be impacted

# this could involve a lot of work, 
# so let's narrow  our search down a bit

# let's look for something AD-relevant
# featureType = histone modifications
# project = ENCODE's Rush AD
# tissue = brain

params = { "featureType": "histone modification",
           "project": "Rush AD",
           "tissue": "brain"}

# First, let's find out how many tracks meet this criteria 
# by using the `countOnly` flag

# without `countOnly`, this query will return a list of objects
# describing the metadata (name, id, access urls, experimental design,
# provenance, and biosample characteristics) for each track that
# matches the search criteria

# http://api.niagads.org/<version>/filer/track/featureType=histone%20modification&project=rush%20ad&tissue=brain&countOnly=true

params.update({"countOnly": True})
response = make_request("filer/track", params)
numTracks = response['num_matched_tracks']

# BTW numTracks is 194.  That's pretty reasonable,
# so let's look for overlaps w/our gene of interest
# http://api.niagads.org/<version>/filer/track/overlaps?featureType=histone%20modification&project=rush%20ad&tissue=brain&span=<chrN:start-end>
del params['countOnly'] # remove countOnly
params.update({ # add in the span of interest from the geneInfo
        "chr": geneInfo['chromosome'],
        "start": geneInfo["start"],
        "end": geneInfo["end"]
        })
overlaps = make_request("filer/track/overlaps", params)

# let's find an interesting track -- the first that has
# >1 featuring within our region of interest
targetTrack = None
for track in overlaps:
    if len(track['features']) > 1:
        targetTrack = track
        break

# and finally, let's get some more information about the track
# to learn what histone modification, in which biosample 
# there there is overlap between our target gene locus and
# our regulatory features
# http://api.niagads.org/<version>/filer/track/<trackId>
targetTrackInfo = make_request("filer/track/" + targetTrack['Identifier'], None)

# uncomment any of the following to print out the responses
# we received or extracted elements that were more closely examined
# pretty_print(hits)
# pretty_print(hits[0])
# pretty_print(variantInfo)
# pretty_print(variantInfo['annotation']['most_severe_consequence'])
# pretty_print(geneInfo)
# pretty_print(overlaps)
# pretty_print(targetTrack)
pretty_print(targetTrackInfo)
