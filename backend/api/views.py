from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    return Response({
        "status": "ok",
        "day": 1,
        "project": "GraphGuard",
        "message": "Day 1 complete — Django is running!"
    })
