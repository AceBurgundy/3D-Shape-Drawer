def get_instance_properties(class_reference):
    """
    Maps a class intance properties, and setters

    Arguments:
        class_reference (Class): An instance of a class

    Returns:
        A dictionary which contains the name of the field, its getter, setter, data type references.
    """
    class_data = {}

    for field_name in dir(class_reference):

        field = getattr(class_reference, field_name)

        if not isinstance(field, property):
            continue

        getter_method = getattr(class_reference, field_name).fget

        class_data[field_name] = {
            "getter": getter_method,
            "setter": getattr(class_reference, field_name).fset
        }

    return class_data

