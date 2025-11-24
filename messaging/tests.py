from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core import mail
from .models import Message

User = get_user_model()

class MessageTests(TestCase):
    def setUp(self):
        self.seeker = User.objects.create_user(username='seeker', password='password', role='SEEKER', email='seeker@example.com')
        self.recruiter = User.objects.create_user(username='recruiter', password='password', role='RECRUITER', email='recruiter@example.com')
        self.client = Client()

    def test_send_message(self):
        self.client.login(username='seeker', password='password')
        response = self.client.post(f'/messaging/{self.recruiter.username}/', {'body': 'Hello Recruiter'})
        self.assertEqual(response.status_code, 302) # Redirects after post
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.first()
        self.assertEqual(message.sender, self.seeker)
        self.assertEqual(message.recipient, self.recruiter)
        self.assertEqual(message.body, 'Hello Recruiter')

    def test_inbox(self):
        Message.objects.create(sender=self.seeker, recipient=self.recruiter, body='Hello')
        self.client.login(username='seeker', password='password')
        response = self.client.get('/messaging/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'recruiter')
        self.assertContains(response, 'Hello')

    def test_conversation(self):
        Message.objects.create(sender=self.seeker, recipient=self.recruiter, body='Hello')
        self.client.login(username='recruiter', password='password')
        response = self.client.get(f'/messaging/{self.seeker.username}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')
        # Check if marked as read
        self.assertTrue(Message.objects.first().is_read)

    def test_send_email(self):
        self.client.login(username='recruiter', password='password')
        response = self.client.post(f'/messaging/email/{self.seeker.username}/', {
            'subject': 'Job Opportunity',
            'message': 'We have a job for you.'
        })
        self.assertEqual(response.status_code, 302) # Redirects after post
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Job Opportunity')
        self.assertEqual(mail.outbox[0].body, 'We have a job for you.')
        self.assertEqual(mail.outbox[0].to, ['seeker@example.com'])
        # Check Reply-To is set to recruiter's email
        self.assertEqual(mail.outbox[0].reply_to, ['recruiter@example.com'])

    def test_update_email_and_receive(self):
        # 1. Seeker updates email
        self.client.login(username='seeker', password='password')
        # Note: profile_edit view expects profile form data as well, so we need to provide it or it might fail validation
        # Let's check what fields are required in ProfileForm. 
        # Looking at profiles/forms.py, no fields seem explicitly required=True in the form definition, 
        # but let's provide some data to be safe.
        response = self.client.post('/profiles/me/edit/', {
            'email': 'newemail@example.com',
            'headline': 'New Headline',
            'skills': 'Python',
            'education-TOTAL_FORMS': '0',
            'education-INITIAL_FORMS': '0',
            'experience-TOTAL_FORMS': '0',
            'experience-INITIAL_FORMS': '0',
            'links-TOTAL_FORMS': '0',
            'links-INITIAL_FORMS': '0',
        })
        self.assertEqual(response.status_code, 302) # Should redirect
        
        self.seeker.refresh_from_db()
        self.assertEqual(self.seeker.email, 'newemail@example.com')

        # 2. Recruiter sends email to seeker
        self.client.login(username='recruiter', password='password')
        response = self.client.post(f'/messaging/email/{self.seeker.username}/', {
            'subject': 'Job Opportunity',
            'message': 'We have a job for you.'
        })
        
        self.assertEqual(len(mail.outbox), 1) # Should be 1 because test runner clears outbox between tests usually, or we just check the last one
        self.assertEqual(mail.outbox[-1].to, ['newemail@example.com'])
