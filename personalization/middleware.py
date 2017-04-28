from . import views
from views import DiscussionViewStore as ViewStore


class StoreView(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.session['ip-addr'] != 'None':
            if self.request.user.is_authenticated():
                if self.request.user.pk in ViewStore.ViewIndex:
                    pass
                else:
                    ViewStore.ViewIndex.update({self.request.user.pk: []})
