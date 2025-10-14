from rest_framework import serializers

from apps.courses.models import Course, TableType, Table, Rooms, Group, Student, Teacher


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'



class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()  # room.name ni chiqaradi
    type = serializers.StringRelatedField()  # type.title ni chiqaradi
    class Meta:
        model = Table
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    table = serializers.StringRelatedField()

    class Meta:
        model = Group
        fields = '__all__'

class AddRemoveStudentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()

    def validate_student_id(self, value):

        if not Student.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Student not found")
        return value

class AddRemoveTeacherSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()

    def validate_teacher_id(self, value):
        if not Teacher.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Teacher not found")
        return value

