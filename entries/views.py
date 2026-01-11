from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from entries.forms import EntriesForm
from entries.models import Entries


class EntriesListView(LoginRequiredMixin, ListView):
    model = Entries
    template_name = "entries/entries_list.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        queryset = Entries.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset

    def entries_list(request):
        query = request.GET.get('q', '')
        if query:

            posts = Entries.objects.filter(
                heading__icontains=query
            ) | Entries.objects.filter(
                content__icontains=query
            )
        else:
            posts = Entries.objects.all()

        return render(request, 'entries/list.html', {'posts': posts})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class EntriesDetailView(LoginRequiredMixin, DetailView):
    model = Entries
    template_name = "entries/entries_detail.html"
    context_object_name = "entries"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Entries, pk=self.kwargs["pk"], user=self.request.user)
        return obj


class EntriesCreateView(LoginRequiredMixin, CreateView):
    model = Entries
    form_class = EntriesForm
    template_name = "entries/entries_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая запись"
        return context

    def get_success_url(self):
        return reverse_lazy("entries:entries_detail", kwargs={"pk": self.object.pk})


class EntriesUpdateView(LoginRequiredMixin, UpdateView):
    model = Entries
    form_class = EntriesForm
    template_name = "entries/entries_form.html"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Entries, pk=self.kwargs["pk"], user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование записи"
        return context

    def get_success_url(self):
        return reverse_lazy("entries:entries_detail", kwargs={"pk": self.object.pk})


class EntriesDeleteView(LoginRequiredMixin, DeleteView):
    model = Entries
    template_name = "entries/entries_confirm_delete.html"
    context_object_name = "entries"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Entries, pk=self.kwargs["pk"], user=self.request.user)
        return obj

    def get_success_url(self):
        return reverse_lazy("entries:home")


class HomeView(LoginRequiredMixin, ListView):
    model = Entries
    template_name = "home.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        return Entries.objects.filter(user=self.request.user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context
