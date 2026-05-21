import pandas as pd

def get_books_dataframe(queryset):
    data = queryset.values(
        'title',
        'author__name',
        'category__name',
        'isbn',
        'quantity',
        'available',
    )
    df = pd.DataFrame(list(data))
    if df.empty:
        return df
    df.columns = ['Title', 'Author', 'Category', 'ISBN', 'Quantity', 'Available']
    return df