from django.db import models
from django.db.models import Count

import uuid

class AgentType(models.TextChoices):
    SUPPLIER = "SUPPLIER"
    CONSUMER = "CONSUMER"
    OTHER = "OTHER"

class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)    
    type = models.CharField(max_length=8,
                            choices=AgentType.choices, default=AgentType.OTHER)
    phone = models.CharField(max_length=23, null=True)
    notes = models.TextField(null=True)
    
    def __str__(self):
        return str(self.name)

class Stack(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.TextField(null=True)        

class Cell(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Stack, on_delete=models.CASCADE)
    is_filled = models.BooleanField(default=False)
    notes = models.TextField(null=True)

class Supply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    count = models.IntegerField(default=1)
    agent_id = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        queryset = type(self).objects.filter(cell_id=self.cell_id).annotate(Count('cell_id'))

        if queryset.exists() and queryset.first().count >= 1:
            raise Exception('Максимальное количество ссылок (1) достигнуто.')
        super().save(*args, **kwargs)
        
        record = Cell.objects.get(id=vars(self.cell_id)['id'])
        record.is_filled = True
        record.save()

    def delete(self, *args, **kwargs):
        record = Cell.objects.get(id=vars(self.cell_id)['id'])
        record.is_filled = False
        record.save()

        super().delete(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        prev_record = Cell.objects.get(id=vars(self.cell_id)['id'])
        prev_record.is_filled = False
        prev_record.save()

        super().update(*args, **kwargs)

        next_record = Cell.objects.get(id=vars(self.cell_id)['id'])
        next_record.is_filled = True
        next_record.save()

