from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class Group(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Expense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Split(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
