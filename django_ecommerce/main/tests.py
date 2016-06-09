"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import index
from django.shortcuts import render_to_response
from payments.models import User
from django.test import RequestFactory
import mock


class MainPageTests(TestCase):

    #############
    ### Setup ###
    #############
    
    @classmethod
    def setUpClass(cls):
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

    ##############    
    ### Routes ###
    ##############

    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_returns_appropriate_html_response_code(self):
        resp = index(self.request)
        self.assertEquals(resp.status_code, 200)

    #########################    
    ### Templates / Views ###
    #########################

    def test_returns_exact_html(self):
        resp = index(self.request)
        self.assertEquals(
            resp.content,
            render_to_response('index.html').content
        )

    def test_index_handles_logged_in_user(self):
        #create the user to lookup
        from payments.models import User 
        user = User(
            name='jj',
            email='j@j.com',
        )
        #create a session that appears to have a logged in user
        self.request.session = {'user':'1'}
        
        with mock.patch('main.views.User') as user_mock:

            #Tell the mock what to do when called
            config = {'get_by_id.return_value':mock.Mock()}
            user_mock.configure_mock(**config)

            #request the index page
            resp=index(self.request)

            #return session to its prev state
            self.request.session = {}

            #verify it returns the page for the logged in user
            expectedHtml = render_to_response(
                'user.html', 
                {'user':user_mock.get_by_id(1)}
            )
            self.assertEquals(resp.content, expectedHtml)