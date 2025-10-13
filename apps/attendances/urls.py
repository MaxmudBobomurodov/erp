from django.urls import path
from .views import (
    AttendanceListView, AttendanceCreateView, AttendanceDetailView,
    AttendanceUpdateView, AttendanceDeleteView,
    AttendanceLevelListView, AttendanceLevelCreateView
)

urlpatterns = [
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/create/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('attendance/<int:id>/', AttendanceDetailView.as_view(), name='attendance-detail'),
    path('attendance/<int:id>/update/', AttendanceUpdateView.as_view(), name='attendance-update'),
    path('attendance/<int:id>/delete/', AttendanceDeleteView.as_view(), name='attendance-delete'),

    path('status/', AttendanceLevelListView.as_view(), name='attendance-level-list'),
    path('status/create/status/', AttendanceLevelCreateView.as_view(), name='attendance-level-create'),
]
