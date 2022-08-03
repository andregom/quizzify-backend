def format_graphy(name):
    graphy = extract_element_from(name, '.')
    return ' '.join(w.capitalize() for w in graphy.split('_'))


def extract_element_from(collection, separator = None, index=0):
    if collection:
        if separator is None:
            return collection[index]
            
        return collection.split(separator)[index]
       

    return collection
