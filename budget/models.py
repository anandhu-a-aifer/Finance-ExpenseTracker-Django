
from django.conf import settings
from django.db import models


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="categories",)
    name = models.CharField(max_length=100)
    spending_limit = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True,)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "name"],name="unique_category_per_user",)]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TYPE_CHOICES = [(INCOME, "Income"),(EXPENSE, "Expense"),]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="transactions",)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name="transactions",)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.title} - {self.amount}"


class MonthlyBudget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="monthly_budgets",)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,related_name="budgets")
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    amount_limit = models.DecimalField(max_digits=12,decimal_places=2,)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "category", "month", "year"],name="unique_monthly_budget",)]

    def __str__(self):
        return f"{self.month}/{self.year}: {self.amount_limit}"
