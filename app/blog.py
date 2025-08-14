from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from pywebpush import webpush, WebPushException
from werkzeug.exceptions import abort
from .auth import login_required
from .models import db, Post, User
import os, json
from datetime import datetime

bp = Blueprint('blog', __name__, static_folder='static')
VAPID_PUBLIC_KEY = os.environ.get("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY")
SUBSCRIPTION_FILE = "subscriptions.json"
API_KEY_BLAST = os.environ.get("API_KEY_BLAST")

@bp.route('/worker.js')
def worker():
    return bp.send_static_file('js/worker.js')

@bp.route('/subscribe', methods=['POST'])
def subscribe():
    subscription_info = request.get_json()

    # Load existing subscriptions
    if os.path.exists(SUBSCRIPTION_FILE):
        with open(SUBSCRIPTION_FILE, "r") as f:
            subscriptions = json.load(f)
    else:
        subscriptions = []

    if subscription_info not in subscriptions:
        subscriptions.append(subscription_info)
        with open(SUBSCRIPTION_FILE, "w") as f:
            json.dump(subscriptions, f, indent=2)

    return "Subscribed", 201

@bp.route('/blast', methods=['POST'])
def blast():
    if request.headers.get("X-API-Key") != API_KEY_BLAST:
        return "Unauthorized", 401

    if not os.path.exists(SUBSCRIPTION_FILE):
        return "No subscribers", 404

    with open(SUBSCRIPTION_FILE, "r") as f:
        subscriptions = json.load(f)

    message = {
        "title": 'Push Notification',
        "message": "This is a test message from Flask app.",
        "data": {"url": "https://www.google.com"},
    }

    dead_subs = []
    success_count = 0
    tmp_count = 0
    for sub in subscriptions:
        status = send_web_push(sub, message)
        if status == "dead":
            dead_subs.append(sub)
        elif status == "ok":
            success_count += 1
        elif status == "temporary":
            tmp_count += 1

    if dead_subs:
        subscriptions = [s for s in subscriptions if s not in dead_subs]
        with open(SUBSCRIPTION_FILE, "w") as f:
            json.dump(subscriptions, f, indent=2)

    return f"Broadcast {success_count} sent. Skip {tmp_count} temporary offline. Removed {len(dead_subs)} dead subscribers.", 200


def send_web_push(subscription_information, message_body):
    try:
        webpush(
            subscription_info=subscription_information,
            data=json.dumps(message_body),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:you@email.com"},
            ttl=14400  # ⏳ 4 jam
        )
        return "ok"

    except WebPushException as ex:
        print(f"Push failed: {repr(ex)}")
        if "410" in str(ex) or "404" in str(ex):
            print("Subscriber invalid, akan dihapus.")
            return "dead"
        print("Error sementara, subscriber tetap disimpan.")
        return "temporary"

@bp.route('/')
def index():
    posts = Post.query.join(User).add_columns(
        Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username
    ).order_by(Post.created.desc()).all()

    return render_template('blog/index.html', posts=posts, vapid_public_key=VAPID_PUBLIC_KEY)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            new_post = Post(
                title=title,
                body=body,
                author_id=g.user.id,
                created=datetime.utcnow()
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = Post.query.join(User).add_columns(
        Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username
    ).filter(Post.id == id).first()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Post.query.get_or_404(id)

    if check_post_author(post):
        abort(403)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            flash('Title is required.')
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.query.get_or_404(id)

    if check_post_author(post):
        abort(403)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))

def check_post_author(post):
    return post.author_id != g.user.id
