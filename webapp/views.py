from django.shortcuts import HttpResponse, render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


from .models import Mech
from .forms import CreateMechForm, UpdateMechForm


class CardList(generic.ListView):
    model = Mech
    queryset = Mech.objects.filter(status=1).order_by('name')
    template_name = 'index.html'
    paginate_by = 10

class MechList(LoginRequiredMixin, generic.ListView):
    login_url = "/accounts/login/"
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

class CreateMechView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    permission_required = "webapp.add_mech"
    login_url = "/accounts/login/"
    model = Mech
    form_class = CreateMechForm
    template_name = 'new_mechs_form.html'    
    success_url = reverse_lazy('mechs')

    def form_valid(self, form):
        messages.success(self.request, "The Mech was successfully created.")
        return super(CreateMechView,self).form_valid(form)

class UpdateMechView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "webapp.change_mech"
    login_url = "/accounts/login/"
    model = Mech
    form_class = UpdateMechForm
    template_name = 'mechs_form.html'    

    def get_success_url(self):
        return reverse('mech_detail', kwargs={'slug': self.object.slug})


    def form_valid(self, form):
        messages.success(self.request, "The Mech was successfully updated.")
        return super(UpdateMechView,self).form_valid(form)

class DeleteMechView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = "webapp.delete_mech"
    login_url = "/accounts/login/"
    model = Mech
    context_object_name = 'mech'
    success_url = reverse_lazy('mechs')
    template_name = 'mech_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "The Mech was successfully deleted.")
        return super(DeleteMechView, self).delete(request, *args, **kwargs)
    
@login_required
@permission_required("webapp.change_mech", raise_exception=True)
def toggle_mech_status(request, slug):
    mech = get_object_or_404(Mech, slug=slug)
    if mech.status == 0:
        mech.status = 1
    else:
        mech.status = 0
    mech.save()
    return redirect('mechs')

def error_404(request, exception):
    return render(request, '404.html')

def error_404(request, exception):
    return render(request, '403.html')