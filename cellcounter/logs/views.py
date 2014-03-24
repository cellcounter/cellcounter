import json
import datetime

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.admin.views.decorators import staff_member_required

from cellcounter.logs.models import AccessRequest


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object


@staff_member_required
def index(request):
    template = loader.get_template('logs/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


@staff_member_required
def host_access(request):

    all = AccessRequest.objects.values()

    hosts = dict()
    for r in all:
        try:
            hosts[r["remote_addr"]].append(r)
        except KeyError:
            hosts[r["remote_addr"]] = [r]
            #hosts[r.remote_addr].push(r)

    hosts_data = dict()
    hosts_data["unique"] = len(hosts)
    hosts_data["hosts"] = hosts

    #hosts = [r.remote_addr for r in all]
    #unique_hosts = OrderedDict.fromkeys(hosts).keys()
    unique_hosts = hosts.keys()


    latest_access_list = AccessRequest.objects.order_by('-time_local')[:10]

    return HttpResponse(json.dumps(hosts_data, cls=DateTimeEncoder),
                        mimetype="application/json" )


@staff_member_required
def page_access(request):

    all = AccessRequest.objects.values()

    pages = dict()
    for r in all:
        try:
            pages[r["request_path"]].append(r)
        except KeyError:
            pages[r["request_path"]] = [r]

    pages_data = dict()
    pages_data["unique"] = len(pages)
    pages_data["pages"] = pages

    return HttpResponse(json.dumps(pages_data, cls=DateTimeEncoder),
                        mimetype="application/json" )


@staff_member_required
def referrer_access(request):

    all = AccessRequest.objects.values()

    referrers = dict()
    for r in all:
        referrer = r["http_referrer"]
        if referrer == "":
            referrer = "<direct>"
        try:
            referrers[referrer].append(r)
        except KeyError:
            referrers[referrer] = [r]

    referrers_data = dict()
    referrers_data["unique"] = len(referrers)
    referrers_data["referrers"] = referrers

    return HttpResponse(json.dumps(referrers_data, cls=DateTimeEncoder),
                        mimetype="application/json" )


@staff_member_required
def date_access(request):

    all = AccessRequest.objects.values()

    dates = dict()
    for r in all:
        date = r["time_local"].timetuple()[0:3]
        year = date[0]
        month = date[1]
        day = date[2]
        if dates.get(year)==None:
            dates[year] = dict()
        if dates[year].get(month)==None:
            dates[year][month] = dict()
        try:
            dates[year][month][day].append(r)
        except KeyError:
            dates[year][month][day] = [r]

    dates_data = dict()
    dates_data["unique"] = len(dates)
    dates_data["dates"] = dates

    return HttpResponse(json.dumps(dates_data, cls=DateTimeEncoder),
                        mimetype="application/json" )

