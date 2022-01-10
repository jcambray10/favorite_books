from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html', {"user": User.objects.all()})

def all_books(request):
    if 'user' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    context = {
        'all_books': Book.objects.all(),
        'this_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'books/all_books.html', context)

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
        request.session['greeting'] = user.first_name
        request.session['user_id'] = user.id
        return redirect('/books')
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)

    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if logged_user.password == request.POST['password']:
            request.session['greeting'] = logged_user.first_name
            request.session['user_id'] = logged_user.id
            return redirect('/books')
    return redirect('/')

def logout(request):
    # print(request.session)
    request.session.flush()
    # print(request.session)
    return redirect('/')

def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')

def create_book(request):
    errors = Book.objects.book_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        user = User.objects.get(id=request.session["user_id"])
        book = Book.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            creator = user
        )
        user.favorited_books.add(book)

        return redirect(f'/books/{book.id}')

def show_one(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "books/one_book.html", context)

def update(request, book_id):
    book = Book.objects.get(id=book_id)
    book.description = request.Post['description']
    book.save()
    return redirect(f"/books/{book_id}")

def like(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.liked_books.add(book)

    return redirect(f'/books/{book_id}')

def unlike(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.liked_books.remove(book)

    return redirect(f'/books/{book_id}')


# echo "# favorite_books" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/jcambray10/favorite_books.git
# git push -u origin main
