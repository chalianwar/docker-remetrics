
import os, json, multiprocessing#,logging

# image_maper_absfilename = ""

# {
#     "config": [],
#     "layers": [
#         "sha256:39e3ef1368026b03219bd17f8364cbeb5807035dafe525e18731fe0f44878e67",
#         "sha256:ba5423b29e1c4493bfd7c06c2e719aec23079b9a97bca294e994482074611b51",
#         "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4",
#         "sha256:6d8bc379e6268baffcf3cddba6bc11e837370ddb8c0ea14b2657ac7d1615e36a",
#         "sha256:090576221c8553def76ebdc661146d044603e64a95793a3cd4aa3102472e33a1",
#         "sha256:35e043cea961b32b15d4d68d70d79332d2fa839b1b3654cdc928859000922826"
#     ],
#     "manifest": "cheesygoat-pluralsight-docker-ci-latest",
#     "version": "schema1"
# },

bad_layer_digest_absfilename = ""

bad_layer_digests = []

# image_mappers = []

with open(bad_layer_digest_absfilename, 'r') as f:
    for line in f:
        bad_layer_digests.append(line.replace("\n", ""))

num_images = 0

with open(os.path.join(dest_dir[0]['job_list_dir'], 'imagename_mapper_digests.json'), 'r') as f:
    _image_mappers = json.load(f)

    logging.debug("load image_mapper: %s", os.path.join(dest_dir[0]['job_list_dir'], 'imagename_mapper_digests.json'))

    for _image_mapper in _image_mappers:

        layers = _image_mapper['layers']
        manifest_name = _image_mapper['manifest']

        for digest in bad_layer_digests:
            if digest in layers:
                num_images = num_images + 1
                print manifest_name


print "the number of images related to the layers",num_images