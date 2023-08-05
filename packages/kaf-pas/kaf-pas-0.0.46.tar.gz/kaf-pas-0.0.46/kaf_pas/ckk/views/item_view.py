from django.db import transaction

from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.ckk.models.combineItems import CombineItems
from kaf_pas.ckk.models.copyItems import CopyItems
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_operations_view import Item_operations_view, Item_operations_viewManager
from kaf_pas.ckk.models.item_view import Item_view, Item_viewManager


def Item_view_query():
    query = Item_view.objects.filter()
    return query


@JsonResponseWithException()
def Item_view_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_view_query().
                get_range_rows1(
                request=request,
                function=Item_viewManager.getRecord,
                distinct_field_names=('id',)
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Fetch1(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_operations_view.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Item_operations_viewManager.getRecord,
                distinct_field_names=('id',)
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Add(request):
    return JsonResponse(DSResponseAdd(data=Item.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item_view_query().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_view_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Item_view.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException(printing=False)
def copyItems(request):
    return JsonResponse(CopyItems(request).response)


@JsonResponseWithException(printing=False)
def combineItems(request):
    return JsonResponse(CombineItems(request).response)


@JsonResponseWithException()
def Item_view_CopyBlockItems(request):
    _request = DSRequest(request=request)
    source = _request.json.get('source')
    destination = _request.json.get('destination')
    items_ids = []

    if isinstance(source, dict) and isinstance(destination, dict):
        srecords = source.get('records')
        drecord = destination.get('record')

        if isinstance(srecords, list) and isinstance(drecord, dict):

            with transaction.atomic():
                for srecord in srecords:
                    item = Item_viewManager.copy_item(item=Item.objects.get(id=srecord.get('id')), parent_item=Item.objects.get(id=drecord.get('id')))
                    items_ids.append(item.id)

    return JsonResponse(DSResponse(request=request, data=items_ids, status=RPCResponseConstant.statusSuccess).response)
