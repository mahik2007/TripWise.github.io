from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .models import *


def home(request):
    return HttpResponse("Backend Running Successfully")


# Signup
@api_view(['POST'])
def signup(request):
    data = request.data
    data['password'] = make_password(data['password'])

    User.objects.create(**data)
    return Response({"msg": "User created"})


#  Login
@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user and check_password(password, user.password):
        return Response({"msg": "Login success", "user_id": user.id})

    return Response({"msg": "Invalid credentials"})


# Create Group
@api_view(['POST'])
def create_group(request):
    Group.objects.create(**request.data)
    return Response({"msg": "Group created"})


# Add Expense
@api_view(['POST'])
def add_expense(request):
    data = request.data.copy()
    splits = data.pop('splits')

    expense = Expense.objects.create(**data)

    for s in splits:
        Split.objects.create(
            expense=expense,
            user_id=s['user_id'],
            amount=s['amount']
        )

    return Response({"msg": "Expense added"})


# Balance Calculation
@api_view(['GET'])
def balances(request, group_id):
    balances = {}

    expenses = Expense.objects.filter(group_id=group_id)

    for exp in expenses:
        splits = Split.objects.filter(expense=exp)

        for s in splits:
            balances[s.user_id] = balances.get(s.user_id, 0) - float(s.amount)
            balances[exp.paid_by_id] = balances.get(exp.paid_by_id, 0) + float(s.amount)

    return Response(balances)


# Settle Up
@api_view(['GET'])
def settle_up(request, group_id):
    from collections import defaultdict

    balances = defaultdict(float)
    expenses = Expense.objects.filter(group_id=group_id)

    for exp in expenses:
        splits = Split.objects.filter(expense=exp)

        for s in splits:
            balances[s.user_id] -= float(s.amount)
            balances[exp.paid_by_id] += float(s.amount)

    creditors = []
    debtors = []

    for user, amount in balances.items():
        if amount > 0:
            creditors.append([user, amount])
        elif amount < 0:
            debtors.append([user, -amount])

    transactions = []

    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        d_user, d_amt = debtors[i]
        c_user, c_amt = creditors[j]

        settle_amt = min(d_amt, c_amt)

        transactions.append({
            "from": d_user,
            "to": c_user,
            "amount": settle_amt
        })

        debtors[i][1] -= settle_amt
        creditors[j][1] -= settle_amt

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return Response(transactions)
# ─── AI CHATBOT VIEW ───────────────────────────────────
import sys
import os

@api_view(['POST'])
def chatbot(request):
    user_message = request.data.get('message', '')

    if not user_message:
        return Response({"error": "Message cannot be empty"}, status=400)

    chatbot_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..')
    )
    if chatbot_path not in sys.path:
        sys.path.insert(0, chatbot_path)

    from ai_chatbot.chatbot import get_ai_response
    reply = get_ai_response(user_message)

    return Response({"reply": reply})