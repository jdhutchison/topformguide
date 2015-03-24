from django.shortcuts import render
from django.shortcuts import get_object_or_404

from topformguide import models
from topformguide.repository import make
from topformguide.repository import model
from topformguide.util import constants
from topformguide.util import string
from topformguide.util import numbers
from topformguide.util.model import findRating

makeRepository = make.MakeRepository()
modelRepository = model.ModelRepository()

def index(request):
    return render(request, 'index.html', None)


def bodylist(request):
    return render(request, 'bodytypes.html',
                  {'path': '/body', 'headingPrefix': 'View', 'instructionInsert': 'a manufacturer\'s cars'})


def displayCar(request, variantId):
    car = get_object_or_404(models.Variant, pk=int(variantId))
    # fuelEconomies = sorted(car.fuelEcomonySet, cmp=compareFuelData)
    fuelData = []
    for econ in sorted(car.fuelEconomySet.all(), cmp=compareFuelData):
        emissionData = findRating(car.emissionDataSet.all(), econ.type)
        fuelData.append({'econ': econ, 'emissions': emissionData})

    return render(request, 'variant.html', {'car': car, 'fuelData': fuelData})


def topBodyTypes(request):
    return render(request, 'bodytypes.html',
                  {'path': '/top/bodytype', 'headingPrefix': 'Top 20', 'instructionInsert': 'the top 20 rated cars'})


def topFuelTypes(request):
    return render(request, 'fueltypes.html')


def showMakes(request, type=None, filter=None):
    path = '/cars'
    title = 'View Cars by Make'
    text = 'Select a Make to see all the Models for that Make'
    if type == 'rating':
        path = '/top/make'
        title = 'View Top 20 Vehicles by Make'
        text = 'Select a Make to see the Top 20 rating vehicles for that make'
    elif type == 'body':
        path = '/body/' + filter
        title = 'View ' + string.deslugify(filter) + 's for a Make'
        text = 'Select a Make to see all the ' + string.deslugify(filter) + 's they produce'

    makes = makeRepository.findNamesMakesWithRatedCars(filter)
    makeLists = splitIntoLists(makes, 3)
    return render(request, 'makelist.html', {'lists': makeLists, 'path': path, 'title': title, 'text': text})


def showModelsForMake(request, make):
    allModels = modelRepository.findModelNamesWithCarsWithRatingsByMake(string.deslugify(make))
    lists = splitIntoLists(allModels, 3)
    return render(request, 'modelsformake.html',
                  {'lists': lists, 'path': '/cars/' + make, 'make': string.deslugify(make)})


def showVariantsForBodyTypeAndMake(request, bodyType, make):
    properMake = string.deslugify(make)
    bodyEnum = string.slugToConstant(bodyType)
    variants = getVariants(make=properMake, body=bodyEnum)
    return render(request, 'bodyandmake.html',
                  {'make': properMake, 'body': bodyEnum, 'variants': variants})



def getTopVariantsForType(request, listType, type, number=20):
    filterValue = string.slugToConstant(type)
    friendly = string.deslugify(type)
    querySet = models.Variant.objects.filter(eGoRating__isnull=False)
    if listType == 'body':
        querySet = querySet.filter(body=filterValue)
    elif listType == 'fuel':
        querySet = querySet.filter(fuelType=filterValue)
        friendly = friendly + ' powered car'
    elif listType == 'make':
        querySet = querySet.filter(model__make__name__iexact=filterValue)

    variants = querySet.order_by('-eGoRating')[:number].all()
    return render(request, 'topcarlist.html', {'friendly': friendly, 'variants': variants})


def variantsForMakeAndModel(request, make, model, year=None):
    makeEnum = string.deslugify(make)
    modelEnum = string.deslugify(model)
    if year is not None:
        year = numbers.toInt(year)

    variants = getVariants(make=makeEnum, model=modelEnum, year=year).all()
    return render(request, 'makeandmodel.html', {'make': makeEnum, 'model': modelEnum, 'variants': variants})


# SEARCH VIEWS
def search(request):
    makes = makeRepository.findNamesMakesWithRatedCars(None)
    return render(request, 'searchform.html', {'makes': makes, 'bodyTypes': constants.ALL_BODY_TYPES})


def searchresults(request):
    year = numbers.toInt(request.POST.get('year'))
    make = request.POST.get('make')
    if not make:
        make = None
    body = request.POST.get('body')
    if not body:
        body = None
    variants = getVariants(make, None, year, body, request.POST.get('engine'), request.POST.get('fuel'))
    return render(request, 'searchresults.html', {'variants': variants.all()})

# DATABASE QUERIES
# def getModelsByMake(make):
#    return models.CarModel.objects.filter(make__name__iexact=make).order_by('name', 'year').all()


# def getModelNamesByMake(make):
#    return models.CarModel.objects.filter(make__name__iexact=make) \
#        .values_list('name', flat=True).distinct().all()


def getVariants(make=None, model=None, year=None, body=None, engine=None, fuel=None):
    query = models.Variant.objects.filter(eGoRating__isnull=False)

    if make is not None:
        query = query.filter(model__make__name__iexact=make)

    if model is not None:
        query = query.filter(model__name__iexact=model)

    if year is not None:
        query = query.filter(model__year=year)

    if body is not None:
        query = query.filter(body=body)

    if engine is not None:
        query = query.filter(engineType=engine)

    if fuel is not None:
        query = query.filter(fuelType=fuel)

    return query.order_by('model__year', 'model__make__name', 'model__name', 'name', '-eGoRating')

def splitIntoLists(simpleList, howMany):
    lists = []
    for i in range(0, howMany):
        lists.append([])

    for i in range(0, len(simpleList)):
        lists[i % howMany].append(simpleList[i])

    return lists

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