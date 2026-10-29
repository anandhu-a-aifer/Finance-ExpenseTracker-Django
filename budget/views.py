from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from .forms import TransactionForm,CategoryForm
from .models import Transaction,Category
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegistrationForm
from django.db.models.functions import TruncMonth




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
    return render(request,"registration/register.html",{"form": form},)

@login_required
def dashboard(request):
    # Only show transactions belonging to the logged-in user.
    user_transactions = Transaction.objects.filter(
        user=request.user
    )

    # Overall income and expenses.
    income = (
        user_transactions.filter(type="income")
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    expenses = (
        user_transactions.filter(type="expense")
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    balance = income - expenses

    # Current month's expenses.
    today = date.today()

    current_month_transactions = user_transactions.filter(
        date__year=today.year,
        date__month=today.month,
    )

    monthly_expenses = (
        current_month_transactions.filter(type="expense")
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    # Latest 10 transactions.
    transactions = user_transactions.select_related(
        "category"
    ).order_by("-date", "-id")[:10]

    # Expense totals grouped by category.
    category_expenses = (
        user_transactions.filter(type="expense")
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    # Calculate the last 6 calendar months, including this month.
    monthly_data = (
        user_transactions.filter(type="expense")
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    monthly_totals = {
        item["month"].strftime("%Y-%m"): float(item["total"] or 0)
        for item in monthly_data
        if item["month"] is not None
    }

    chart_labels = []
    chart_values = []

    for offset in range(5, -1, -1):
        month_index = today.month - offset
        year = today.year

        while month_index <= 0:
            month_index += 12
            year -= 1

        month_date = date(year, month_index, 1)
        month_key = month_date.strftime("%Y-%m")

        chart_labels.append(month_date.strftime("%b %Y"))
        chart_values.append(monthly_totals.get(month_key, 0))

    context = {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "monthly_expenses": monthly_expenses,
        "transactions": transactions,
        "category_expenses": category_expenses,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    }

    return render(request,"finance/dashboard.html",context,)

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

@login_required
def category_list(request):
    categories = Category.objects.filter(
        user=request.user
    ).order_by("name")

    return render(
        request,
        "finance/category_list.html",
        {"categories": categories},
    )


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()

            messages.success(
                request,
                "Category added successfully."
            )
            return redirect("category_list")
    else:
        form = CategoryForm()

    return render(
        request,
        "finance/category_form.html",
        {
            "form": form,
            "title": "Add Category",
        },
    )


@login_required
def edit_category(request, pk):
    category = get_object_or_404(
        Category,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Category updated successfully."
            )
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)

    return render(request,"finance/category_form.html",{"form": form,"title": "Edit Category",},)


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category,pk=pk,user=request.user,)
    if request.method == "POST":
        category.delete()
        messages.success(request,"Category deleted successfully.")
        return redirect("category_list")

    return render(request,"finance/category_confirm_delete.html",{"category": category},)