def pick_fields(node, fields):
    return {k: v for k, v in dict(node).items() if k in fields}
