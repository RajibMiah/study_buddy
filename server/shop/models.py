from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

# Create your models here.

SUBSCRIPTION = (
    ('F', 'FREE'),
    ('M', 'MONTHLY'),
    ('Y', 'YEARLY'),
)

User = get_user_model()


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)
    pro_expiry_date = models.DateField(null=True, blank=True)
    subscription_type = models.CharField(
        max_length=100, choices=SUBSCRIPTION, default='FREE')

    def __str__(self) -> str:
        return str(self.user)


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_description = RichTextField()
    is_premium = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to="course")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_module_name = models.CharField(max_length=100)
    course_description = RichTextField()
    video_url = models.URLField(max_length=200)
    can_view = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.course)
