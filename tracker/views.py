from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum
from .forms import SignupForm

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Category aggregation
    category_data = expenses.values('category').annotate(total=Sum('amount'))

    labels = [item['category'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'total': total,
        'labels': labels,
        'data': data
    })

@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('dashboard')

    return render(request, 'add_expense.html', {'form': form})

@login_required
def delete_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)
    expense.delete()
    return redirect('dashboard')

def signup(request):
    form = SignupForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('/accounts/login/')

    return render(request, 'signup.html', {'form': form})