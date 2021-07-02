from django.db import models


class Collection(models.Model):

    title = models.CharField("제목", max_length=20)

    class Meta:
        ordering = ["-id"]


class NestedCollection(models.Model):

    parent = models.ForeignKey(Collection, on_delete=models.CASCADE)

    title = models.CharField(max_length=20)

    class Meta:
        ordering = ["-id"]
        unique_together = ["parent", "title"]


class NestedResource(models.Model):

    parent = models.OneToOneField(
        Collection, on_delete=models.CASCADE, related_name="child"
    )

    title = models.CharField(max_length=20)

    class Meta:
        ordering = ["-id"]
