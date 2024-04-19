from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegisterForm, InventoryItemForm, CheckoutForm
from .models import InventoryItem, Category, Checkout
from inventory_management.settings import LOW_QUANTITY
from django.db.models import Q
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
        sort_by = request.GET.get('sort', 'pc_name')  # Default sort field updated to 'pc_name'
        search_query = request.GET.get('search', '')

        items = InventoryItem.objects.filter(user=request.user)

        if search_query:
            query = (
                Q(pc_name__icontains=search_query) | \
                Q(barcode__icontains=search_query) | \
                Q(category__name__icontains=search_query) | \
                Q(supplier__name__icontains=search_query) | \
                Q(department__location__icontains=search_query) | \
                Q(notes__icontains=search_query)
            )
            items = items.filter(query)

        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        
        items = items.order_by(sort_by)
        
        return render(request, 'inventory/dashboard.html', {
            'items': items,
            'search_query': search_query,
            'next_sort_order': 'desc' if sort_order == 'asc' else 'asc'
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
        # Capture barcode data from the POST request and save it
        barcode = self.request.POST.get('barcode', '')  # Assuming barcode data is sent in POST request
        form.instance.barcode = barcode  # Assuming you have a 'barcode' field in your model
        return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'

@csrf_exempt  # Temporarily disable CSRF for this view for demonstration purposes.
def update_inventory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Decode and load the JSON data
            barcode = data.get('barcode')

            # Here add logic to handle the barcode,
            # such as looking up the InventoryItem, updating quantities, etc.

            # For demonstration, let's just return the barcode in the response
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
            # Assuming category is a ForeignKey in InventoryItem
            return JsonResponse({'exists': True, 'item': {'name': item.name, 'quantity': item.quantity + 1, 'category_id': item.category.id if item.category else None}})
        except InventoryItem.DoesNotExist:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)

@login_required
@permission_required('inventory.can_checkout_items', raise_exception=True)
def checkout_item(request, item_id):
    item = InventoryItem.objects.get(pk=item_id)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            if not item.is_checked_out:  # Check if the item is not already checked out
                item.is_checked_out = True
                item.last_checked_out_by = request.user
                item.last_checked_out_at = timezone.now()
                item.save()
                
                checkout = form.save(commit=False)
                checkout.item = item
                checkout.checked_out_to = request.user
                checkout.checked_out_by = request.user
                checkout.checked_out_at = timezone.now()
                checkout.save()
                
                messages.success(request, 'Item successfully checked out.')
                return redirect('dashboard')
            else:
                messages.error(request, 'This item is not available for checkout.')
        return render(request, 'inventory/checkout_item.html', {'form': form, 'item': item})
    else:
        form = CheckoutForm(initial={'checked_out_to': request.user})
    return render(request, 'inventory/checkout_item.html', {'form': form, 'item': item})

def list_checked_out_items(request):
    checkouts = Checkout.objects.select_related('item', 'user').all()
    return render(request, 'inventory/itemsout.html', {'checkouts': checkouts})