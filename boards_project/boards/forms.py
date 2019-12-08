from django import forms

class ActivateUserForm(forms.Form):
    activation_hash = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(ActivateUserForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError("password and it's confirmation do not match")