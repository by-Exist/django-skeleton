import factory
from ..models import Collection, NestedCollection, NestedResource


class CollectionFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"[{n}] Collection")

    class Meta:
        model = Collection


class NestedCollectionFactory(factory.django.DjangoModelFactory):
    parent = factory.SubFactory(CollectionFactory)
    title = factory.Sequence(lambda n: f"[{n}] N-Collection")

    class Meta:
        model = NestedCollection


class NestedResourceFactory(factory.django.DjangoModelFactory):
    parent = factory.SubFactory(CollectionFactory)
    title = factory.Sequence(lambda n: f"[{n}] N-Resource")

    class Meta:
        model = NestedResource
