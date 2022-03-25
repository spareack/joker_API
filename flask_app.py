from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_num = db.Column(db.Integer)
    name = db.Column(db.String, default="Unknown")
    score = db.Column(db.String, default=0)


@app.route("/register_new_user", methods=['POST'])
def register_new_user():
    try:
        data = request.json
        player = Player(name=data['name'], actor_num=data['actor_num'])
        db.session.add(player)
        db.session.commit()

        return jsonify({"status": 0})

    except Exception as e:
        return jsonify({"status": 1, "info": str(e)})


@app.route("/get_rating", methods=['POST', 'GET'])
def get_rating():
    try:
        all_players = db.session.query(Player).order_by(Player.score.desc()).all()
        response = list({"name": player.name, "score": player.score} for player in all_players)

        return jsonify({"status": 0, "players": response})

    except Exception as e:
        return jsonify({"status": 1, "info": str(e)})


@app.route("/change_rating", methods=['POST'])
def change_rating():
    try:
        data = request.json
        players_list = data["players"]

        for player_data in players_list:
            player = db.session.query(Player).filter_by(actor_num=player_data['actor_num']).first_or_404()
            player.score += player['score_change']

        db.session.commit()
        return jsonify({"status": 0})

    except Exception as e:
        return jsonify({"status": 1, "info": str(e)})


@app.route("/change_name", methods=['POST'])
def change_name():
    try:
        data = request.json
        player = db.session.query(Player).filter_by(actor_num=data['actor_num']).first_or_404()
        player.name = data['new_name']
        db.session.commit()
        return jsonify({"status": 0})

    except Exception as e:
        return jsonify({"status": 1, "info": str(e)})
