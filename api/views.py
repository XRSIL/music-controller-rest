from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from datetime import datetime


# Create your views here.

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serialiazer = self.serializer_class(data=request.data)

        if serialiazer.is_valid():
            guest_can_pause = serialiazer.data.get('guest_can_pause')
            votes_to_skip = serialiazer.data.get('votes_to_skip')
            host = self.request.session.session_key

            queryset = Room.objects.filter(host=host)

            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.updated_at = datetime.now()
                room.save(update_fields=['guest_can_pause', 'votes_to_skip', 'updated_at']),

            else:
                room = Room(host=host, votes_to_skip=votes_to_skip, guest_can_pause=guest_can_pause)
                room.save()

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

