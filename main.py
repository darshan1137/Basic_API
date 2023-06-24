from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), unique=True, nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

# with app.app_context():
#     db.create_all()

@app.route('/')
def home():
    return "<h1>Hello! Welcome to my Web App</h2>" \
           "<p> Check '/test' for the endpoint to read the Word from DB </p>" \
           "<p>Go to '/change?text=example' for changing the Word</p>"


@app.route("/test")
def test():
    reply = db.session.query(Test).get(1)
    return jsonify(reply.to_dict()), 200

@app.route("/change", methods=["POST", "GET"])
def change():
    new_text = request.args.get("text")
    test = db.session.query(Test).get(1)
    if test:
        test.text = new_text
        db.session.commit()
        return jsonify(response={"Success": "Value updated successfully"}), 200
    else:
        return jsonify(response={"Failed": "Database Error"}), 404



if __name__ == "__main__":
    app.run(debug=True)