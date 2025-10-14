from django.urls import path

from apps.erp_statistics.views import AllGroupsStatsView, StudentsStatisticsView

urlpatterns = [
    path('student/', AllGroupsStatsView.as_view(), name='attendance-list'),
    path('statistics/students-statistic/', StudentsStatisticsView.as_view(), name='students-statistics'),

]
