from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.attendances.models import Attendance
from apps.courses.models import Group


class AllGroupsStatsView(APIView):

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="All groups statistics",
                examples={
                    "application/json": [
                        {
                            "group": "English A1",
                            "start_date": "2025-09-01",
                            "end_date": "2025-12-15",
                            "active_students": 12,
                            "failed_students": 3
                        }
                    ]
                }
            )
        }
    )
    def get(self, request):
        data = []
        for group in Group.objects.all():
            active_students = Attendance.objects.filter(
                group=group, level__title='Present'
            ).values('student').distinct().count()
            failed_students = Attendance.objects.filter(
                group=group, level__title='Failed'
            ).values('student').distinct().count()

            data.append({
                "group": group.title,
                "start_date": group.start_date,
                "end_date": group.end_date,
                "active_students": active_students,
                "failed_students": failed_students
            })
        return Response(data)  # ✅ Har doim DRF Response qaytariladi

class StudentsStatisticsView(APIView):
    """
    Get all groups with students statistics:
    - active students
    - failed students
    - start and end dates
    """
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Students statistics for all groups",
                examples={
                    "application/json": [
                        {
                            "group": "English A1",
                            "start_date": "2025-09-01",
                            "end_date": "2025-12-15",
                            "active_students": 12,
                            "failed_students": 3
                        }
                    ]
                }
            )
        }
    )
    def get(self, request):
        data = []
        for group in Group.objects.all():
            active_students = Attendance.objects.filter(
                group=group, level__title='Present'
            ).values('student').distinct().count()
            failed_students = Attendance.objects.filter(
                group=group, level__title='Failed'
            ).values('student').distinct().count()

            data.append({
                "group": group.title,
                "start_date": group.start_date,
                "end_date": group.end_date,
                "active_students": active_students,
                "failed_students": failed_students
            })
        return Response(data)