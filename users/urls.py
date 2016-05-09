from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'HDASE.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^sign-up', "users.views.home"),
                       url(r'^log-in', "users.views.log_in"),
                       url(r'^log-out', "users.views.log_out"),
                       url(r'^start-question', "users.views.start_question"),
                       url(r'^ask-question', "users.views.ask_question"),
                       url(r'^get-question', "users.views.get_question"),
                       url(r'^first-attempt', "users.views.first_attempt"),
                       )
