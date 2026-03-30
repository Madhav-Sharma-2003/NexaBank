from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankAccount, Transaction
from decimal import Decimal
from django.http import JsonResponse
import random

def search_user(request):
    username = request.GET.get('username', '')
    if len(username) < 3:
        return JsonResponse({'found': False})
    
    try:
        user = User.objects.get(username__icontains=username)
        account = BankAccount.objects.get(user=user)
        return JsonResponse({
            'found': True,
            'username': user.username,
            'account_number': account.account_number,
            'account_type': account.account_type,
        })
    except (User.DoesNotExist, BankAccount.DoesNotExist):
        return JsonResponse({'found': False})


def generate_account_number():
    return str(random.randint(100000000000, 999999999999))

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        account_type = request.POST['account_type']

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        
        account_number = generate_account_number()
        while BankAccount.objects.filter(account_number=account_number).exists():
            account_number = generate_account_number()

        BankAccount.objects.create(
            user=user,
            account_number=account_number,
            account_type=account_type,
            balance=0.00
        )

        login(request, user)
        messages.success(request, f'Account created! Account Number: {account_number}')
        return redirect('dashboard')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    try:
        account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        messages.error(request, 'Account does not exist!')
        return redirect('register')

    transactions = account.transactions.all().order_by('-timestamp')

    if request.method == 'POST':
        action = request.POST.get('action')
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Invalid amount!')
            return redirect('dashboard')

        if action == 'deposit':
            account.balance += amount
            account.save()
            Transaction.objects.create(
                account=account,
                transaction_type='deposit',
                amount=amount,
                description=description
            )
            messages.success(request, f'₹{amount} deposited!')

        elif action == 'withdrawal':
            if amount > account.balance:
                messages.error(request, 'Insufficient balance!')
            else:
                account.balance -= amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    transaction_type='withdrawal',
                    amount=amount,
                    description=description
                )
                messages.success(request, f'₹{amount} withdrawn!')

        elif action == 'transfer':
            target_account_number = request.POST.get('target_account')
            try:
                target_account = BankAccount.objects.get(account_number=target_account_number)
            except BankAccount.DoesNotExist:
                messages.error(request, 'Account number does not exist!')
                return redirect('dashboard')

            if target_account == account:
                messages.error(request, 'You cannot transfer to your own account!')
                return redirect('dashboard')

            if amount > account.balance:
                messages.error(request, 'Insufficient balance!')
            else:
                account.balance -= amount
                target_account.balance += amount
                account.save()
                target_account.save()
                Transaction.objects.create(
                    account=account,
                    transaction_type='transfer',
                    amount=amount,
                    description=f'Transfer to {target_account_number}'
                )
                Transaction.objects.create(
                    account=target_account,
                    transaction_type='deposit',
                    amount=amount,
                    description=f'Transfer from {account.account_number}'
                )
                messages.success(request, f'₹{amount} transferred!')

        return redirect('dashboard')

    return render(request, 'accounts/dashboard.html', {
        'account': account,
        'transactions': transactions
    })
    
def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/landing.html')
