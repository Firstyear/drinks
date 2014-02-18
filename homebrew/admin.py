from django.contrib import admin
from homebrew.models import SourceIngredient, Yeast, Batch, Box, Sugar, Label, Comment

# Register your models here.
admin.site.register(Label)
admin.site.register(SourceIngredient)
admin.site.register(Yeast)
admin.site.register(Sugar)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('pot_start_date', 'predicted_brew_ready', 'predicted_ready', 'predicted_abv')
admin.site.register(Batch, BatchAdmin)
admin.site.register(Box)
admin.site.register(Comment)
