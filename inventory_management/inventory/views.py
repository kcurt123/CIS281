from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegisterForm, InventoryItemForm, CheckoutForm, PersonForm
from .models import InventoryItem, Category, Checkout, Person
from inventory_management.settings import LOW_QUANTITY
from django.db.models import Q, Prefetch, OuterRef, Subquery, F, Value
from django.db.models.functions import Concat
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest
from django.utils import timezone
import json

class Index(TemplateView):
	template_name = 'inventory/index.html'

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        sort_order = request.GET.get('order', 'asc')
        sort_by = request.GET.get('sort', 'pc_name')
        search_query = request.GET.get('search', '')
        print_mode = 'print' in request.GET

        items = InventoryItem.objects.filter(user=request.user)

        if search_query and not print_mode:
            query = (
                Q(pc_name__icontains=search_query) | 
                Q(category__name__icontains=search_query) | 
                Q(supplier__name__icontains=search_query) | 
                Q(location_name__icontains=search_query) | 
                Q(department__location__icontains=search_query) | 
                Q(notes__icontains=search_query)
            )
            items = items.filter(query)

        if sort_by in ['domain_user', 'department', 'person_name']:  # Use 'person_name' instead of 'person'
            if sort_by == 'domain_user':
                last_checkout_user = Checkout.objects.filter(
                    item_id=OuterRef('pk')
                ).order_by('-checked_out_at').values('checked_out_to__domain_user')[:1]
                items = items.annotate(domain_user=Subquery(last_checkout_user))

            elif sort_by == 'department':
                last_checkout_department = Checkout.objects.filter(
                    item_id=OuterRef('pk')
                ).order_by('-checked_out_at').values('checked_out_to__department')[:1]
                items = items.annotate(department=Subquery(last_checkout_department))

            elif sort_by == 'person_name':
                last_checkout_person = Checkout.objects.filter(
                    item_id=OuterRef('pk')
                ).order_by('-checked_out_at').annotate(
                    full_name=Concat('checked_out_to__first_name', Value(' '), 'checked_out_to__last_name')
                ).values('full_name')[:1]
                items = items.annotate(person_name=Subquery(last_checkout_person))

            sort_prefix = '' if sort_order == 'asc' else '-'
            items = items.order_by(f"{sort_prefix}{sort_by}")
        else:
            sort_prefix = '' if sort_order == 'asc' else '-'
            items = items.order_by(f"{sort_prefix}{sort_by}")

        if print_mode:
            return render(request, 'inventory/dashboard_print.html', {
                'items': items,
                'print_mode': True,
                'show_print_button': True
            })

        return render(request, 'inventory/dashboard.html', {
            'items': items,
            'search_query': search_query,
            'next_sort_order': 'desc' if sort_order == 'asc' else 'asc',
            'show_print_button': True
        })


class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/signup.html', {'form': form})

class LogoutView(View):
    def post(self, request):
        logout(request)
        return render(request, 'inventory/logout.html')

class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        barcode = self.request.POST.get('barcode', '')  
        form.instance.barcode = barcode 
        return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        """
        Override the get_object method to retrieve the item based on the URL parameter (pk).
        """
        pk = self.kwargs.get('pk')
        return get_object_or_404(InventoryItem, pk=pk, user=self.request.user)

    def form_valid(self, form):
        return super().form_valid(form)

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'

@csrf_exempt  
def update_inventory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8')) 
            barcode = data.get('barcode')

            
            return JsonResponse({'status': 'success', 'barcode': barcode})
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
    else:
        return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)
	
def check_item_by_barcode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        barcode = data.get('barcode', '')
        try:
            item = InventoryItem.objects.get(barcode=barcode)
            return JsonResponse({'exists': True, 'item': {'name': item.name, 'quantity': item.quantity + 1, 'category_id': item.category.id if item.category else None}})
        except InventoryItem.DoesNotExist:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)

@login_required
@permission_required('inventory.can_checkout_items', raise_exception=True)
def checkout_item(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            if not item.is_checked_out:  
                item.is_checked_out = True
                item.last_checked_out_by = request.user
                item.last_checked_out_at = timezone.now()
                item.save()
                
                checkout = form.save(commit=False)
                checkout.item = item
                checkout.checked_out_to = form.cleaned_data['checked_out_to']  
                checkout.checked_out_by = request.user
                checkout.checked_out_at = timezone.now()
                checkout.save()
                
                messages.success(request, 'Item successfully checked out.')
                return redirect('checked-out-items')  
            else:
                messages.error(request, 'This item is not available for checkout.')
        else:
            return render(request, 'inventory/checkout_item.html', {'form': form, 'item': item})
    else:
        form = CheckoutForm(initial={'item': item,'checked_out_by': request.user})
    return render(request, 'inventory/checkout_item.html', {'form': form, 'item': item})


def checked_out_items(request):
    search_query = request.GET.get('search', '')
    sort_order = request.GET.get('order', 'asc')
    sort_by = request.GET.get('sort', 'checked_out_at')
    print_mode = 'print' in request.GET  # Check for print mode

    checkouts = Checkout.objects.filter(returned=False)

    if search_query:
        checkouts = checkouts.filter(
            Q(item__pc_name__icontains=search_query) |
            Q(checked_out_by__username__icontains=search_query) |  
            Q(checked_out_to__first_name__icontains=search_query) |  
            Q(checked_out_to__last_name__icontains=search_query)
        )

    if not print_mode and sort_order == 'desc':  
        sort_by = f'-{sort_by}'
    checkouts = checkouts.order_by(sort_by)

    if print_mode:
        return render(request, 'inventory/checked_out_items_print.html', {
            'checkouts': checkouts,
            'search_query': search_query,
            'print_mode': True
        })

    return render(request, 'inventory/checked_out_items.html', {
        'checkouts': checkouts,
        'search_query': search_query,
        'next_sort_order': 'desc' if sort_order == 'asc' else 'asc',
        'show_print_button': True
    })


def return_item(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    if item.is_checked_out:
        item.is_checked_out = False
        item.save()
        Checkout.objects.filter(item=item, returned=False).update(returned=True)
        messages.success(request, f'{item.pc_name} has been successfully returned.')
    else:
        messages.error(request, 'This item was not checked out.')

    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('dashboard')

def get_dashboard(request):
    items = InventoryItem.objects.all().prefetch_related(
        Prefetch('checkouts', queryset=Checkout.objects.select_related('checked_out_to'))
    )
    return render(request, 'dashboard.html', {'items': items})

def dashboard_print(request):
    # Default columns to show if none are selected
    default_columns = ['pc_name', 'domain_user', 'person', 'department', 'device_type', 'cost', 'new_computer', 'date_delivered', 'computer_laptop', 'dock', 'lcd', 'lcd2', 'stand', 'keyboard', 'cd', 'supplier', 'notes', 'status']
    selected_columns = request.GET.getlist('cols') or default_columns
    items = InventoryItem.objects.all()
    return render(request, 'dashboard-print.html', {
        'items': items,
        'selected_columns': selected_columns
    })


