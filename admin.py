
from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Course, Lesson, Question, Choice, Submission


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "grade")
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "score", "exam_date")
    list_filter = ("course",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissionAdmin)

