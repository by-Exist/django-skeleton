from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=20)


class NestedCollection(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey(Collection, on_delete=models.CASCADE)


class NestedResource(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey(Collection, on_delete=models.CASCADE)
