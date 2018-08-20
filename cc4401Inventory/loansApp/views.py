from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from loansApp.models import Article_Loan

@login_required
def loan_data(request, loan_id):
    try:
        loan = Article_Loan.objects.get(id=loan_id)
        context = {
            'loan': loan,
        }

        return render(request, 'loansApp/loans_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')

