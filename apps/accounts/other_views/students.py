from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from apps.accounts.serializers import StudentSerializer
from apps.courses.models import Student


# 1️⃣ GET /users/students/ - List all students
class StudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 2️⃣ GET /users/student/{id}/ - Get student details
class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: StudentSerializer()}
    )
    def get(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 3️⃣ PUT /users/update/student/{id}/ - Update student
class StudentUpdateView(APIView):
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        request_body=StudentSerializer
    )

    def put(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student updated successfully', 'student': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4️⃣ POST /users/get-students-by-ids/ - Get students by IDs
class GetStudentsByIdsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))
            },
            required=['ids']
        ),
        responses={200: StudentSerializer(many=True)},
        operation_description="Get teachers by a list of IDs"
    )
    def post(self, request):
        ids = request.data.get('ids', [])
        students = Student.objects.filter(id__in=ids)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        groups = student.group.all().values_list('title', flat=True)
        return Response(groups, status=status.HTTP_200_OK)


class StudentAttendanceView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, student_id):
        # Bu joyni o'z modelinga qarab to'ldirasan
        # Masalan, Attendance modeli bo'lsa:
        # attendances = Attendance.objects.filter(student_id=student_id)
        # grouped_data = {...}

        grouped_data = {
            "October 2025": [
                {"date": "2025-10-01", "status": "present"},
                {"date": "2025-10-02", "status": "absent"},
            ]
        }
        return Response(grouped_data, status=status.HTTP_200_OK)
