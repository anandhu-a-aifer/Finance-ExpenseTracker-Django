from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TransactionForm
from .models import Transaction

from django.contrib import messages
from django.contrib.auth import login
from .forms import RegistrationForm




def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,"Account created successfully. Please log in.",)
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request,"finance/registration/register.html",{"form": form},)

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    income = transactions.filter(type="income").aggregate(total=Sum("amount"))["total"] or 0
    expenses = transactions.filter(type="expense").aggregate(total=Sum("amount"))["total"] or 0
    context = {
        "transactions": transactions[:10],
        "income": income,
        "expenses": expenses,
        "balance": income - expenses,
    }

    return render(request, "finance/dashboard.html", context)


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST,user=request.user,)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TransactionForm(user=request.user)

    return render(request,"finance/transaction_form.html",{"form": form},)

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction,pk=pk,user=request.user,)

    if request.method == "POST":
        transaction.delete()
        return redirect("dashboard")

    return render(
        request,
        "finance/confirm_delete.html",
        {"transaction": transaction},
    )

