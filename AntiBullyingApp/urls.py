from django.conf.urls import patterns, include, url
from HelloWorldApp import views
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^/$', views.home,name='home'),
	url(r'^/home/form/$',views.form,name='form'),
	url(r'^/home/form/output/$',views.return_data,name='return_data'),
	url(r'^/home/dashboard/doughnut/$',views.doughnut,name='doughnut'),	
)

