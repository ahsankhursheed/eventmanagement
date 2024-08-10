from django.test import TestCase, Client
from django.urls import reverse
from .models import Event, CustomUsers
from django.contrib import messages

class EventTests(TestCase):
    
    def setUp(self):

        self.user = CustomUsers.objects.create_user(username='testuser', password='testpassword')
        self.owner = CustomUsers.objects.create_user(username='owner', password='ownerpassword')
        
        self.event = Event.objects.create(
            title='Test Event',
            description='A test event description.',
            date='2024-08-15',
            location='Test Location',
            owner=self.owner
        )
        self.client = Client()
    
    def test_event_list_view(self):

        response = self.client.get(reverse('events:event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_list.html')
        self.assertContains(response, 'Test Event')
    
    def test_event_detail_view(self):

        response = self.client.get(reverse('events:event_detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_detail.html')
        self.assertContains(response, 'Test Event')
        self.assertContains(response, 'A test event description.')
    
    def test_event_create_view(self):

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('events:event_create'), {
            'title': 'New Event',
            'description': 'New event description',
            'date': '2024-08-20',
            'location': 'New Location',
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Event.objects.filter(title='New Event').exists())
    
    def test_event_update_view(self):

        self.client.login(username='owner', password='ownerpassword')
        response = self.client.post(reverse('events:event_update', kwargs={'pk': self.event.pk}), {
            'title': 'Updated Event',
            'description': 'Updated description',
            'date': '2024-09-01',
            'location': 'Updated Location',
        })
        self.assertEqual(response.status_code, 302) 
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event')
    
    def test_event_delete_view(self):

        self.client.login(username='owner', password='ownerpassword')
        response = self.client.post(reverse('events:event_delete', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())
    
    def test_user_logout_view(self):

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('events:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)
    
    def test_attend_event_view(self):

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('events:attend_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.event.attendees.all())
    
    def test_unattend_event_view(self):

        self.event.attendees.add(self.user)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('events:unattend_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, self.event.attendees.all())
    


    def test_owner_cannot_attend_event(self):
        self.client.login(username='owner', password='ownerpassword')
        response = self.client.get(reverse('events:attend_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.owner, self.event.attendees.all())

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == "You cannot attend your own event." for msg in messages_list))


