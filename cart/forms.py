from django.forms import ModelForm, HiddenInput, TextInput
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.contrib.contenttypes.models import ContentType
import models

class ItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = u''
    class Meta:
        model = models.Item
        fields = ('content_type','object_id','quantity')
        widgets = {
            'content_type':HiddenInput,
            'object_id':HiddenInput,
            'quantity':TextInput(attrs={'size':'3'}),
        }

ItemFormSet = modelformset_factory(models.Item, form = ItemForm, max_num=0) 
