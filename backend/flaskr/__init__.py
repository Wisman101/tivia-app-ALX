import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, object):
    start = (request.args.get("page", 1, type=int) - 1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return object[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route("/categories")
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()

        return jsonify({
            "categories": {category.id: category.type for category in categories}
        })


    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  
  @TODO:
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route("/questions", methods=["GET", "POST"])
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()

        if request.get_json():
            searchterm = request.get_json().get("searchTerm", None)
            if searchterm:
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(searchterm))).order_by(
                    Question.id).all()
            else:
                question = request.get_json().get("question", None)
                answer = request.get_json().get("answer", None)
                difficulty = request.get_json().get("difficulty", None)
                category = request.get_json().get("category", None)

                if not (question and difficulty and answer and category):
                    abort(400)

                new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                new_question.insert()

                questions = Question.query.order_by(Question.id).all()

        formated_questions = [question.format() for question in questions]
        paginate_questions(request, formated_questions)

        return jsonify({
            "questions": paginate_questions(request, formated_questions),
            "total_questions": len(questions),
            "categories": retrieve_categories().json['categories'],
            "current_category": "All"
        })
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()
        return jsonify({
            "success": True,
            "deleted": question_id
        })

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_category_questions(category_id):
        questions = Question.query.filter(Question.category == category_id).order_by(Question.id).all()

        formated_questions = [question.format() for question in questions]
        paginate_questions(request, formated_questions)

        return jsonify({
            "questions": paginate_questions(request, formated_questions),
            "total_questions": len(questions),
            "categories": retrieve_categories().json['categories'],
            "current_category": retrieve_categories().json['categories']["{}".format(category_id)]
        })
    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route("/quizzes", methods=["POST"])
    def play_game():
        previous_questions = request.get_json().get("previous_questions")
        category = request.get_json().get("quiz_category")

        if category['id'] == 0:
            questions = Question.query.order_by(Question.id).all()
        else:
            questions = Question.query.filter(Question.category == category['id']).order_by(Question.id).all()

        for question in questions:
            if question.id not in previous_questions:
                return jsonify({
                    "question": question.format()
                })

        return jsonify({
            "question": False
        })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error_code": 404,
            "message": "Resource Not Found",
            "success": False
        }), 404

    @app.errorhandler(405)
    def method_not_allow(error):
        return jsonify({
            "error_code": 405,
            "message": "Method Not Allowed",
            "success": False
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error_code": 400,
            "message": "Bad Request",
            "success": False
        }), 400

    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            "error_code": 422,
            "message": "unprocessable",
            "success": False
        }), 422

    return app
