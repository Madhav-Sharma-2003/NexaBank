from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import BankAccount, Transaction
from .serializers import BankAccountSerializer, TransactionSerializer
from decimal import Decimal
import random

def generate_account_number():
    return str(random.randint(100000000000, 999999999999))

# ── REGISTER ──────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    account_type = request.data.get('account_type', 'savings')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

    account_number = generate_account_number()
    while BankAccount.objects.filter(account_number=account_number).exists():
        account_number = generate_account_number()

    BankAccount.objects.create(
        user=user,
        account_number=account_number,
        account_type=account_type,
        balance=0.00
    )

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'message': 'Account successfully created!',
        'token': token.key,
        'username': user.username,
        'account_number': account_number,
    }, status=201)


# ── LOGIN ──────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=401)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'username': user.username,
    })


# ── ACCOUNT DETAIL ─────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_account(request):
    try:
        account = BankAccount.objects.get(user=request.user)
        serializer = BankAccountSerializer(account)
        return Response(serializer.data)
    except BankAccount.DoesNotExist:
        return Response({'error': 'Account not found'}, status=404)


# ── TRANSACTIONS ───────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_transactions(request):
    account = BankAccount.objects.get(user=request.user)
    transactions = account.transactions.all().order_by('-timestamp')
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


# ── DEPOSIT ────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_deposit(request):
    amount = request.data.get('amount')
    description = request.data.get('description', '')

    try:
        amount = Decimal(str(amount)).quantize(Decimal('0.01'))
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return Response({'error': 'Valid amount is required'}, status=400)

    account = BankAccount.objects.get(user=request.user)
    account.balance += amount
    account.save()

    Transaction.objects.create(
        account=account,
        transaction_type='deposit',
        amount=amount,
        description=description
    )

    return Response({
        'message': f'₹{amount} deposited!',
        'new_balance': str(account.balance)
    })


# ── WITHDRAWAL ─────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_withdrawal(request):
    amount = request.data.get('amount')
    description = request.data.get('description', '')

    try:
        amount = Decimal(str(amount)).quantize(Decimal('0.01'))
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return Response({'error': 'Valid amount is required'}, status=400)

    account = BankAccount.objects.get(user=request.user)

    if amount > account.balance:
        return Response({'error': 'Insufficient balance!'}, status=400)

    account.balance -= amount
    account.save()

    Transaction.objects.create(
        account=account,
        transaction_type='withdrawal',
        amount=amount,
        description=description
    )

    return Response({
        'message': f'₹{amount} withdrawn!',
        'new_balance': str(account.balance)
    })


# ── TRANSFER ───────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_transfer(request):
    amount = request.data.get('amount')
    target_account_number = request.data.get('target_account')
    description = request.data.get('description', '')

    try:
        amount = Decimal(str(amount)).quantize(Decimal('0.01'))
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return Response({'error': 'Valid amount is required'}, status=400)

    try:
        sender = BankAccount.objects.get(user=request.user)
        receiver = BankAccount.objects.get(account_number=target_account_number)
    except BankAccount.DoesNotExist:
        return Response({'error': 'Account not found'}, status=404)

    if sender == receiver:
        return Response({'error': 'You cannot transfer to your own account'}, status=400)

    if amount > sender.balance:
        return Response({'error': 'Insufficient balance!'}, status=400)

    sender.balance -= amount
    receiver.balance += amount
    sender.save()
    receiver.save()

    Transaction.objects.create(
        account=sender,
        transaction_type='transfer',
        amount=amount,
        description=f'Transfer to {target_account_number}'
    )
    Transaction.objects.create(
        account=receiver,
        transaction_type='deposit',
        amount=amount,
        description=f'Transfer from {sender.account_number}'
    )

    return Response({
        'message': f'₹{amount} transferred!',
        'new_balance': str(sender.balance)
    })