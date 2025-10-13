from rest_framework import serializers
from .models import Attendance, AttendanceLevel
from apps.courses.models import Student, Group

class AttendanceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceLevel
        fields = ['id', 'title', 'descriptions']

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    group_name = serializers.CharField(source='group.title', read_only=True)
    level_title = serializers.CharField(source='level.title', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'group', 'group_name', 'level', 'level_title', 'created', 'updated']
