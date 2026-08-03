def decide(*args, **kwargs):
    return {"decision": "allowed", "args": args, "kwargs": kwargs}


def account(*args, **kwargs):
    return {"accounted": True, "args": args, "kwargs": kwargs}


def should_accept_ability(*args, **kwargs):
    return True
