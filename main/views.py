from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage

from .models import Crime
from .forms import DateForm


def paginate(request, objects_list, default_limit=20, pages_count=3):
    """ Функция пагинации """
    try:
        limit = int(request.GET.get('limit', default_limit))
    except ValueError:
        limit = default_limit
    if limit > 100:
        limit = default_limit
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise 404

    paginator = Paginator(objects_list, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    if not pages_count:
        page_range = paginator.page_range
    else:
        start = page.number - pages_count
        if start < 0:
            start = 0
        page_range = paginator.page_range[start: page.number + int(pages_count / 2)]
    return page, page_range


def index(request):
    form = DateForm()
    if request.method != "POST":
        if 'filter-report-date' in request.session:
            request.POST = request.session['filter-report-date']
            request.method = 'POST'
    if request.method == "POST":
        form = DateForm(request.POST)
        request.session['filter-report-date'] = request.POST

    if form.is_valid():
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        data = Crime.objects.filter(date__report_date__range=(date_from, date_to))
    else:
        data = Crime.objects.last_data()
    page, page_range = paginate(request, data)

    context = {
        'data': page.object_list,
        'page': page,
        'page_range': page_range,
        'form': form,
    }
    return render(request, 'main/index.html', context)
