from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)
app.config['SECRET_KEY'] = 'slavisaneo'

#bootstrap flask extension
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, default=False, server_default="false")
    has_wifi = db.Column(db.Boolean, default=False, server_default="false")
    has_sockets = db.Column(db.Boolean, default=False, server_default="false")
    can_take_calls = db.Column(db.Boolean, default=False, server_default="false")
    coffee_price = db.Column(db.String(250), nullable=True)


# db.create_all()

#WTform

class CafeForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    has_toilet = StringField("Is there any toilet", validators=[DataRequired()])
    has_wifi = StringField("Have you found WIFI spot", validators=[DataRequired()])
    has_sockets = StringField("Is there any sockets", validators=[DataRequired()])
    can_take_calls = StringField("Can you take calls", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Add")


#home page with a little bit decor :)
@app.route("/")
def home():
    return render_template("index.html")


#render all cafes from database
@app.route("/cafes")
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template("cafes.html", all_posts=all_cafes)


#more details about cafe
@app.route("/info/<int:index>")
def info(index):
    data_id = index
    cafe = Cafe.query.get(data_id)

    return render_template("info.html", post=cafe)


#wtflask form to add new cafe into database with add button, all fields must be filled out
@app.route("/add", methods=["GET", "POST"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=bool(form.has_toilet.data),
            has_wifi=bool(form.has_wifi.data),
            has_sockets=bool(form.has_sockets.data),
            can_take_calls=bool(form.can_take_calls.data),
            coffee_price=form.coffee_price.data
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


#delete cafe from database
@app.route("/delete")
def delete():
    delete_id = request.args.get("index")
    delete_data = Cafe.query.get(delete_id)
    db.session.delete(delete_data)
    db.session.commit()
    return redirect(url_for("cafes"))


#edit some precise fields(name,has_sockets,coffee_price)
@app.route("/edit", methods=["GET", "POST"])
def edit():

    edit_id = request.args.get("index")
    cafe_to_edit = Cafe.query.get(edit_id)
    edit_form = CafeForm(
        name=cafe_to_edit.name,
        map_url=cafe_to_edit.map_url,
        img_url=cafe_to_edit.img_url,
        location=cafe_to_edit.location,
        seats=cafe_to_edit.seats,
        has_toilet=bool(cafe_to_edit.has_toilet),
        has_wifi=bool(cafe_to_edit.has_wifi),
        has_sockets=bool(cafe_to_edit.has_sockets),
        can_take_calls=bool(cafe_to_edit.can_take_calls),
        coffee_price=cafe_to_edit.coffee_price
    )
    if edit_form.validate_on_submit():
        cafe_to_edit.name = edit_form.name.data
        cafe_to_edit.has_sockets = bool(edit_form.has_sockets.data)
        cafe_to_edit.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for("cafes"))

    return render_template("add.html", form=edit_form)


#filter only sockets cafe places
@app.route("/sockets")
def sockets():
    soc_post = Cafe.query.filter_by(has_sockets=1).all()
    print(soc_post.name)
    return render_template("cafes.html", all_posts=soc_post)


#filter only wifi cafe places
@app.route("/wifi")
def wifi():
    wifi_post = Cafe.query.filter_by(has_wifi=1).all()
    return render_template("cafes.html", all_posts=wifi_post)


#filter only toilet cafe places
@app.route("/toilet")
def toilet():
    toilet_post = Cafe.query.filter_by(has_toilet=1).all()
    return render_template("cafes.html", all_posts=toilet_post)


#filter only cafe places that can take calls
@app.route("/can-take")
def can_take():
    can_take_post = Cafe.query.filter_by(can_take_calls=1).all()
    return render_template("cafes.html", all_posts=can_take_post)


if __name__ == '__main__':
    app.run(debug=True)
