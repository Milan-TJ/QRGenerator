from django import forms

ERROR_CHOICES = [
    ('L', 'Low (7%)'),
    ('M', 'Medium (15%)'),
    ('Q', 'Quartile (25%)'),
    ('H', 'High (30%)'),
]

class QRForm(forms.Form):
    data = forms.CharField(
        label="Text or URL",
        widget=forms.Textarea(attrs={"rows":3, "placeholder":"Enter text or URL..."}),
        max_length=5000
    )
    box_size = forms.IntegerField(label="Box size (px)", min_value=1, max_value=40, initial=10)
    border = forms.IntegerField(label="Border (boxes)", min_value=0, max_value=10, initial=4)
    error_correction = forms.ChoiceField(label="Error correction", choices=ERROR_CHOICES, initial='M')
    logo = forms.ImageField(
        label="Optional logo (small PNG/JPEG)",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'file-upload-input',
            'id': 'logo-upload'
        })
    )
