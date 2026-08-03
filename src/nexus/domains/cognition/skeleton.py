DOMAIN_NAME = "cognition"
DOMAIN_TAG = "interpretive"


def get_domain_manifest():
    return {
        "name": DOMAIN_NAME,
        "tag": DOMAIN_TAG,
        "principles": ["perception", "memory", "reasoning", "attention", "learning"],
        "status": "skeleton",
    }
