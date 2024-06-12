from django import forms


class APIEndpointForm(forms.Form):
    endpoint_name = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'gin',
        }
    ))

    class Meta:
        fields = ['endpoint']