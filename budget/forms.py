from django import forms
from .models import Transaction, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["title", "amount", "date", "type", "category"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"}),}
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None:
            self.fields["category"].queryset = (Category.objects.filter(user=user))
    def save(self, commit=True):
        transaction = super().save(commit=False)
        if self.user is not None:
            transaction.user = self.user
        if commit:
            transaction.save()
        return transaction

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]