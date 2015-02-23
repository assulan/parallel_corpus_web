
from parallel_corpus_web.models import ParallelPage, MyUser
from django.contrib import admin
from django.contrib.auth.models import User


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_work')
    list_filter = ('has_work', )

admin.site.register(MyUser, MyUserAdmin)

class ParallelPageAdmin(admin.ModelAdmin):
    list_display = ('my_user', 'is_assigned')
    list_filter = ('is_assigned', 'is_test', 'is_dev', 'my_user', 'correct_score', 'incorrect_score')


admin.site.register(ParallelPage, ParallelPageAdmin)