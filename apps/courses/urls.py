from django.urls import path

from apps.courses.views import CourseListView, CourseCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    # Courses CRUD
    path('courses/', CourseListView.as_view(), name='course-list'),  # GET all courses
    path('courses/create/course/', CourseCreateView.as_view(), name='course-create'),  # POST new course
    path('courses/<int:id>/', CourseDetailView.as_view(), name='course-detail'),  # GET course detail
    path('courses/<int:id>/update/course/', CourseUpdateView.as_view(), name='course-update'),  # PUT update
    path('courses/<int:id>/delete/course/', CourseDeleteView.as_view(), name='course-delete'),  # DELETE
]
