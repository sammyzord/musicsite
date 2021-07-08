from django.test import TestCase
from django.urls import reverse
from .models import Song
from django.contrib.auth.models import User


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_login_logged_in(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/login", follow=True)
        self.assertRedirects(response, "/")

    def test_register_logged_in(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/register", follow=True)
        self.assertRedirects(response, "/")


class TrendingViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_get_anonymous(self):
        response = self.client.get("/trending", follow=True)
        self.assertRedirects(response, "/login?next=/trending")

    def test_get(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/trending")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/trending.html")


class SongViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.song = Song.objects.create(
            song_name="Test Song",
            artist_name="Test Artist",
            song_genre="Test Genre",
            user=self.user,
        )

    def test_get_anonymous(self):
        response = self.client.get("/songs", follow=True)
        self.assertRedirects(response, "/login?next=/songs")

    def test_get_user(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/songs")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/songs.html")

    def test_create(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            "/songs",
            {"song_name": "Numb", "artist_name": "Linkin Park", "song_genre": "Rock"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Song.objects.filter(song_name="Numb", artist_name="Linkin Park").exists()
        )

    def test_edit_anonymous(self):
        response = self.client.get(f"/songs/edit/{self.song.id}", follow=True)
        self.assertRedirects(response, f"/login?next=/songs/edit/{self.song.id}")

    def test_edit_wrong_user(self):
        User.objects.create_user(username="dummy", password="12345")
        self.client.login(username="dummy", password="12345")
        response = self.client.get(f"/songs/edit/{self.song.id}", follow=True)
        self.assertRedirects(response, "/songs")

    def test_get_edit(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(f"/songs/edit/{self.song.id}", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/edit_songs.html")

    def test_edit(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            f"/songs/edit/{self.song.id}",
            {"song_name": "Numb", "artist_name": "Linkin Park", "song_genre": "Rock"},
        )
        self.assertRedirects(response, "/songs")
        self.assertTrue(
            Song.objects.filter(song_name="Numb", artist_name="Linkin Park").exists()
        )

    def test_delete(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(f"/songs/delete/{self.song.id}")
        self.assertRedirects(response, "/songs")
        self.assertFalse(
            Song.objects.filter(
                song_name="Test Song", artist_name="Test Artist"
            ).exists()
        )
