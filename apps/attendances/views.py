from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from .models import Attendance, AttendanceLevel
from .serializers import AttendanceSerializer, AttendanceLevelSerializer
from .teacher_permissions import IsTeacher



class AttendanceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttendanceCreateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER)
                ),
                'level_title': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['ids', 'level_title'],
            example={
                'ids': [1, 3],
                'level_title': 'Present'
            }
        )
    )
    def post(self, request):
        ids = request.data.get('ids', [])
        level_title = request.data.get('level_title')

        if not ids or not level_title:
            return Response(
                {'error': 'ids va level_title kiritilishi kerak'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            level_obj = AttendanceLevel.objects.get(title__iexact=level_title)
        except AttendanceLevel.DoesNotExist:
            return Response(
                {'error': f"'{level_title}' nomli level topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

        updated_count = Attendance.objects.filter(id__in=ids).update(level=level_obj.id)


        updated_attendances = Attendance.objects.filter(id__in=ids)
        updated_serializer = AttendanceSerializer(updated_attendances, many=True)

        all_attendances = Attendance.objects.all()
        all_serializer = AttendanceSerializer(all_attendances, many=True)

        return Response({
            'updated_count': updated_count,
            'updated_records': updated_serializer.data,
            'all_records': all_serializer.data
        }, status=status.HTTP_200_OK)


class AttendanceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            attendance = Attendance.objects.get(id=id)
        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

class AttendanceDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            attendance = Attendance.objects.get(id=id)
        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        attendance.delete()
        return Response({'message': 'Attendance deleted successfully'}, status=status.HTTP_200_OK)

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