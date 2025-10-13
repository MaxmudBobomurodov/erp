from django.urls import path

from apps.accounts.other_views.students import StudentListView, StudentDetailView, StudentUpdateView, \
    GetStudentsByIdsView, StudentAttendanceView, StudentGroupsView
from apps.accounts.other_views.teachers import TeacherListView, TeacherDetailView, TeacherUpdateView, \
    GetTeachersByIdsView, TeacherGroupsView
from apps.accounts.other_views.users import UserListAPIView, StudentCreateAPIView, TeacherCreateAPIView, \
    SuperuserCreateView, UserCreateView, UserDeleteView
from apps.accounts.views import LoginAPIView, LogoutAPIView, MyView, ChangeUserPasswordView, ResetUserPasswordView, \
    VerifyOtpView, SetNewPasswordView

app_name = "accounts"

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/me/', MyView.as_view(), name='me'),
    path('users/', UserListAPIView.as_view(), name='users'),
    path('users/create/student/', StudentCreateAPIView.as_view(), name='student-create'),
    path('users/create/teacher/', TeacherCreateAPIView.as_view(), name='teacher-create'),
    path('auth/change-password/', ChangeUserPasswordView.as_view(), name='change-password'),
    path('auth/reset-password/', ResetUserPasswordView.as_view(), name='reset-password'),
    path('auth/verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('auth/set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('users/create/superuser/', SuperuserCreateView.as_view(), name='create-superuser'),
    path('users/create/user/', UserCreateView.as_view(), name='create-user'),
    path('users/delete/user/{id}/', UserDeleteView.as_view(), name='user-delete'),
    path('users/students/', StudentListView.as_view()),
    path('users/student/<int:id>/', StudentDetailView.as_view()),
    path('users/update/student/<int:id>/', StudentUpdateView.as_view()),
    path('users/get-students-by-ids/', GetStudentsByIdsView.as_view()),
    path('student-groups/<int:student_id>/', StudentGroupsView.as_view()),
    path('attendance/student/<int:student_id>/', StudentAttendanceView.as_view()),
    path('users/teachers/', TeacherListView.as_view()),
    path('users/teacher/<int:id>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('users/update/teacher/<int:id>/', TeacherUpdateView.as_view(), name='teacher-update'),
    path('users/get-teachers-by-ids/', GetTeachersByIdsView.as_view(), name='teacher-by-ids'),
    path('teacher-groups/<int:teacher_id>/', TeacherGroupsView.as_view(), name='teacher-groups'),

]

