# coding: utf8

from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.models import User, Userlog, Preview, Tag, Movie, Comment, Moviecol
from app.home.forms import RegisterForm, LoginForm, UserDetailForm, PwdForm, CommentForm
from app import db, app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import uuid
from sqlalchemy import or_
import os
import datetime


def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex + fileinfo[-1])
    return filename


@home.route("/<int:page>/", methods=["GET"])
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query

    tid = request.args.get("tid", 0)
    if int(tid) != 0:
        page_data=page_data.filter_by(tag_id=int(tid))

    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data=page_data.filter_by(star=int(star))

    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time)==1:
            page_data=page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data=page_data.order_by(
                Movie.addtime.asc()
            )

    pm = request.args.get("pm", 0)
    if int(pm) != 0:
        if int(pm)==1:
            page_data=page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data=page_data.order_by(
                Movie.playnum.asc()
            )

    cm = request.args.get("cm", 0)
    if int(cm) != 0:
        if int(cm)==1:
            page_data=page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data=page_data.order_by(
                Movie.commentnum.asc()
            )
    if page is None:
        page=1
    page_data=page_data.paginate(page=page, per_page=10)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    return render_template("home/index.html", tags=tags, p=p, page_data=page_data)


@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter(or_(User.name==data["account"], User.phone==data["account"],User.email==data["account"])).first()
        if not user.check_pwd(data["pwd"]):
            flash("Wrong Password", "err")
            return redirect(url_for("home.login"))
        session["user"] = user.name
        session["user_id"] = user.id

        userlog = Userlog (
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))


@home.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["username"],
            email=data["email"],
            pwd=generate_password_hash(data["pwd"]),
            phone=data["phone"],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("Successfully added", "ok")
    return render_template("home/register.html", form=form)


@home.route("/user/", methods=["GET", "POST"])
@user_login_req
def user():
    form = UserDetailForm()
    user = User.query.get(int(session["user_id"]))
    form.avatar.validators = []
    form.info.validators = []
    if request.method == "GET":
        form.username.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])
            os.chmod(app.config["FC_DIR"], "rw")

        if form.avatar.data.filename != "":
            file_avatar = secure_filename(form.avatar.data.filename)
            user.avatar = change_filename(file_avatar)
            form.avatar.data.save(app.config["FC_DIR"] + user.avatar)

        name_count = User.query.filter_by(name=data["username"]).count()
        if data["username"] != user.name and name_count == 1:
            flash("Username is already in use.", "err")
            return redirect(url_for("home.user"))
        user.name = data["username"]

        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("Email address is already in use.", "err")
            return redirect(url_for("home.user"))
        user.email = data["email"]

        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("Phone number is already in use.", "err")
            return redirect(url_for("home.user"))

        user.phone = data["phone"]
        print(user.phone)
        user.info = data["info"]
        db.session.add(user)
        db.session.commit()
        flash("Successfully changed", "ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)


@home.route("/pwd/", methods=["GET","POST"])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session["user"]).first()
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash("Successfully changed", "ok")
        return redirect(url_for("home.login"))
    return render_template("home/pwd.html", form=form)


@home.route("/comments/<int:page>/", methods=["GET", "POST"])
@user_login_req
def comments(page= None):
    if page is None:
        page = 1
    page_data = Comment.query.join(User).filter(
        User.id == session["user_id"]
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/comments.html", page_data=page_data)


@home.route("/loginlog/<int:page>/", methods=["GET"])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.filter_by(
        user_id = int(session["user_id"])
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/loginlog.html", page_data = page_data)


@home.route("/moviecol/add/", methods=["GET"])
@user_login_req
def moviecol_add():
    uid = request.args.get("uid", "")
    mid = request.args.get("mid", "")
    moviecol = Moviecol.query.filter_by(
        user_id = int(uid),
        movie_id = int(mid)
    ).count()
    if moviecol == 1:
        data = dict(ok=0)

    if moviecol == 0:
        moviecol = Moviecol(
            user_id=int(uid),
            movie_id=int(mid)
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    import json
    return json.dumps(data)


@home.route("/moviecol/<int:page>/", methods=["GET"])
@user_login_req
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(Movie).filter(
        Movie.id == Moviecol.movie_id,
        Moviecol.user_id == int(session["user_id"])
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/moviecol.html", page_data=page_data)


@home.route("/animation/")
def animation():
    data = Preview.query.all()
    return render_template("home/animation.html", data=data)


@home.route("/search/<int:page>", methods=["GET"])
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    movie_count = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).count()
    page_data = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template("home/search.html", key=key, page_data=page_data, movie_count=movie_count)


@home.route("/play/<int:id>/<int:page>", methods=["GET","POST"])
def play(id = None, page=None):
    movie = Movie.query.join(Tag).filter(
        Movie.tag_id == Tag.id,
        Movie.id == int(id)
    ).first_or_404()
    if page is None:
        page = 1
    page_data = Comment.query.join(User).join(Movie).filter(
        Movie.id == movie.id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    movie.playnum = movie.playnum + 1
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data["content"],
            user_id=session["user_id"],
            movie_id=movie.id
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash("Successfully Added", "ok")
        return redirect(url_for('home.play', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template("home/play.html", movie=movie, form=form, page_data=page_data)
