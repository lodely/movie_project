#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
import os

from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app import app
from app.admin.base import admin_login_req, change_filename
from app.admin.form.forms import MovieForm, EditMovieForm
from app.models import Tags, Movie, db

from app.admin import admin

# 添加电影
@admin.route("/movie/add", methods=['GET', 'POST'])
@admin_login_req
def movie_add():
    form = MovieForm()

    # 查询数据库标签并赋值给表单，此方法可以实时同步数据库的标签数据
    # 避免新添加的标签无法显示
    form.tag_id.choices = Tags.get_all_tags()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            # 若已经存在则不再添加
            if Movie.query.filter(or_(Movie.logo==data['logo'], Movie.url==data['url'],Movie.title==data['title'])).all():
                flash("电影已经存在，请不要重复添加", "err")
            else:
                with db.auto_commit():
                    file_url = secure_filename(form.url.data.filename)
                    file_logo = secure_filename(form.logo.data.filename)
                    if not os.path.exists(app.config["UP_DIR"]):
                        os.makedirs(app.config["UP_DIR"])
                        os.chmod(app.config["UP_DIR"], "rw")

                    url = change_filename(file_url)
                    logo = change_filename(file_logo)
                    form.url.data.save(app.config["UP_DIR"]+url)
                    form.logo.data.save(app.config["UP_DIR"]+logo)
                    new_movie = Movie(
                        title=data['title'],
                        url=url,
                        logo=logo,
                        info=data['info'],
                        star=int(data['star']),
                        tag_id=int(data['tag_id']),
                        area=data['area'],
                        release_time=data['release_time'],
                        length=data['length']
                    )
                    db.session.add(new_movie)
                flash("电影添加成功", "ok")
                return redirect(url_for("admin.movie_add"))
        else:
            flash("电影添加失败", 'err')
            return redirect(url_for("admin.movie_add"))
    return render_template("admin/movie_add.html", form=form)

# 电影列表
@admin.route("/movie/list/<int:page>", methods=['GET', 'POST'])
@admin_login_req
def movie_list(page=0):
    if not page:
        page = 1
    movies = Movie.get_ten_page(page=page)
    return render_template("admin/movie_list.html", movies=movies)

# 编辑电影
@admin.route("/movie/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def movie_edit(id=None):
    form = EditMovieForm()
    # 查询数据库标签并赋值给表单，此方法可以实时同步数据库的标签数据
    # 避免新添加的标签无法显示
    form.tag_id.choices = Tags.get_all_tags()

    movie = Movie.query.filter_by(id=id).first()

    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data

            with db.auto_commit():
                file_logo = secure_filename(form.logo.data.filename)
                if not os.path.exists(app.config["UP_DIR"]):
                    os.makedirs(app.config["UP_DIR"])
                    os.chmod(app.config["UP_DIR"], "rw")

                logo = change_filename(file_logo)
                form.logo.data.save(app.config["UP_DIR"]+logo)

                movie.title = data['title'],
                movie.logo = logo,
                movie.info = data['info'],
                movie.star = int(data['star']),
                movie.tag_id = int(data['tag_id']),
                movie.area = data['area'],
                movie.release_time = data['release_time'],
                movie.length = data['length']

                db.session.add(movie)
            flash("电影编辑成功", "ok")
            return redirect(url_for("admin.movie_edit", id=id))
        else:
            flash("电影编辑失败", 'err')
            return redirect(url_for("admin.movie_edit", id=id))

    return render_template("admin/movie_edit.html", form=form)

# 电影删除
@admin.route("/movie/del/<int:id>", methods=['GET'])
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.filter_by(id=id).first_or_404()
    if movie:
        with db.auto_commit():
            db.session.delete(movie)
        # flash("电影删除成功！", "ok")
        return redirect(url_for("admin.movie_list", page=1))
    return render_template("admin/movie_list.html")