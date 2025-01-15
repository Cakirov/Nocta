from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from blog.models import Post, Category, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from blog.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View

def index(request):
    return render(request, 'index.html')
# Create your views here.

def index(request):
    context = dict()
    post_list = Post.objects.all()

    query = request.GET.get('q')

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(user__first_name__icontains=query)
        ).distinct()
        
    paginator = Paginator(post_list, 9) # bir sayfada kaç tane görünmesi gerek
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    
    context['posts'] = posts
    context['post_list'] = Post.objects.distinct()
    context['cat'] = Category.objects.all()
    context['popular_list'] = Post.objects.all().order_by('-read', '-id')[:3]

    
    #   pagination, search
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post=post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    
    read = post.read
    read += 1
    degis = Post.objects.filter(slug=slug).update(read=read)

    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'detail.html', context)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form  = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'forms.html', {'form': form})

@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('detail', pk = comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.delete()
    return redirect('detail', pk = comment.post.pk)


def category_show(request, category_slug):
    context = dict()
    context['category'] = get_object_or_404(
        Category, slug=category_slug,
    )

    context['items'] = Post.objects.filter(
        category=context['category'],
    )

    return render(request, 'category_show.html', context)

def contact_view(request):
    return render(request, 'contact.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'register.html')
            
        # Create user if username is available
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except:
            messages.error(request, 'Registration failed. Please try again.')
            return render(request, 'register.html')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Kullanıcıyı doğrula
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Kullanıcıyı oturum aç
            messages.success(request, 'Giriş başarılı! Ana sayfaya yönlendiriliyorsunuz.')
            return redirect('index')  # Giriş sonrası ana sayfaya yönlendir
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')

    return render(request, 'login.html')

def search_results(request):
    query = request.GET.get('q')
    results = Post.objects.filter(title__icontains=query) if query else Post.objects.none()
    context = {
        'results': results,
        'query': query,
        'cat': Category.objects.all(),
        'popular_list': Post.objects.all().order_by('-read', '-id')[:9]
    }
    return render(request, 'search_results.html', context)

def page_view(request):
    return render(request, 'page.html')  # page.html dosyasını render et

def category_view(request):
    # You can add any context data you want to pass to the template here
    return render(request, 'category.html')  # Ensure this points to your category.html file

