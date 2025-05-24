from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import redirect

from buses.serializers import BusSerializer, RouteSerializer, LongRouteNamesSerializer
from main.models import Bus, Route, LongRouteName


# Create your views here.
class BusViewSet(ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class LRNViewSet(ModelViewSet):
    queryset = LongRouteName.objects.all()
    serializer_class = LongRouteNamesSerializer


def route_stops_form(request, route_number, stop_count, reverse):
    context = {
        'route_number': route_number,
        'stop_count_range': range(1, stop_count + 1),
        'reverse': reverse,
    }
    return render(request, 'main/add_ostanovka.html', context)


def save_route_stops(request):
    if request.method != 'POST':
        return HttpResponse("Not OK: Only POST method allowed", status=405)  # 405 Method Not Allowed
    try:
        route_name = request.POST.get('route_name')
        reverse = request.POST.get('reverse')
        stop_count = len([key for key in request.POST if key.startswith('stop_name_')])

        for i in range(1, stop_count + 1):
            stop_name = request.POST.get(f'stop_name_{i}')

            LongRouteName.objects.create(
                route_name=route_name,
                bus_stop_name=stop_name,
                bs_num=i,
                bs_num_reverse=reverse
            )

        return HttpResponse('OK: Stops saved successfully', status=200)

    except Exception as e:
        return HttpResponse(f"Not OK: Error - {str(e)}", status=500)  # 500 Internal Server Error


def route_detail(request, route_id):
    route = get_object_or_404(Route, bus_num=route_id)
    context = {
        'route': route,
    }
    return render(request, 'main/ostanovkas.html', context)
