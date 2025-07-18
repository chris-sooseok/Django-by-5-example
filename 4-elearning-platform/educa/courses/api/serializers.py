from rest_framework import serializers
from courses.models import Subject, Course, Module, Content
from django.db.models import Count

class SubjectSerializer(serializers.ModelSerializer):
    # adding additional field to serializer class, rendered from object being serialized
    total_courses = serializers.IntegerField()

    # serializer method field, which is a read-only field that gets its value by calling a method
    popular_courses = serializers.SerializerMethodField()

    def get_popular_courses(self, obj):
        courses = obj.courses.annotate(
            total_students=Count('students')
        ).order_by('total_students')[:3]
        return [
            f'{c.title} ({c.total_students})' for c in courses
        ]
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'total_courses', 'popular_courses']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    # ? format how modules field is serialized, rendering __str__ method value
    # modules = serializers.StringRelatedField(many=True, read_only=True)

    # ? many=True indicates you are serializing multiple objects
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'slug',
            'overview',
            'created',
            'owner',
            'modules'
        ]


# custom field
class ItemRelatedField(serializers.RelatedField):
    # ? render tamplates and items
    def to_representation(self, value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = Content
        fields = ['order', 'item']

class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)
    class Meta:
        model = Course
        fields = [
        'id',
        'subject',
        'title',
        'slug',
        'overview',
        'created',
        'owner',
        'modules'
        ]