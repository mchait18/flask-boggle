from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_page(self):
        with self.client as client:
            res= client.get('/')
            html = res.get_data(as_text=True)
           
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle</h1>', html)
            self.assertIn('Seconds Left:', html)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn('board', session)
           
    def test_invalid_word(self):
        """Test if word is on the board"""
        self.client.get('/')
        resp = self.client.get('/check-word?word=impossible')
        self.assertEqual(resp.json['result'], 'not-on-board')

    def non_English_word(self):
        """Test if word is in the dictionary"""
        self.client.get('/')
        response = self.client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')

    

