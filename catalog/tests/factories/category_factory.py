import factory

from catalog.models.category import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    category_name = factory.Faker("word")
