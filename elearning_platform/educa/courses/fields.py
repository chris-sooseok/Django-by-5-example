from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        # ? for_fields indicate the fields used to order the data
        self.for_fields = for_fields
        # ? super refers to parent class
        super().__init__(*args, **kwargs)

    # overriding pre_save method
    def pre_save(self, model_instance, add):

        # check whether a value already exists for this field in the model instance
        # attname: attribute name given to the field in the model
        # if attname is different from None, calculate the order
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                # retrieve all module objects in this use case
                qs = self.model.objects.all()
                if self.for_fields:
                    # the field only taks into consideration existing modules that belong to the same course
                    query = {
                        field: getattr(model_instance, field) for field in self.for_fields
                    }
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                value = 0

            setattr(model_instance, self.attname, value)

            return value
        else:
            return super().pre_save(model_instance, add)