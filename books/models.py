from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower_name = models.CharField(max_length=255)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower_name} - {self.book.title}"
