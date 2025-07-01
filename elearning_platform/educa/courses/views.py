from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Course, Subject
from django.db.models import Count
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.apps import apps
from django.forms.models import modelform_factory
from .models import Module, Content
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from students.forms import CourseEnrollForm
from django.core.cache import cache

class OwnerMixin:
    # used wuth CRUD operations overrding views get_queryset
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    # used with FormMixin which is executed when the submitted form is valid
    # the default behavior is to save the form and redirect user to success_url
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    # buidling model form
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    # template used for CreateView and UpdateView
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    # model = Course
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'
    #
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(owner=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    # ? TemplateResponseMixin renders templates and return an HTTP response
    # ? View is the basic class-based view
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        # ? get multiple forms
        return ModuleFormSet(instance=self.course, data=data)

    # dispatch is provided by View class
    # takes HTTP request and parameters to delegate to a lowercase method that matches the HTTP method used
    def dispatch(self, request, pk):
        # ? routes the HTTP request method to the appropriate method of the view class
        # ? override to include course object
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user
        )
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        # ? render course and formset for get request
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )

    def post(self, request, *args, **kwargs):
        # ? validate formset and save
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        # ? if not valid, display errors
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    content_model = None
    # ? content is set if already exist
    content = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        # ? check model name and return the actual model class
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(
                app_label='courses', model_name=model_name
            )

    def get_form(self, content_model, *args, **kwargs):
        # ? modelform is a dynamic form following
        Form = modelform_factory(
            content_model, exclude=['owner', 'order', 'created', 'updated']
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, content_id=None):
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        # ? content model
        self.content_model = self.get_model(model_name)
        # id of the object that is being updated, or none to create new objects
        if content_id:
            self.content = get_object_or_404(
                self.content_model, id=content_id, owner=request.user
            )
        return super().dispatch(request, module_id, model_name, content_id)

    def get(self, request, module_id, model_name, content_id=None):
        form = self.get_form(self.content_model, instance=self.content)
        return self.render_to_response(
            {'form': form, 'content': self.content}
        )

    def post(self, request, module_id, model_name, content_id=None):
        form = self.get_form(
            self.content_model,
            instance=self.content,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            content = form.save(commit=False)
            content.owner = request.user
            content.save()
            if not content_id:
                # new content
                Content.objects.create(module=self.module, item=content)
            return redirect('module_content_list', self.module.id)

        return self.render_to_response(
            {'form': form, 'content': self.content}
        )

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'
    def get(self, request, module_id):
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
            )
        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(
                id=id, course__owner=request.user
            ).update(order=order)

        return self.render_json_response({'saved': 'OK'})

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id, module__course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')

        if not subjects:
            subjects = Subject.objects.annotate(
                total_courses=Count('courses')
            )
            cache.set('all_subjects', subjects)

        all_courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        if subject:
            # if subject given, cache courses of the subject
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            # if no subject is given, cache all courses
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)

        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses,
            }
        )

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            # ! object attribute is automatically set by get_object method retrieved by pk passed to this path
            initial={'course': self.object}
        )
        return context