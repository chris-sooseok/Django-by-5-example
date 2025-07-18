from rest_framework import generics
from rest_framework import viewsets
from courses.api.serializers import SubjectSerializer, CourseSerializer
from courses.models import Subject, Course
from django.db.models import Count
from courses.api.pagination import StandardPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseWithContentsSerializer

# class SubjectListView(generics.ListAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer
#     pagination_class = StandardPagination
#
# class SubjectDetailView(generics.RetrieveAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer

# ? viewset lets DRF build URLs dynamically with a Router object
# ? with viewset you can avoid repeating logic for multiple views
class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination

class CourseViewSet(viewsets.ReadOnlyModelViewSet):

    # ? adding additional action to viewsets, the method name is also used as url
    @action(
        # ? indicating this is an action to be performed on a single object
        detail=True,
        methods=['POST'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(
        detail=True,
        methods=['get'],
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled]
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # ? prefetch fetches the related Module objects in an efficient manner
    # ? this will avoid additional SQL queries when serializing nested modules for each course
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

# ? custom API view, but is also added to above viewset as an additional action
class CourseEnrollView(APIView):
    # ? requires credentials from Authentication header
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})