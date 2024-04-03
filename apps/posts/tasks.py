from system.celery import app
from apps.posts.models import Post
from datetime import datetime


@app.task()
def mark_outdated_posts_as_inactive():
    outdated_posts = Post.objects.filter(end_date__lte=datetime.now())
    if not outdated_posts.exists():
        return
    outdated_posts.update(active=False)
