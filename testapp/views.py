


# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Board,Topic

from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from django.db.models import Count, Max
from django.contrib.auth.decorators import login_required

def home(request):
    boards = Board.objects.annotate(
        num_topics=Count('topics'),
        num_posts=Count('topics__posts'),
        last_post=Max('topics__posts__created_at')
    )
    return render(request, 'home.html', {'boards': boards})



@login_required
def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    topics = board.topics.select_related('created_by').all()

    for topic in topics:
        topic.num_posts = topic.posts.count()
        last_post = topic.posts.order_by('-created_at').first()
        topic.last_post_date = last_post.created_at if last_post else None

    return render(request, 'board_topics.html', {'board': board, 'topics': topics})

from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        topic = Topic.objects.create(subject=subject, board=board, created_by=request.user)
        Post.objects.create(message=message, topic=topic, created_by=request.user)

        return redirect('board_topics', board_id=board.pk)
    return render(request, 'new_topic.html', {'board': board})

def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, pk=topic_id)
    posts = topic.posts.order_by('-created_at')
    return render(request, 'topic_posts.html', {'topic': topic, 'posts': posts})




# boards/views.py
@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, pk=topic_id)
    if request.method == 'POST':
        message = request.POST['message']
        Post.objects.create(message=message, topic=topic, created_by=request.user)
        return redirect('topic_posts', board_id=board_id, topic_id=topic_id)
    return render(request, 'reply_topic.html', {'topic': topic})
