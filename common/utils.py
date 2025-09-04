def set_dict_attr(obj, data):
    """ Позволяет обновлять атрибуты объекта динамически, используя данные из словаря """
    for attr, value in data.items():
        setattr(obj, attr, value)
    return obj
