from django.contrib import admin
from .models import Borrow
from datetime import date
import csv
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse


class LibraryAdminSite(admin.AdminSite):

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['stats'] = {
            'total_borrows': Borrow.objects.count(),
            'active_borrows': Borrow.objects.filter(status='pending').count(),
            'late_borrows': Borrow.objects.filter(status='late').count(),
            'returned_borrows': Borrow.objects.filter(status='returned').count(),
        }
        return super().index(request, extra_context)

# export functions

def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="borrows.csv"'
    writer = csv.writer(response)
    writer.writerow(['User', 'Book', 'Borrow Date', 'Due Date', 'Status'])
    for borrow in queryset:
        writer.writerow([borrow.user, borrow.book, borrow.borrow_date, borrow.due_date, borrow.status])
    return response
def export_excel(modeladmin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Borrows"
    ws.append(['User', 'Book', 'Borrow Date', 'Due Date', 'Status'])
    for borrow in queryset:
        ws.append([str(borrow.user), str(borrow.book), str(borrow.borrow_date), str(borrow.due_date), borrow.status])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="borrows.xlsx"'
    wb.save(response)
    return response


def export_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="borrows.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    style_n = styles['Normal']  # Style for wrapped text

    # Header row
    data = [['User', 'Book', 'Borrow Date', 'Due Date', 'Status']]

    for borrow in queryset:
        # Wrap long text (user and book) using Paragraph
        data.append([
            Paragraph(str(borrow.user), style_n),
            Paragraph(str(borrow.book), style_n),
            str(borrow.borrow_date),
            str(borrow.due_date),
            borrow.get_status_display()  # Use this for prettier names (e.g., 'PENDING')
        ])

    # Define fixed column widths (total ~540 points for Letter size)
    # User (120), Book (220), Dates (70 each), Status (60)
    table = Table(data, colWidths=[120, 220, 70, 70, 60])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align text to top of cell
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    doc.build(elements)
    return response

export_csv.short_description = "Export selected as CSV"
export_excel.short_description = "Export selected as Excel"
export_pdf.short_description = "Export selected as PDF"

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'book',
        'borrow_date',
        'due_date',
        'return_date',
        'status',
        'is_overdue_colored'
    )

    list_filter = ('status', 'borrow_date', 'due_date')

    search_fields = (
        'user__username',
        'user__registration_number',
        'book__title',
        'book__isbn'
    )

    actions = ['mark_as_returned', export_excel, export_pdf, export_csv]
    date_hierarchy = 'borrow_date'
    autocomplete_fields = ['user', 'book']

    @admin.display(description='Overdue?', boolean=True)
    def is_overdue_colored(self, obj):
        if obj.status != 'returned' and obj.due_date < date.today():
            return True
        return False

    def mark_as_returned(self, request, queryset):
        count = 0
        for borrow in queryset.filter(status__in=['pending', 'late']):
            borrow.status = 'returned'
            borrow.save()
            count += 1

        self.message_user(request, f"{count} books have been marked as returned.")

    mark_as_returned.short_description = "Mark selected as Returned"


