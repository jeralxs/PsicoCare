from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from transbank.error.transbank_error import TransbankError
from .webpay_config import transaction

def init_transaction(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        session_id = 'sessionId123'
        buy_order = 'buyOrder123'
        return_url = 'http://localhost:8000/payments/return/'

        try:
            response = transaction.create(buy_order, session_id, amount, return_url)
            # Ajustar según la estructura real de la respuesta
            url = response['url']  # Asegúrate de que la clave es correcta
            token = response['token']  # Asegúrate de que la clave es correcta
            return redirect(f"{url}?token_ws={token}")
        except TransbankError as e:
            return HttpResponse('Error: ' + str(e))

    return render(request, 'payments/init_transaction.html')

def return_transaction(request):
    token = request.GET.get('token_ws')

    try:
        response = transaction.commit(token)
        return render(request, 'payments/success.html', {'response': response})
    except TransbankError as e:
        return HttpResponse('Error: ' + str(e))

