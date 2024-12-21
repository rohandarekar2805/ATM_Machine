from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from decimal import Decimal  
def home(request):
    return render(request, 'home.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from decimal import Decimal

def create_account(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        name = request.POST.get('name')
        balance = request.POST.get('balance')
        pin = request.POST.get('pin')

        
        errors = []

        
        if not account_number.isdigit() or len(account_number) != 12:
            errors.append("Account number must be exactly 12 digits.")

        
        if len(name) > 30:
            errors.append("Name must not exceed 30 characters.")

        
        try:
            balance = Decimal(balance)
            if balance < 0:
                errors.append("Balance must be a positive number.")
        except:
            errors.append("Invalid balance. Please enter a valid number.")

        # Validate PIN (4 digits)
        if not pin.isdigit() or len(pin) != 4:
            errors.append("PIN must be exactly 4 digits.")

        # If errors exist, send them back to the form
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'create_account.html')

        # If no errors, save the account
        Account.objects.create(
            account_number=account_number,
            name=name,
            balance=balance,
            pin=pin
        )
        messages.success(request, "Account created successfully!")
        return redirect('create_account')

    return render(request, 'create_account.html')


def login(request):
    if request.method == 'POST':
        account_number = request.POST['account_number']
        pin = request.POST['pin']
        try:
            account = Account.objects.get(account_number=account_number, pin=pin)
            request.session['account_id'] = account.id
            return redirect('dashboard')
        except Account.DoesNotExist:
            messages.error(request, 'Invalid account number or PIN')
    return render(request, 'login.html')

def dashboard(request):
    account_id = request.session.get('account_id')
    if not account_id:
        return redirect('login')
    account = Account.objects.get(id=account_id)
    return render(request, 'dashboard.html', {'account': account})




def deposit(request):
    account_id = request.session.get('account_id')
    if not account_id:
        return redirect('login')
    
    account = Account.objects.get(id=account_id)
    
    if request.method == 'POST':
        try:
            
            amount = Decimal(request.POST['amount'])
            account.balance += amount  
            account.save()  
            messages.success(request, f"${amount} deposited successfully!") 
        except (ValueError, Decimal.InvalidOperation):  
            messages.error(request, "Invalid amount entered. Please enter a valid number.") 
        return redirect('deposit')  
    
    return render(request, 'deposit.html')  


def withdraw(request):
    account_id = request.session.get('account_id')
    if not account_id:
        return redirect('login')
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        try:
           
            amount = Decimal(request.POST['amount'])
            if amount > account.balance:
                messages.error(
                    request,
                    f"Insufficient funds. Your current balance is ${account.balance}."
                )
            else:
                account.balance -= amount
                account.save()
                messages.success(request, f"${amount} withdrawn successfully!")
        except (ValueError, Decimal.InvalidOperation):
            messages.error(request, "Invalid amount entered. Please enter a valid number.")
        return redirect('withdraw')
    return render(request, 'withdraw.html')  

def logout(request):
    request.session.flush()
    return redirect('login')
