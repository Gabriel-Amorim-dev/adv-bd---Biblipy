from django.contrib import admin
from django.db import models
from .models import Author, Category, Book


class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = (
        'title',
        'isbn',
        'publisher',
        'publication_year',
        'category',
        'quantity',
        'available'
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'isbn',
        'quantity',
        'available',
        'is_low_stock'
    )
    list_display_links = ('title',)
    list_editable = ('quantity', 'available')
    autocomplete_fields = ['author', 'category']
    search_fields = ('title', 'isbn', 'author__name')
    list_filter = ('available', 'category', 'publication_year')
    date_hierarchy = 'created_at'

    @admin.display(boolean=True, description='Low Stock?')
    def is_low_stock(self, obj):
        return obj.quantity < 3


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'book_count')
    search_fields = ('name',)
    inlines = [BookInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _book_count=models.Count('books')
        )

    @admin.display(description='Total Books')
    def book_count(self, obj):
        return obj._book_count


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)