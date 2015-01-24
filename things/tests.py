from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.test import Client, TestCase

from .models import Thing, ThingTaker


class ThingBasicTest(TestCase):
    def setUp(self):
        self.book = Thing.objects.create(name='Book')
        self.table = Thing.objects.create(name='Table')
        self.ola = ThingTaker.objects.create(
            first_name='Ola',
            last_name='Sendecka',
        )
        self.tomek = ThingTaker.objects.create(
            first_name='Tomek',
            last_name='Paczkowski',
        )


class ThingTest(ThingBasicTest):
    def test_things_are_displayed(self):
        url = reverse('things:list', kwargs={'token': self.ola.token})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'things/list.html')
        self.assertContains(response, self.book.name)
        self.assertContains(response, self.table.name)

    def test_thing_detail_page_is_displayed(self):
        url = reverse('things:detail',
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'things/detail.html')
        self.assertContains(response, self.book.name)

    def test_thing_taken_by_user(self):
        self.book.taken_by = self.ola
        self.book.save()
        url = reverse('things:detail',
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.get(url)
        self.assertContains(response, self.book.taken_by.first_name)
        self.assertContains(response, self.book.taken_by.last_name)


class TakeThingTest(ThingBasicTest):
    def test_take_thing(self):
        url = reverse('things:take',
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.post(url, data={'taker_token': self.ola.token})
        
        self.assertEqual(302, response.status_code)
        book = Thing.objects.get(pk=self.book.pk)
        self.assertEquals(self.ola, book.taken_by)

    def test_take_thing_with_invalid_token(self):
        invalid_token = 'xxxxx'
        url = reverse('things:take',
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.post(url, data={'token': invalid_token})
        
        self.assertEquals(404, response.status_code)

    def test_take_thing_with_no_token(self):
        url = reverse('things:take', 
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.post(url, data={})
        self.assertEquals(404, response.status_code)

    def test_token_from_url_in_take_form(self):
        url = reverse('things:detail',
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'things/detail.html')
        button_code = render_to_string(
            'things/include/take_form.html', 
            {'token': self.ola.token, 'thing': self.book})
        self.assertContains(response, self.ola.token)

    def test_cannot_take_thing_when_its_taken(self):
        self.book.taken_by = self.tomek
        self.book.save()
        url = reverse('things:detail',
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.get(url)
        
        self.assertNotContains(response, 'form')


class GiveBackThingTest(ThingBasicTest):
    def test_give_back_thing(self):
        url = reverse('things:give_back',
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.post(url, data={'taker_token': self.ola.token})
        
        self.assertEqual(302, response.status_code)
        book = Thing.objects.get(pk=self.book.pk)
        self.assertEquals(None, book.taken_by)
    
    def test_cannot_give_back_thing_taken_by_others(self):
        self.book.taken_by = self.tomek
        self.book.save()
        url = reverse('things:detail',
                      kwargs={'pk': self.book.pk, 'token': self.ola.token})
        response = self.client.get(url)
        
        self.assertNotContains(response, 'form')
