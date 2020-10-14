# encoding: utf-8
# Date: 2019-07-15 17:12

__author__ = 'ryan.liu'

from rest_framework import viewsets
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


class BasicViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = False
        instance.save()
        return Response(dict(id=instance.id))
