#Built this to improve readability when going through guard clauses
def validate_dict(dictionary, keys):
    if type(dictionary) is not dict:
        check = False
    else:
        dict_keys = dictionary.keys()
        check = True
        for key in keys:
            if key not in dict_keys or dictionary[key] == "":
                check = False
                continue
    return check