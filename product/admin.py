from django.contrib import admin
from .models import Product, Comment


class CommentadminInLine(admin.TabularInline):
    model = Comment
    fields = ['id', 'body',]
    extra = 0


class productadmin(admin.ModelAdmin):
    list_display = ['id','name']
    inlines = [CommentadminInLine, ]

class Commentadmin(admin.ModelAdmin):
    list_display = ['body',]


admin.site.register(Product,productadmin)
admin.site.register(Comment,Commentadmin)

