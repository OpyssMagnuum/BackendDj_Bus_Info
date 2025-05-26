from django.db.models import Q
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


def route_presort(request):
    if request.method == 'POST':
        stop1 = request.POST.get('stop1', '').strip()
        stop2 = request.POST.get('stop2', '').strip()
        if stop1 and stop2:
            return redirect('results', stop1=stop1, stop2=stop2)
    return render(request, 'main/presort.html')


def route_postsort(request, stop1: str, stop2: str):
    # Находим маршруты, содержащие stop1
    routes_with_stop1 = Route.objects.filter(
        Q(long_route__bus_stop_name__icontains=stop1) |
        Q(long_route_reverse__bus_stop_name__icontains=stop1)
    ).distinct()

    # Находим маршруты, содержащие stop2
    routes_with_stop2 = Route.objects.filter(
        Q(long_route__bus_stop_name__icontains=stop2) |
        Q(long_route_reverse__bus_stop_name__icontains=stop2)
    ).distinct()

    # Пересечение - маршруты, содержащие обе остановки
    routes_with_both_stops = routes_with_stop1.intersection(routes_with_stop2)

    print("Найдено маршрутов:", routes_with_both_stops.count())

    processed_routes = []

    for route in routes_with_both_stops:
        # Получаем все остановки для маршрута (прямого направления)
        stops_forward = list(route.long_route.all().order_by('bs_num'))

        # Получаем все остановки для маршрута (обратного направления)
        stops_backward = list(route.long_route_reverse.all().order_by('bs_num'))

        # Проверяем оба направления
        for direction, stops in [('forward', stops_forward), ('backward', stops_backward)]:
            # Находим индексы наших остановок
            stop1_ids = [i for i, stop in enumerate(stops) if stop1.lower() in stop.bus_stop_name.lower()]
            stop2_ids = [i for i, stop in enumerate(stops) if stop2.lower() in stop.bus_stop_name.lower()]

            # Проверяем все возможные комбинации
            for i in stop1_ids:
                for j in stop2_ids:
                    if i < j:  # Только если stop1 идет перед stop2
                        segment = stops[i:j + 1]
                        processed_routes.append({
                            'bus_num': route.bus_num,
                            'short_route_name': route.short_route_name,
                            'stops': segment,
                            'stops_count': len(segment) - 1,
                            'direction': direction
                        })

    # Сортируем маршруты по количеству остановок
    processed_routes.sort(key=lambda x: x['stops_count'])

    context = {
        'stop1': stop1,
        'stop2': stop2,
        'routes': processed_routes,
    }

    return render(request, 'main/postsort.html', context)