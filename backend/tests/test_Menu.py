import pytest
from django.core.cache import cache
from django.forms import ValidationError
from menu.managers import MenuManager
from menu.models import Menu


@pytest.mark.django_db
class TestMenu:
    CACHE_NAME = 'menu_qs'
    NAME_MIN_LEN = 3
    HREF_MIN_LEN = 3
    NAME_MAX_LEN = 30
    HREF_MAX_LEN = 30

    @pytest.fixture
    def menu_links(self):
        home = Menu.objects.create(name='Home page')
        Menu.objects.create(name='Support')

        cats = Menu.objects.create(name='Categories', parent=home)
        Menu.objects.create(name='Category 1', parent=cats)
        Menu.objects.create(name='Category 2', parent=cats)

        about = Menu.objects.create(name='About us', parent=home)
        Menu.objects.create(name='Contacts', parent=about)

        assert Menu.objects.count() == 7
        return Menu.objects.all()

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        cache.clear()
        assert cache.get(self.CACHE_NAME) is None
        yield
        cache.clear()
        assert cache.get(self.CACHE_NAME) is None

    def test_required_fields(self):
        with pytest.raises(ValidationError) as e:
            Menu.objects.create()
        assert e.value.message_dict == {'name': ['Это поле не может быть пустым.']}  # fmt:skip # noqa: E501

    def test_min_max_length(self):
        msg = 'Убедитесь, что это значение содержит не {comp} {must} символов (сейчас {passed}).'  # noqa: E501
        short_name = 'a' * (self.NAME_MIN_LEN - 1)
        short_href = 'a' * (self.HREF_MIN_LEN - 1)
        long_name = 'a' * (self.NAME_MAX_LEN + 1)
        long_href = 'a' * (self.HREF_MAX_LEN + 1)

        with pytest.raises(ValidationError) as e:
            Menu.objects.create(name=short_name, href=short_href)
        assert e.value.message_dict == {
            'name': [msg.format(comp='менее', must=self.NAME_MIN_LEN, passed=len(short_name))],  # fmt:skip # noqa: E501
            'href': [msg.format(comp='менее', must=self.HREF_MIN_LEN, passed=len(short_href))],  # fmt:skip # noqa: E501
        }

        with pytest.raises(ValidationError) as e:
            Menu.objects.create(name=long_name, href=long_href)
        assert e.value.message_dict == {
            'name': [msg.format(comp='более', must=self.NAME_MAX_LEN, passed=len(long_name))],  # fmt:skip # noqa: E501
            'href': [msg.format(comp='более', must=self.HREF_MAX_LEN, passed=len(long_href))],  # fmt:skip # noqa: E501
        }

    @pytest.mark.parametrize(
        argnames='href_str',
        argvalues=(
            pytest.param('Root link', id='latin with space'),
            pytest.param('Корневая ссылка', id='cyrillic with space'),
        ),
    )
    def test_slugify_validation(self, href_str: str):
        with pytest.raises(ValidationError) as e:
            Menu.objects.create(name='Root link', href=href_str)
        assert e.value.message_dict == {
            'href': ['Значение должно состоять только из латинских букв, цифр, знаков подчеркивания или дефиса.'],  # fmt:skip # noqa: E501
        }

    def test_slugify(self):
        p = Menu.objects.create(name='Главная ссылка')
        assert p.href == 'glavnaia-ssylka'

    def test_retrieve(self):
        p = Menu.objects.create(name='Parent link', href='parent-link')
        Menu.objects.create(name='Child link', href='child-link', parent=p)
        assert Menu.objects.count() == 2

        p, c = Menu.objects.all()
        assert p.name == 'Parent link'
        assert p.href == 'parent-link'
        assert c.name == 'Child link'
        assert c.href == 'child-link'
        assert c.parent == p

    def test_caching_on_retrieve(self, menu_links: MenuManager):
        # clear_cache autouse
        Menu.objects.all()
        cached = cache.get(self.CACHE_NAME)
        assert cached is not None
        assert list(cached) == list(Menu.objects.all())
        # QuerySet are non-comparable values_left == values_right & id_left != id_right # noqa: E501
        # id(Menu.objects.all()) == id(Menu.objects.all()) => False

    def test_caching_on_create(self, menu_links: MenuManager):
        cache_before: MenuManager = cache.get(self.CACHE_NAME)
        Menu.objects.create(name='New link')
        cache_after: MenuManager = cache.get(self.CACHE_NAME)

        assert cache_before.count() != cache_after.count()
        assert list(cache_after) == list(Menu.objects.all())

    def test_caching_on_update(self, menu_links: MenuManager):
        cache_before: MenuManager = cache.get(self.CACHE_NAME)
        # TODO on update post_save signal is not called!
        Menu.objects.filter(pk=1).update(name='Absolutely new link!!!')
        cache_after: MenuManager = cache.get(self.CACHE_NAME)

        assert (e := cache_after.get(pk=1)).name == 'Absolutely new link!!!'
        assert e.href == cache_before.get(pk=1).href
        assert cache_before.count() == cache_after.count()
        assert list(cache_before) != list(cache_after)

    def test_caching_on_delete(self, menu_links: MenuManager):
        to_delete = Menu.objects.create(name='Link to delete')
        cache_before: MenuManager = cache.get(self.CACHE_NAME)
        assert cache_before.contains(to_delete)

        Menu.objects.filter(pk=to_delete.pk).delete()
        cache_after: MenuManager = cache.get(self.CACHE_NAME)

        assert list(cache_before) != list(cache_after)
        assert cache_after.count() == cache_before.count() - 1
        assert not cache_after.contains(to_delete)
