"""
"""
import json
import random

from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.urls import resolve
from rest_framework.authtoken.models import Token

from . import models

# Create your tests here.
test_user = [
    {'username': 'test_1', 'first_name': 'test_1',
        'last_name': 'test_1', 'email': 'test_1@test.com'},
    {'username': 'test_2', 'first_name': 'test_2',
        'last_name': 'test_2', 'email': 'test_2@test.com'},
    {'username': 'test_3', 'first_name': 'test_3',
        'last_name': 'test_3', 'email': 'test_3@test.com'},
]

test_task = [
    {
        'name': 'test 1',
        'description': 'description 1',
        'task_status': random.choice(
                [models.TaskList.DONE, models.TaskList.UNDONE]),
        'user':''
    },
    {
        'name': 'test 2',
        'description': 'description 2',
        'task_status': random.choice(
                [models.TaskList.DONE, models.TaskList.UNDONE]),
        'user':''
    },
    {
        'name': 'test 3',
        'description': 'description 3',
        'task_status': random.choice(
                [models.TaskList.DONE, models.TaskList.UNDONE]),
        'user':''
    },
]


class TaskListTestCases(APITestCase):
    """docstring for TaskListTestCases"""

    def create_test_users(self):
        """ Create dummy test user record
        """
        for user_obj in test_user:
            User.objects.create(
                username=user_obj['username'],
                first_name=user_obj['first_name'],
                last_name=user_obj['last_name'],
                email=user_obj['email']
            ).set_password(
                User.objects.make_random_password()
            )

    def create_test_task(self):
        """docstring for create_test_task"""
        user_list = User.objects.all()
        for task in test_task:
            user = random.choice(user_list)
            models.TaskList.objects.create(
                name=task['name'] + str(user.id),
                description=task['description'],
                task_status=task['task_status'],
                user=user
            )

    def setUp(self):
        """ Set up dummy test data
        """
        self.create_test_users()
        self.create_test_task()

    def test_task_list(self):
        """ Check API key following validation scenarios
        1. Check API response (200, 403)
        2. Check user validation
        3. Check API response
        """
        task_list_url = reverse("task-list")
        user_list = User.objects.all()
        user = random.choice(user_list)
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            task_list_url
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_crud_task_update(self):
        """ Check API key following validation scenarios
        1. Check CRUD API response (200, 201, 204)
        2. Check user permission to modify
        3. Check API response
        """
        task_list_url = reverse("task-list")
        user_list = User.objects.all()
        user = random.choice(user_list)
        task = {
            'name': 'new task',
            'description': 'new task description',
            'task_status': random.choice(
                    [models.TaskList.DONE, models.TaskList.UNDONE])
        }
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            task_list_url,
            task
        )
        # Check that the response is 201 OK.
        self.assertEqual(response.status_code, 201)

        task_id = response.data['id']

        task['name'] = "update task"
        url = reverse("task-retrieve",
                      kwargs={"task_id": task_id})
        response = self.client.put(
            url, task
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        url = reverse("task-retrieve",
                      kwargs={"task_id": task_id})
        response = self.client.delete(
            url
        )
        # Check that the response is 204 OK.
        self.assertEqual(response.status_code, 204)
