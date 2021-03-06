from pyramid.view import view_config
from pyramid.response import Response
from adhocracy.core.models.adhocracyroot import IAdhocracyRootMarker


class AdhocracyRootView(object):

    def __init__(self, context, request):
            self.context = context
            self.request = request

    #default view
    @view_config(context=IAdhocracyRootMarker,
                 renderer='adhocracyroot_templates/view.pt')
    def __call__(self):
        return {'project': 'adhocracy.core'}

    #different view with name @@secondview
    @view_config(context=IAdhocracyRootMarker,
                 name="secondview",)
    def secondview(self):
        return Response('OK')
