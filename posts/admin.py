from django.contrib import admin

from .models import Post, Comment
from account.models import User

# class PostInLine(admin.TabularInline):
#     model = Post
#     fields = ['id']
#     extra = 1

class CommentAdmin(admin.ModelAdmin):
    list_display = [ 'id','text','created_time','updated_time']
    # inlines = [PostInLine, ]

class CommentAdminInline(admin.TabularInline):
    model = Comment
    fields = [ 'id','text']
    extra = 1

class Postadmin(admin.ModelAdmin):
    list_display = [ 'id','auth','title','is_enable','publish_date','created_date','updated_time']
    inlines = [CommentAdminInline, ]

class Useradmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_first_login' , 'user_last_login']

class Tokenadmin(admin.ModelAdmin):
    list_display = ['username', 'token']


# admin.site.register(Post, Postadmin)
# admin.site.register(Post)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(Tokenlist, Tokenadmin)
# admin.site.register(User)



