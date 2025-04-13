from flask_openapi3 import Info, Tag, OpenAPI
from flask import request, jsonify
from flask_cors import CORS
from models import ReviewInput, ReviewLikeRequest, GameNameQuery
from datetime import datetime
import sqlite3

info = Info(title="Review", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

review_tag = Tag(name="Reviews", description="Reviews de jogos")

def get_db_connection():
    conn = sqlite3.connect('API/review.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        game_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        review TEXT NOT NULL,
        likes INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

create_table()

@app.post(
    "/reviews",
    tags=[review_tag],
    summary="Posta uma review para um jogo.",
    responses={
        201: {
            "description": "Review adicionada com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Review adicionada com sucesso!"
                    }
                }
            }
        }
    }
)
def post_review(body: ReviewInput):
    username = body.username
    game_name = body.game_name
    rating = body.rating
    review = body.review

    print(f"Inserindo review - Usuário: {username}, Jogo: {game_name}, Nota: {rating}, Review: {review}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (username, game_name, rating, review)
        VALUES (?, ?, ?, ?)
    """, (username, game_name, rating, review))

    conn.commit()

    cursor.execute("SELECT * FROM reviews WHERE username = ? AND game_name = ?", (username, game_name))
    inserted_review = cursor.fetchone()
    print(f"Review inserida: {inserted_review}")

    conn.close()

    return {"message": "Review adicionada com sucesso!"}, 201

# GET - Reviews de um jogo
@app.get("/review", tags=[review_tag], summary="Obtém todas as reviews de um jogo.", responses={
    200: {
        "description": "Lista de reviews do jogo.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "username": "Joao",
                        "game_name": "Final Fantasy",
                        "review": "Muito bom!",
                        "likes": 2,
                        "created_at": "2024-04-12T12:34:56"
                    }
                ]
            }
        }
    }
})
def get_reviews(query: GameNameQuery):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM reviews WHERE game_name = ? ORDER BY created_at DESC
    ''', (query.game_name,))
    reviews = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in reviews]), 200

@app.put("/review/like", tags=[review_tag], summary="Adiciona um like para uma review de um jogo de um usuário.", responses={
    200: {
        "description": "Like adicionado com sucesso.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Like adicionado com sucesso!"
                }
            }
        }
    },
    404: {
        "description": "Review não encontrada.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Review não encontrada!"
                }
            }
        }
    }
})
def like_review(body: ReviewLikeRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM reviews WHERE game_name = ? AND username = ?
    ''', (body.game_name, body.username))
    
    review = cursor.fetchone()

    if review is None:
        conn.close()
        return jsonify({"message": "Review não encontrada!"}), 404

    cursor.execute('''
        UPDATE reviews SET likes = likes + 1 WHERE game_name = ? AND username = ?
    ''', (body.game_name, body.username))
    conn.commit()
    conn.close()
    return jsonify({"message": "Like adicionado com sucesso!"}), 200

# GET - Últimas 20 reviews
@app.get("/review/last", tags=[review_tag], summary="Obtém as 20 últimas reviews feitas.", responses={
    200: {
        "description": "Últimas 5 reviews.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 7,
                        "username": "Ana",
                        "game_name": "Celeste",
                        "review": "Desafiador e emocionante.",
                        "likes": 5,
                        "created_at": "2024-04-12T22:10:00"
                    }
                ]
            }
        }
    }
})
def get_last_reviews():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM reviews ORDER BY created_at DESC LIMIT 20
    ''')
    reviews = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in reviews]), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)