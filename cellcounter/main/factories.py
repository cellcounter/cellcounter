import factory
import factory.fuzzy
from django.contrib.auth.models import User

from cellcounter.main import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "test%s" % n)
    first_name = factory.fuzzy.FuzzyText(length=6)
    last_name = factory.fuzzy.FuzzyText(length=6)
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'test')

    is_active = True
    is_staff = False
    is_superuser = False


class CellTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CellType

    readable_name = 'test'
    machine_name = 'test'
    abbr_name = 'test'
    comment = "Test"
    visualisation_colour = '#FFFFFF'


class LicenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.License

    title = "a"
    details = "a"


class CopyrightHolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CopyrightHolder

    name = "a"

    @factory.post_generation
    def users(self, create, extracted):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.user.add(user)
        else:
            self.user.add(UserFactory())


class CellImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CellImage

    title = "test"
    description = "test"
    file = factory.django.ImageField(color='blue')
    thumbnail_left = 1
    thumbnail_top = 1
    thumbnail_width = 100

    celltype = factory.SubFactory(CellTypeFactory)
    uploader = factory.SubFactory(UserFactory)
    copyright = factory.SubFactory(CopyrightHolderFactory)
    license = factory.SubFactory(LicenseFactory)


class SimilarLookingGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SimilarLookingGroup

    name = "a"

    @factory.post_generation
    def cell_image(self, create, extracted):
        if not create:
            return

        if extracted:
            for cell_image in extracted:
                self.cell_image.add(cell_image)
        else:
            self.cell_image.add(CellImageFactory())
