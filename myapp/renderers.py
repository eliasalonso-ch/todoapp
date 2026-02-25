from rest_framework.renderers import JSONRenderer
import json

from rest_framework.renderers import JSONRenderer
import json

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')
        
        # if status code is 2xx it's a success
        success = response.status_code < 400
        
        wrapped = {
            'success': success,
            'message': None,
            'data': data
        }
        
        return super().render(wrapped, accepted_media_type, renderer_context)