DOMAIN_NAME = "physics"
DOMAIN_TAG = "foundation"


def get_domain_manifest():
    return {
        "name": DOMAIN_NAME,
        "tag": DOMAIN_TAG,
        "principles": ["matter", "energy", "force", "motion", "information"],
        "status": "skeleton",
    }
