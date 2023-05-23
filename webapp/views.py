from django.shortcuts import HttpResponse, render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Mech
from .forms import CreateMechForm, UpdateMechForm

class MechList(generic.ListView):
    model = Mech
    queryset = Mech.objects.all().order_by('name')
    template_name = 'mechs.html'
    paginate_by = 10


class MechDetail(LoginRequiredMixin, generic.ListView):
    login_url = "/accounts/login/"

    def get(self, request, slug, *args, **kwargs):
        queryset = Mech.objects.all()
        mech = get_object_or_404(queryset, slug=slug)
        return render(
            request,
            "mech_detail.html",
            {
                "mech": mech
            },
        )
 
class CreateMechView(LoginRequiredMixin, generic.CreateView):
    login_url = "/accounts/login/"
    model = Mech
    form_class = CreateMechForm
    template_name = 'mechs_form.html'    
    success_url = reverse_lazy('mechs')

    def form_valid(self, form):
        messages.success(self.request, "The Mech was successfully created.")
        return super(CreateMechView,self).form_valid(form)

class UpdateMechView(LoginRequiredMixin, UpdateView):
    login_url = "/accounts/login/"
    model = Mech
    form_class = UpdateMechForm
    template_name = 'mechs_form.html'    
    success_url = reverse_lazy('mechs')

    def form_valid(self, form):
        messages.success(self.request, "The Mech was successfully updated.")
        return super(UpdateMechView,self).form_valid(form)

class DeleteMechView(LoginRequiredMixin, DeleteView):
    login_url = "/accounts/login/"
    model = Mech
    context_object_name = 'mech'
    success_url = reverse_lazy('mechs')
    template_name = 'mech_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "The Mech was successfully deleted.")
        return super(DeleteMechView, self).delete(request, *args, **kwargs)
    
@login_required
def toggle_mech_status(request, slug):
    mech = get_object_or_404(Mech, slug=slug)
    if mech.status == 0:
        mech.status = 1
    else:
        mech.status = 0
    mech.save()
    return redirect('mechs')