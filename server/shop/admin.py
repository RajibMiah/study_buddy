from django.contrib import admin

from shop.models import Account, Course, CourseModule

admin.site.register(Account)
admin.site.register(Course)
admin.site.register(CourseModule)
