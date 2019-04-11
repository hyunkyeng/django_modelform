from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# import hashlib
from .models import Board, Comment
from .forms import BoardForm, CommentForm

# Create your views here.
def index(request):
    # if request.user.is_authenticated:
    #     gravatar_url = hashlib.md5(request.user.email.strip().lower().encode('utf-8')).hexdigest()
    # else:
    #     gravatar_url = None
    boards = get_list_or_404(Board.objects.order_by('-pk'))
    context = {
        'boards':boards,
        # 'gravatar_url': gravatar_url,
    }
    return render(request, 'boards/index.html', context)

@login_required
def create(request):
    # POST 요청이면 FORM 데이터를 처리한다.
    if request.method == 'POST':
        # 이 처리과정은 "binging" 으로 불리는데, 폼의 유효성 체크를 할 수 있도록 해준다
        form = BoardForm(request.POST)
        # form 유효성 체크
        if form.is_valid():
            # title = form.cleaned_data.get('title')
            # content = form.cleaned_data.get('content')
            # 검증을 통과한 깨끗한 데이터를 form에서 가져와서 coard를 만든다.
            
            # board 를 바로 저장하지 않고, 현재 user를 넣고 저장
            # 실제 DB에 반영 전까지의 단계를 진행하고, 그 중간에 user 정보를 request.user에서 가져와서 그 후에 저장한다. 
            # board = Board.objects.create(title=title, content=content)
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect('boards:detail', board.pk)
    # GET요청 ( 혹은 다른 메서드)이면 기본 폼을 생성한다.
    else:
        form = BoardForm()
    context = {'form':form}
    return render(request, 'boards/form.html', context)
        
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    comment_form = CommentForm()
    context = {
        'board':board,
        'comment_form':comment_form,
    }
    return render(request, 'boards/detail.html', context)
    
def delete(requsest, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if requsest.method == 'POST':
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:index')
        
@login_required
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            form = BoardForm(request.POST, instance=board)  #1
            if form.is_valid():
                board = form.save()                         #2
                return redirect('boards:detail', board.pk)
        # GET 요청이면(수정하기 버튼을 눌렀을 때)
        else:
            # BoardForm 을 초기화(사용자 입력 값을 넣어준 상태로)
            # form = BoardForm(initial={'title': board.title, 'content': board.content})
            form = BoardForm(instance=board)                #3
        # 1. POST : 요청에서 검증에 실패하였을때, 오류 메세지가 포함된 상태
        # 2. GET : 요청에서 초기화된 상태
    else:
        return redirect('boards:index')
    context = {
        'form': form,
        'board': board,
    }
    return render(request, 'boards/form.html', context)
    
    
@require_POST
@login_required
def comment_create(request, board_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.board_id = board_pk
        comment.save()
    return redirect('boards:detail', board_pk)
    

@require_POST
@login_required
def comment_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('boards:detail', board_pk)
    