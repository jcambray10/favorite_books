from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        check = User.objects.filter(email=postdata['email'])
        if len(postdata['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long."
        if len(postdata['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long."
        if len(postdata['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters."
        elif postdata['password'] != postdata['confirm_password']:
            errors['password'] = "Passwords do not match."
        if len(postdata['email']) < 1:
            errors['reg_email'] = "Email address cannot be blank."
        elif not EMAIL_REGEX.match(postdata['email']):
            errors['reg_email'] = "Please enter a valid email address."
        elif check:
            errors['reg_email'] = "Email address is already registered."
        return errors

    def login_validator(self, postdata):
        errors= {}
        check = User.objects.filter(email=postdata['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postdata['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title cannot be blank."
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 characters long."
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()