from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from .models import Attendance, AttendanceLevel
from .serializers import AttendanceSerializer, AttendanceLevelSerializer

# Barcha attendance larni olish
class AttendanceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Attendance yaratish
class AttendanceCreateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Attendance tafsiloti
class AttendanceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            attendance = Attendance.objects.get(id=id)
        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Attendance yangilash
class AttendanceUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def put(self, request, id):
        try:
            attendance = Attendance.objects.get(id=id)
        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Attendance o‘chirish
class AttendanceDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            attendance = Attendance.objects.get(id=id)
        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        attendance.delete()
        return Response({'message': 'Attendance deleted successfully'}, status=status.HTTP_200_OK)

# Attendance level lar (statuslar)
class AttendanceLevelListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        levels = AttendanceLevel.objects.all()
        serializer = AttendanceLevelSerializer(levels, many=True)
        return Response(serializer.data)

class AttendanceLevelCreateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=AttendanceLevelSerializer)
    def post(self, request):
        serializer = AttendanceLevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
