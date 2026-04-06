from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime, timedelta
from collections import defaultdict

from .models import Expense, Budget
from .forms import ExpenseForm, SignupForm


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)

    query = request.GET.get('q')
    category = request.GET.get('category')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if query:
        expenses = expenses.filter(title__icontains=query)

    if category:
        expenses = expenses.filter(category=category)

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    show_all = request.GET.get('show_all')

    if show_all:
        expenses = expenses.order_by('-date')
    else:
        expenses = expenses.order_by('-date')[:5]

    total = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0

    current_month = datetime.now().month
    current_year = datetime.now().year

    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    )

    monthly_total = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    last_7_days = datetime.now().date() - timedelta(days=7)
    weekly_total = Expense.objects.filter(
        user=request.user,
        date__gte=last_7_days
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    category_data = monthly_expenses.values('category').annotate(total=Sum('amount'))

    labels = [item['category'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    top_category = category_data.order_by('-total').first()
    top_category_name = top_category['category'] if top_category else "None"

    days = []
    daily_totals = []

    for i in range(6, -1, -1):
        day = datetime.now().date() - timedelta(days=i)
        total_day = Expense.objects.filter(
            user=request.user,
            date=day
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        days.append(day.strftime("%d %b"))
        daily_totals.append(float(total_day))

    monthly_data = defaultdict(float)

    for exp in Expense.objects.filter(user=request.user):
        key = exp.date.strftime("%b")
        monthly_data[key] += float(exp.amount)

    months = list(monthly_data.keys())
    monthly_totals = list(monthly_data.values())

    budget_obj, _ = Budget.objects.get_or_create(
        user=request.user,
        month=current_month,
        year=current_year,
        defaults={'amount': 0}
    )

    budget = budget_obj.amount
    percent_used = (monthly_total / budget * 100) if budget > 0 else 0

    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'total': total,
        'monthly_total': monthly_total,
        'weekly_total': weekly_total,
        'top_category': top_category_name,
        'labels': labels,
        'data': data,
        'days': days,
        'daily_totals': daily_totals,
        'months': months,
        'monthly_totals': monthly_totals,
        'budget': budget,
        'percent_used': round(percent_used, 2),
        'show_all': show_all
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


@login_required
def set_budget(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        current_month = datetime.now().month
        current_year = datetime.now().year

        budget_obj, _ = Budget.objects.get_or_create(
            user=request.user,
            month=current_month,
            year=current_year,
            defaults={'amount': 0}
        )

        budget_obj.amount = amount
        budget_obj.save()

    return redirect('dashboard')