from django.shortcuts import render, redirect
from django.contrib import messages
from .form import *
from .models import *

def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.initial_amount = var.amount
            var.save()
            messages.info(request, 'New Item has been added to the Store')
            return redirect('all-items')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('add-item')
    else:
        form = AddItemForm()
        context = {'form': form}
        return render(request, 'store/add_item.html', context)

        
        
def update_item(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.info(request, 'Item info has been updated')
            return redirect('all-items')
        else:
            messages.warning(request, 'Something went wrong')
            #return redirect('add-item')
    else:
        form = UpdateItemForm(instance=item)
        context = {'form': form}
        return render(request, 'store/update_item.html', context)
    
    

def all_items(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'store/all_items.html', context)



def delete_item(request, pk):
    item = Item.objects.get(pk=pk)
    item.delete()
    messages.info(request, 'Item deleted successfully')
    return redirect('all-items')



def issue_item(request):
    if request.method == 'POST':
        form = IssueItemForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.issued_by = request.user
            get_item = Item.objects.get(pk=var.item.pk)
            if get_item.amount != 0: 
                if get_item.amount > var.issued_amount:
                    get_item.amount = get_item.amount - var.issued_amount
                    get_item.save()
                    var.save()
                    messages.info(request, f'Item has been issued to {var.issued_to}')
                    return redirect('all-items')
                else:
                    messages.warning(request, f'Not much item remaining in the store. We only have ({get_item.amount}) left!')
                    return redirect('all-items')
                    
            else:
                messages.warning(request, 'No item in the store.')
                return redirect('all-items')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('issue-item')
    else:
        form = IssueItemForm()
        context = {'form': form}
        return render(request, 'store/issue_item.html', context)


def issue_history(request):
    items = IssueItem.objects.all().order_by('-issued_date')
    context = {'items':items}
    return render(request, 'store/issue_history.html', context)


def return_item(request):
    if request.method == 'POST':
        form = ReturnItemForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            get_item = Item.objects.get(pk=var.item.pk)
            get_item.amount = get_item.amount +var.returned_amount
            if get_item.amount > get_item.initial_amount:
                messages.warning(request, f'Items returned are more than the initial amount ({get_item.initial_amount}) we had in the store')
                return redirect('all-items')
            else:    
                get_item.save()
                var.save()
                messages.info(request, 'This Item has been returned back to the store')
                return redirect('all-items')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('return-item')
    else:
        form = ReturnItemForm()
        context = {'form': form}
        return render(request,'store/return_item.html', context)
    
    
    
def return_history(request):
    items = ReturnItem.objects.all()
    context = {'items': items}
    return render(request,'store/return_history.html', context)


def restock_item(request):
    if request.method == 'POST':
        form = RestockItemForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            get_item = Item.objects.get(pk=var.item.pk)
            var.initial_value = get_item.initial_amount
            if get_item.initial_amount is None:
                get_item.initial_amount = 0
            get_item.initial_amount += var.amount  # Adjust initial_amount
            get_item.amount += var.amount  # Also adjust amount 
            get_item.save()
            var.save()
            messages.info(request, 'Item has been restocked in the store.')
            return redirect('all-items')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('restock-item')            
    else:
        form = RestockItemForm()
        context = {'form': form}
        return render(request, 'store/restock_item.html', context)


def restock_history(request):
    items =  RestockItem.objects.all()
    context = {'items':items}
    return render(request, 'store/restock_history.html', context)