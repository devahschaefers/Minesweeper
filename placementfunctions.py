def topLeft(orginal_location, textRect):
    return (orginal_location)


def topRight(orginal_location, textRect):
    return (orginal_location[0] - textRect.width, orginal_location[1])


def bottomLeft(orginal_location, textRect):
    return (orginal_location[0], orginal_location[1] - textRect.height)


def bottomRight(orginal_location, textRect):
    return (orginal_location[0] - textRect.width,
            orginal_location[1] - textRect.height)


def center(orginal_location, textRect):
    return (orginal_location[0] - textRect.width // 2, orginal_location[1] - textRect.height // 2)
