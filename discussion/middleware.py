from ipware.ip import get_ip
from . import views, models




# ipstore = IPDataStore()
"""
class GetIP(object):

	def process_view(self, request, view_func, view_args, view_kwargs):
		ip = get_ip(request)
		if ip:
			request.session['ip-addr'] = ip
			request.session['no-ip'] = False
			try:
				dataStore=models.IpDataStore.objects.get(ipAddr=ip)
			except models.IpDataStore.DoesNotExist:
				dataStore=models.IpDataStore.objects.create(ipAddr=ip)
				dataStore.save()
			print ip
		else:
			request.session['ip-addr'] = 'None'
			request.session['no-ip'] = True
"""


class GetAndStoreIP(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        ip = get_ip(request)
        if ip:
            request.session['ip-addr'] = ip
            request.session['no-ip'] = False

            if ip in views.IPDataStore.IpDataStore:
                pass
            else:
                views.IPDataStore.IpDataStore.update({ip: {'views': []}})
            # request.session['dataStore'] = IPDataStore
            print ip
            print 'dataStore -> %s' % views.IPDataStore.IpDataStore
        else:
            request.session['ip-addr'] = 'None'
            request.session['no-ip'] = True

# def getIpStoreInstance():
#	return ipstore
