from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
import logging

logger = logging.getLogger('shoapapp')

library_request = {}


class RequestFrequencyControl:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_now = datetime.now()
        IP_USER = request.META.get('REMOTE_ADDR', None)
        logger.info(f'ip {IP_USER}')
        if IP_USER in library_request:
            logger.info(f'old {library_request[IP_USER]}')
            logger.info(f'now {time_now}')
            old_time_visit = library_request[IP_USER]
            difference = time_now - old_time_visit
            logger.info(f'difference {difference.total_seconds()}')
            if difference.total_seconds() < 5:
                return HttpResponse(render(request, 'shopapp/time-limit.html', {'seconds': 5 - difference.total_seconds()}))
        library_request[IP_USER] = time_now
        response = self.get_response(request)
        return response




