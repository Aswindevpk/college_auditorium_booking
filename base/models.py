from django.db import models
#for unified id
import uuid   


# this is a base model where it is included to all models 
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # make this a class 
    class Meta:
        abstract =True
