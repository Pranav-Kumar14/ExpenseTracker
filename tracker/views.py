from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum
from .forms import SignupForm
from .models import Expense
from django.db.models import Sum
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    # Monthly total
    current_month = datetime.now().month
    monthly_total = expenses.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0
    # Last 7 days
    last_7_days = datetime.now().date() - timedelta(days=7)
    weekly_total = expenses.filter(date__gte=last_7_days).aggregate(Sum('amount'))['amount__sum'] or 0
    # Category breakdown
    category_data = expenses.values('category').annotate(total=Sum('amount'))
    labels = [item['category'] for item in category_data]
    data = [float(item['total']) for item in category_data]
    # Top category
    top_category = category_data.order_by('-total').first()
    top_category_name = top_category['category'] if top_category else "None"
    # Daily trend (last 7 days)
    days = []
    daily_totals = []
    for i in range(6, -1, -1):
        day = datetime.now().date() - timedelta(days=i)
        total_day = expenses.filter(date=day).aggregate(Sum('amount'))['amount__sum'] or 0

        days.append(day.strftime("%d %b"))
        daily_totals.append(float(total_day))
    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'total': total,
        'monthly_total': monthly_total,
        'weekly_total': weekly_total,
        'top_category': top_category_name,
        'labels': labels,
        'data': data,
        'days': days,
        'daily_totals': daily_totals
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