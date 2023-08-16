from django.shortcuts import render
from django.views import View
from .models import Book

def landing_page(request):
    # We can manage cookies like sessionid, csrftoken and many more
    print(f"Session ID: {request.COOKIES['sessionid']}")
    return render(request, "landing.html")


class BookView(View):
    def get(self, request):
        books = Book.objects.all()

        return render(request, "books/list.html", {"books":books})


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)

        return render(request, "books/detail.html", {'book':book})