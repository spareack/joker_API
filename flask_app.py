from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_num = db.Column(db.String)
    name = db.Column(db.String, default="Unknown")
    score = db.Column(db.Integer, default=0)
    clan_id = db.Column(db.Integer, default=-1)


class Clan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="Unknown_clan")
    description = db.Column(db.String, default="None")

    def get_clan_score(self):
        all_members = db.session.query(Player).filter_by(clan_id=id).all()
        return sum(member.score for member in all_members)


@app.route("/get_clan", methods=['POST'])
def get_clan():
    try:
        data = request.json
        clan = db.session.query(Clan).filter_by(id=data['clan_id']).first_or_404()

        return jsonify({"status": 0,
                        "clan_name": clan.name,
                        "description": clan.description,
                        "clan_score": clan.get_clan_score()})

    except Exception as e:
        return jsonify({"status": 1, "info": str(e)})


@app.route("/join_clan", methods=['POST'])
def join_clan():
    try:
        data = request.json
        player = db.session.query(Player).filter_by(actor_num=data['actor_num']).first_or_404()
        player.clan_id = data['clan_id']
        db.session.commit()

        return jsonify({"status": 0})

    except Exception as e:
        return jsonify({"status": 1, "info": str(e)})


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
            player.score += player_data['score_change']

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
