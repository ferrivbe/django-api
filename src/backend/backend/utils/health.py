from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    """
    The health view.
    """

    def __init__(self):
        """
        Creates a new instance of HealthView.
        """
        self.renderer_classes = [JSONRenderer]
        self.permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Gets API health.",
    )
    def get(self, request):
        """
        Gets the API health.
        """
        return Response({"health": "API healthy"}, status=status.HTTP_200_OK)
