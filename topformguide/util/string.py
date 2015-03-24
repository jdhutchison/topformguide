from topformguide.util import constants

def slugToConstant(slug):
    """
    Turns part of a URL slug into a standard constant (or constant name), e.g. cab-chassis becomes CAB_CHASSIS
    :param slug: [string] The url slug part to transform. Required.
    :return: The constant/enum from the slug, or None if None is passed in.
    """
    if slug is None:
        return None
    elif slug == 'suv':
        return constants.SUV

    return slug.replace('-', '_').upper()


def constantToSlug(constant):
    """

    :param constant:
    :return:
    """
    if constant is None:
        return None

    return constant.replace('_', '-').lower()


def constantToHuman(constant):
    if constant is None:
        return None
    elif constant == constants.SUV:
        return constants.SUV

    return constant.replace('_', ' ').title()

def deslugify(slug):
    if slug is None:
        return None
    elif slug == 'suv':
        return constants.SUV

    return slug.replace('-', ' ').title()