from django.contrib import  auth as django_auth
from django.http import  JsonResponse
from sign.models import Event
from django.core.exceptions import  ValidationError
import  hashlib, base64, time

def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', 'b')
    auth = get_http_auth.split()

    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
    except IndexError:
        return "null"

    userid, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=userid, password=password)
    if user is not None and user.is_active:
        django_auth.login(request, user)
        return 'success'
    else:
        return "fail"

def user_sign(request):
    if request.method == 'POST':
        client_time = request.POST.get('time', '')
        client_sign = request.POST.get('sign','')
    else:
        return 'error'

    if client_time == '' or client_sign =='':
        return 'sign null'

    now_time = time.time()
    server_time = str(now_time).split('.')[0]

    time_difference = int(server_time) - int(client_time)
    if time_difference >= 60:
        return "time.out"

    #sign check
    md5 = hashlib.md5()
    sign_str = client_time + "&Guest-Bugmaster"
    sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()
    if server_sign != client_sign:
        return "sign error"
    else:
        return "sign right"

def sec_add_event(request):
    auth_result = user_auth(request)
    if auth_result == "null":
        return  JsonResponse({'status': 10011, 'message': 'user auth null'})

    if auth_result == "fail":
        return JsonResponse({'status': 10012, 'message':'user auth fail'})

    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': 'error'})
    return JsonResponse({'status': 200, 'message': 'add event success'})

def md5_add_event(request):
    sign_result = user_sign(request)
    if sign_result == 'sign null':
        return JsonResponse({'status': 10011, 'message': 'user sign null'})
    elif sign_result == 'time.out':
        return JsonResponse({'status': 10012, 'message': 'user sign time out'})
    elif sign_result == 'sign error':
        return JsonResponse({'status': 10013, 'message': 'user sign error'})

    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': 'error'})
    return JsonResponse({'status': 200, 'message': 'add event success'})