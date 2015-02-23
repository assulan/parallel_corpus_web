from django.conf.urls import patterns, include, url
from parallel_corpus_web import receivers

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'parallel_corpus_web.views.index', name='index'),
    url(r'^logout/$', 'parallel_corpus_web.views.logout', name='logout'),
    url(r'^home/$', 'parallel_corpus_web.views.home', name='home'),
    url(r'^correct/(\d+)/(\d+)/$', 'parallel_corpus_web.views.correct', name='correct'),
    url(r'^incorrect/(\d+)/(\d+)/$', 'parallel_corpus_web.views.incorrect', name='incorrect'),
    url(r'^about/$', 'parallel_corpus_web.views.about', name='about'),
    url(r'^download/$', 'parallel_corpus_web.views.download', name='download'),
    url(r'^stats/$', 'parallel_corpus_web.views.stats', name='stats'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

