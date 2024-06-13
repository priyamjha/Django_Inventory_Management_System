from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    initial_amount = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class IssueItem(models.Model):
    dept_choices = (
        ('Field', 'Field'),
        ('Security', 'Security')
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    issued_amount = models.PositiveIntegerField()
    issued_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    issued_to = models.CharField(max_length=100)
    department = models.CharField(max_length=30, choices=dept_choices)
    issued_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField()
    #is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item} - {self.issued_to}'


class ReturnItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    returned_date = models.DateTimeField(auto_now_add=True)
    returned_amount = models.PositiveIntegerField()
    #all_items_returned = models.BooleanField(default=False)
    returned_by = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.item} - {self.returned_by}'


class RestockItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    initial_value = models.PositiveIntegerField(null=True, blank=True)