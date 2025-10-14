from django.urls import path

from apps.courses.views import CourseListView, CourseCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView, \
    TableTypeListView, TableTypeCreateView, TableTypeDetailView, TableTypeUpdateView, TableTypeDeleteView, \
    TableListView, TableCreateView, TableDetailView, TableUpdateView, TableDeleteView, RoomListView, RoomCreateView, \
    RoomDetailView, RoomUpdateView, RoomDeleteView, GroupListView, GroupCreateView, GroupDetailView, GroupDeleteView, \
    GroupUpdateView, AddStudentView, RemoveStudentView, AddTeacherView, RemoveTeacherView

urlpatterns = [
    # Courses
    path('courses/', CourseListView.as_view(), name='course-list'),  # GET all courses
    path('courses/create/course/', CourseCreateView.as_view(), name='course-create'),  # POST new course
    path('courses/<int:id>/', CourseDetailView.as_view(), name='course-detail'),  # GET course detail
    path('courses/<int:id>/update/course/', CourseUpdateView.as_view(), name='course-update'),  # PUT update
    path('courses/<int:id>/delete/course/', CourseDeleteView.as_view(), name='course-delete'),  # DELETE

    # Tably-type
    path('table-types/', TableTypeListView.as_view(), name='tabletype-list'),
    path('table-types/create/tabletype/', TableTypeCreateView.as_view(), name='tabletype-create'),
    path('table-types/<int:pk>/', TableTypeDetailView.as_view(), name='tabletype-detail'),
    path('table-types/<int:pk>/update/tabletype/', TableTypeUpdateView.as_view(), name='tabletype-update'),
    path('table-types/<int:pk>/delete/tabletype/', TableTypeDeleteView.as_view(), name='tabletype-delete'),

    # Table
    path('tables/', TableListView.as_view(), name='table-list'),
    path('tables/create/table/', TableCreateView.as_view(), name='table-create'),
    path('tables/<int:pk>/', TableDetailView.as_view(), name='table-detail'),
    path('tables/<int:pk>/update/table/', TableUpdateView.as_view(), name='table-update'),
    path('tables/<int:pk>/delete/table/', TableDeleteView.as_view(), name='table-delete'),

    # room
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/create/room/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/update/room/', RoomUpdateView.as_view(), name='room-update'),
    path('rooms/<int:pk>/delete/room/', RoomDeleteView.as_view(), name='room-delete'),

    # Group
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/group/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:pk>/update/group/', GroupUpdateView.as_view(), name='group-update'),
    path('groups/<int:pk>/delete/group/', GroupDeleteView.as_view(), name='group-delete'),
    # Group add/remove
    path('courses/groups/<int:pk>/add-student/', AddStudentView.as_view(), name='group-add-student'),
    path('courses/groups/<int:pk>/remove-student/', RemoveStudentView.as_view(), name='group-remove-student'),
    path('courses/groups/<int:pk>/add-teacher/', AddTeacherView.as_view(), name='group-add-teacher'),
    path('courses/groups/<int:pk>/remove-teacher/', RemoveTeacherView.as_view(), name='group-remove-teacher'),
]
