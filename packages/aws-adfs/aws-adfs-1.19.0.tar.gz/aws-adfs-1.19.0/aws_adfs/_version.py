
# This file was generated by 'versioneer.py' (0.18) from
# revision-control system data, or from the parent directory name of an
# unpacked source archive. Distribution tarballs contain a pre-generated copy
# of this file.

import json

version_json = '''
{
 "date": "2019-10-15T08:31:12+0200",
 "dirty": false,
 "error": null,
 "full-revisionid": "8a29917204c25b9199e45f0b73b386960161be81",
 "version": "1.19.0"
}
'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)
