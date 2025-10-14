from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from apps.courses.models import Course, TableType, Table, Rooms, Group, Student, Teacher
from apps.courses.serializers import CourseSerializer, TableTypeSerializer, TableSerializer, RoomSerializer, \
    GroupSerializer, AddRemoveStudentSerializer, AddRemoveTeacherSerializer


#  List all courses
class CourseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Create a new course
class CourseCreateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  Get course details
class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


#  Delete a course
class CourseDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        course.delete()
        return Response({'message': 'Course deleted successfully'}, status=status.HTTP_200_OK)


# Update a course
class CourseUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=CourseSerializer)
    def put(self, request, id):
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TableType CRUD
class TableTypeListView(generics.ListAPIView):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer


class TableTypeCreateView(generics.CreateAPIView):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer


class TableTypeDetailView(generics.RetrieveAPIView):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer


class TableTypeUpdateView(generics.UpdateAPIView):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer


class TableTypeDeleteView(generics.DestroyAPIView):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer


class TableListView(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


# Table CRUD
class TableCreateView(generics.CreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableDetailView(generics.RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableUpdateView(generics.UpdateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableDeleteView(generics.DestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


# Room Crud
class RoomListView(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer


class RoomCreateView(generics.CreateAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(generics.RetrieveAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer


class RoomUpdateView(generics.UpdateAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer


class RoomDeleteView(generics.DestroyAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupCreateView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetailView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupUpdateView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDeleteView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# add/remove student
class AddStudentView(GenericAPIView):
    serializer_class = AddRemoveStudentSerializer

    def post(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = serializer.validated_data['student_id']
        student = Student.objects.get(pk=student_id)

        if student.group.filter(pk=student_id).exists():
            return Response(
                {"error": "Student already in group"},
                status=400
            )

        student.group.add(Group.objects.get(pk=pk))

        return Response({"message": f"Student {student.full_name} added to group"})


class RemoveStudentView(GenericAPIView):
    serializer_class = AddRemoveStudentSerializer

    def post(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = serializer.validated_data['student_id']
        student = Student.objects.get(pk=student_id)
        student.group.remove(Group.objects.get(pk=pk))
        return Response({"message": "Student removed"})


class AddTeacherView(GenericAPIView):
    serializer_class = AddRemoveTeacherSerializer

    def post(self, request, pk):
        group = Group.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        teacher_id = serializer.validated_data['teacher_id']
        teacher = Teacher.objects.get(pk=teacher_id)

        if group.teacher.filter(pk=teacher_id).exists():
            return Response(
                {"error": "Teacher already in group"},
                status=400
            )

        group.teacher.add(teacher)

        return Response({"message": f"Teacher {teacher.full_name} added to group {group.title}"})


class RemoveTeacherView(GenericAPIView):
    serializer_class = AddRemoveTeacherSerializer

    def post(self, request, pk):
        group = Group.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        teacher_id = serializer.validated_data['teacher_id']
        teacher = Teacher.objects.get(pk=teacher_id)

        group.teacher.remove(teacher)

        return Response({"message": f"Teacher {teacher.full_name} removed from group {group.title}"})
