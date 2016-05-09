from django.contrib import admin
from users.models import *
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'gender')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


class AnsweredAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


class AttendedCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'weight', 'created')


class CourseQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'course', 'weight', 'created')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answered, AnsweredAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(AttendedCourse, AttendedCourseAdmin)
admin.site.register(CourseQuestion, CourseQuestionAdmin)
