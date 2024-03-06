def get_instance_properties(class_reference):
    class_data = {}
    instance = class_reference()

    for field_name in dir(class_reference):
        field = getattr(class_reference, field_name)

        if not isinstance(field, property):
            continue

        getter_method = getattr(class_reference, field_name).fget
        class_data[field_name] = {
                "getter": getter_method,
                "setter": getattr(class_reference, field_name).fset,
                "type": type(getter_method(instance))
        }

    return class_data

