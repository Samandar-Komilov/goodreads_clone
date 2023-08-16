from django.test import TestCase
from django.urls import reverse
from .models import Book


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        Book.objects.create(title="Book1", description="desc1", isbn="123123")
        Book.objects.create(title="Book2", description="desc2", isbn="123124")
        Book.objects.create(title="Book3", description="desc3", isbn="123125")

        response = self.client.get(reverse("books:list"))

        books = Book.objects.all()
        # response ichida bazadagi barcha kitoblar bor yoki yoqligini check qilish
        for book in books:
            self.assertContains(response, book.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123")

        # reverse uchun /books/detail bo'lib qoladi, buni fix uchun kwargs ishlatamiz
        response = self.client.get(reverse("books:detail", kwargs={"id":book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)