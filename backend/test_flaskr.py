import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

database_name = "trivia"
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'L3g3nd%40ry',
                                                'localhost:5432', database_name)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = database_path
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        print(self.database_path)
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_category_method_not_allowed(self):
        print(self.database_path)
        res = self.client().post("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error_code'], 405)
        self.assertTrue(data['message'])
        self.assertTrue(not data['success'])

    def test_get_questions(self):
        print(self.database_path)
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])

    def test_search_questions(self):
        print(self.database_path)
        res = self.client().post("/questions", json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])

    def test_search_questions_not_found(self):
        print(self.database_path)
        res = self.client().post("/questions", json={"searchTerm": "kiki"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error_code'], 404)
        self.assertTrue(data['message'])
        self.assertTrue(not data['success'])

    def test_delete_question(self):
        print(self.database_path)
        res = self.client().delete("/questions/4")

        self.assertEqual(res.status_code, 200)

    def test_delete_question_not_found(self):
        print(self.database_path)
        res = self.client().delete("/questions/4")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error_code'], 404)
        self.assertTrue(data['message'])
        self.assertTrue(not data['success'])

    def test_get_questions_by_category(self):
        print(self.database_path)
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])

    def test_get_quizzes(self):
        print(self.database_path)
        res = self.client().post("/quizzes", json={"previous_questions": [1, 2, 3], "quiz_category": {'type': 'sport', 'id': 6}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_get_quizzes_bad_request(self):
        print(self.database_path)
        res = self.client().post("/quizzes", json={"previous_questions": [1, 2, 3]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error_code'], 400)
        self.assertTrue(data['message'])
        self.assertTrue(not data['success'])

    def test_create_questions(self):
        print(self.database_path)
        res = self.client().post("/questions", json={
            "question": "when did Queen ELizabeth die?",
            "answer": "2022",
            "category": "4",
            "difficulty": "2"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])

        def test_create_questions_bad_request(self):
            print(self.database_path)
            res = self.client().post("/questions", json={
                "question": "when did Queen ELizabeth die?",
                "answer": "2022",
                "category": "4",
                "difficult": "2"
            })
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['error_code'], 400)
            self.assertTrue(data['message'])
            self.assertTrue(not data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
