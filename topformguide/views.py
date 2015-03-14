from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from topformguide import models
from topformguide.util import constants
from topformguide.util import calculations


def index(request):
    return render(request, 'index.html', None)


def bodylist(request):
    return render(request, 'bodytypes.html')


def displayCar(request, variantId):
    car = get_object_or_404(models.Variant, pk=int(variantId))
    # fuelEconomies = sorted(car.fuelEcomonySet, cmp=compareFuelData)
    fuelData = []
    for econ in sorted(car.fuelEconomySet.all(), cmp=compareFuelData):
        emissionData = calculations.findRating(car.emissionDataSet.all(), econ.type)
        fuelData.append({'econ': econ, 'emissions': emissionData})

    return render(request, 'variant.html', {'car': car, 'fuelData': fuelData})


def compareFuelData(econ1, econ2):
    # Sort by economy type
    orderFor1 = constants.ECON_TYPE_SORT_MAP[econ1.type]
    orderFor2 = constants.ECON_TYPE_SORT_MAP[econ2.type]
    if orderFor1 != orderFor2:
        return orderFor1 - orderFor2

    # Sort by unit
    orderFor1 = constants.FUEL_ECON_UNIT_SORT_ORDER[econ1.unit]
    orderFor2 = constants.FUEL_ECON_UNIT_SORT_ORDER[econ2.unit]
    return orderFor1 - orderFor2