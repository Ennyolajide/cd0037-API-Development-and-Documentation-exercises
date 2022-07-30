import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.

def get_formatted_books():
    books = Book.query.all()
    return [_.format() for _ in books]

def paginate(data, page = 1):
    start = ((page - 1) * BOOKS_PER_SHELF)
    end = (start + BOOKS_PER_SHELF)
    return data[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response

    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
    @app.route('/books', methods=['GET'])
    def get_books():
        formatted_data = get_formatted_books()
        page = request.args.get('page', 1, type=int)
        paginated_data = paginate(formatted_data, page)

        return jsonify({
            'success': True,
            'books': paginated_data,
            'total_books': len(formatted_data)
        })  


    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    @app.route('/books/<int:id>', methods=['PATCH'])
    def update_book(id):
        body = request.get_json()
        book = Book.query.get(id)
        book.rating = body.get('rating', 0)
        status = book.update() if book else False
        return jsonify({
            'success': status
        })  

    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh

    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'
    @app.route('/books/<int:id>', methods=['DELETE'])
    def delete_book(id): 
        book = Book.query.get(id)
        status = book.delete() if book else False 
        formatted_data = get_formatted_books()
        paginated_data = paginate(formatted_data)

        return jsonify({
            'success' : True,
            'deleted' : book.id,
            'books': paginated_data,
            'total_books': len(formatted_data)
        })
        


    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.

    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()
        book = Book(
            title = body.get('title', ''),
            author = body.get('author', ''),
            rating = body.get('rating', '')
        )
        status = book.insert()
        formatted_data = get_formatted_books()
        paginated_data = paginate(formatted_data)
        
        return jsonify({
            'success': status,
            'created': book.id,
            'books': paginated_data,
            'total_books': len(formatted_data)
        })

    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.

    

    return app
