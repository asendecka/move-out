from django import forms

from .models import Thing
from .utils import resize_image


class ThingForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        picture = None
        if self.cleaned_data['picture']:
            picture = resize_image(self.cleaned_data.pop('picture'))
        kwargs['commit'] = False
        instance = super(ThingForm, self).save(*args, **kwargs)
        instance.picture = picture
        instance.save()
        return instance

    class Meta:
        model = Thing
        fields = ('name', 'picture', 'description')
