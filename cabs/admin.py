from django.contrib import admin
from .models import Feedback,Post


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'date','email')
    list_filter = ('date',)
    search_fields = ( 'details',)

    class Meta:
        model = Feedback


class PostAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'date','time','destination')
    list_filter = ('date',)
    search_fields = ( 'id',)

    class Meta:
        model = Feedback


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Post, PostAdmin)

