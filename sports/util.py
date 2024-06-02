def validate_dict(dictionary, keys):
    dict_keys = dictionary.keys()
    check = True
    for key in keys:
        if key not in dict_keys or dictionary[key] == "":
            check = False
            continue
    return check