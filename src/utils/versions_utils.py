def version_tuple(version):
    return tuple(map(int, version.split(".")))


def separate_name_from_version(package):
    if "@" in package:
        name, version = package.split("@", 1)
        return name, version

    return package, False


def compare_versions_symbols(need_version, attempt_version2):
    operators = [">=", "<=", "=", ">", "<"]

    operator = "="

    for op in operators:
        if need_version.startswith(op):
            operator = op
            need_version = need_version[len(op):]
            break

    v1_tuple = version_tuple(need_version)
    v2_tuple = version_tuple(attempt_version2)

    if operator == ">=":
        return v2_tuple >= v1_tuple
    elif operator == "<=":
        return v2_tuple <= v1_tuple
    elif operator == "=":
        return v2_tuple == v1_tuple
    elif operator == ">":
        return v2_tuple > v1_tuple
    elif operator == "<":
        return v2_tuple < v1_tuple

    return False
