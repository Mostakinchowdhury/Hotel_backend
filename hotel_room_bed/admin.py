from django.contrib import admin

# Register your models here.
from django.apps import apps

# Get all models from the current 'api' app
models = apps.get_app_config('hotel_room_bed').get_models()

for model in models:
    # Create a dynamic Admin class for each model
    admin_class = type(
        f"{model.__name__}Admin",
        (admin.ModelAdmin,),
        {
            "list_display": [field.name for field in model._meta.fields],
            "list_filter": [field.name for field in model._meta.fields if field.name != "id"],
            "search_fields": [field.name for field in model._meta.fields if field.get_internal_type() in ["CharField", "TextField"]],
            "ordering": ["-id"],


            
            }

    )
    
    # Register the model with the dynamic Admin class
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
