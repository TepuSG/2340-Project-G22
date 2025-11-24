from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from profiles.models import Profile
from django.urls import reverse

User = get_user_model()

class CandidateSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create Recruiter 1 (The one searching)
        self.recruiter1 = User.objects.create_user(username='recruiter1', password='password', role=User.Roles.RECRUITER)
        self.profile_r1 = Profile.objects.create(user=self.recruiter1, is_public=True, skills="python")

        # Create Recruiter 2 (Another recruiter)
        self.recruiter2 = User.objects.create_user(username='recruiter2', password='password', role=User.Roles.RECRUITER)
        self.profile_r2 = Profile.objects.create(user=self.recruiter2, is_public=True, skills="python")

        # Create Seeker (The candidate)
        self.seeker = User.objects.create_user(username='seeker', password='password', role=User.Roles.SEEKER)
        self.profile_s = Profile.objects.create(user=self.seeker, is_public=True, skills="python")

    def test_candidate_search_excludes_recruiters(self):
        self.client.login(username='recruiter1', password='password')
        
        # Assuming the URL name is 'recommended.candidate_search' based on grep results
        url = reverse('recommended.candidate_search')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        candidates = response.context['candidates']
        candidate_profiles = [c['profile'] for c in candidates]
        
        # Seeker should be present
        self.assertIn(self.profile_s, candidate_profiles)
        
        # Recruiter 1 (self) should NOT be present
        self.assertNotIn(self.profile_r1, candidate_profiles)
        
        # Recruiter 2 (other recruiter) should NOT be present
        self.assertNotIn(self.profile_r2, candidate_profiles)

    def test_recruiter_overview_excludes_recruiters(self):
        self.client.login(username='recruiter1', password='password')
        
        # Create a job for recruiter1 so that overview logic runs fully
        from jobs.models import Job
        Job.objects.create(
            recruiter=self.recruiter1, 
            title="Python Dev", 
            skills="python", 
            location="Remote", 
            salary=100000, 
            description="Test Job"
        )

        url = reverse('recommended.overview')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        candidates = response.context['candidates']
        candidate_profiles = [c['profile'] for c in candidates]
        
        # Seeker should be present (because skills match "python")
        self.assertIn(self.profile_s, candidate_profiles)
        
        # Recruiter 1 (self) should NOT be present
        self.assertNotIn(self.profile_r1, candidate_profiles)
        
        # Recruiter 2 (other recruiter) should NOT be present
        self.assertNotIn(self.profile_r2, candidate_profiles)

