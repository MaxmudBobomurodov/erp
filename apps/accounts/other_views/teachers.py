from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers import TeacherSerializer
from apps.courses.models import Teacher, Group


class TeacherListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeacherDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: TeacherSerializer()},
        operation_description="Get details of a teacher by ID"
    )
    def get(self, request, id):
        try:
            teacher = Teacher.objects.get(id=id)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeacherUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=TeacherSerializer,
        responses={200: TeacherSerializer()},
        operation_description="Update teacher details by ID"
    )
    def put(self, request, id):
        try:
            teacher = Teacher.objects.get(id=id)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data, partial=True)  # partial=True -> qisman update
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Teacher updated successfully', 'teacher': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetTeachersByIdsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))
            },
            required=['ids']
        ),
        responses={200: TeacherSerializer(many=True)},
        operation_description="Get teachers by a list of IDs"
    )
    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        teachers = Teacher.objects.filter(id__in=ids)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeacherGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'List of group titles'},
        operation_description="Retrieve the list of groups that a specific teacher is enrolled in"
    )
    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        # Agar related_name='teacher' bo'lsa:
        groups = teacher.teacher.all().values_list('title', flat=True)

        # Agar related_name='groups' bo'lsa:
        # groups = teacher.groups.all().values_list('title', flat=True)

        return Response(list(groups), status=status.HTTP_200_OK)
