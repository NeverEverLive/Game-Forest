from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.viewsets import ModelViewSet

from forum.forms import AuthUserForm, RegisterForm, GameForm, DeveloperForm, SponsorForm, PublisherForm, CompanyForm, AwardForm
from forum.models import *
from forum.serializers import *


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DeveloperViewSet(ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer


class PublisherViewSet(ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class AwardViewSet(ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = GenreSerializer


@login_required(login_url='login/', redirect_field_name='detail_page')
def detail_page(request, pk):
    game = Game.objects.get(pk=pk)
    developer = Developer.objects.all()
    publisher = Publisher.objects.all()
    sponsor = Sponsor.objects.all()
    award = AwardGameRelation.objects.all()

    context = {
        'game': game,
        'developer': developer,
        'publisher': publisher,
        'sponsor': sponsor,
        'award': award,
    }
    template = 'detail.html'
    return render(request, template, context)


class HomeView(ListView):
    model = Game
    template_name = 'index.html'
    context_object_name = 'queryset'

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     context['queryset'] = Game.objects.all()
    #     context['company'] = Company.objects.all()


class HomeDetailView(DetailView):
    model = Game
    template_name = 'detail.html'
    context_object_name = 'get_article'


class ForumLogin(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home_page')

    def get_success_url(self):
        return self.success_url


class RegisterView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form_valid = super(RegisterView, self).form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


class LogOutView(LogoutView):
    next_page = reverse_lazy('home_page')


class CustomSuccessMessageMixin:
    @property
    def success_message(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(CustomSuccessMessageMixin, self).form_valid(form)

    def get_success_url(self):
        return f'{self.success_url}?id={self.object.id}'


def is_member(user):
    return user.groups.filter(name='Editor').exists()


def edit(request):
    template = 'edit.html'
    return render(request, template)


@user_passes_test(is_member)
def create_game(request):
    success = False
    game = Game.objects.all()
    developer = Developer.objects.all()
    publisher = Publisher.objects.all()
    sponsor = Sponsor.objects.all()
    award = AwardGameRelation.objects.all()
    game_form = GameForm(request.POST)

    if request.method == 'POST':
    # developer_form = DeveloperForm
    # publisher_form = PublisherForm
    # sponsor_form = SponsorForm
        game_form = GameForm(request.POST)

        if game_form.is_valid():                                # для добавления разработчиков и т.д.
            new_developer = game_form.cleaned_data.get('developer')
            new_publisher = game_form.cleaned_data.get('publisher')
            new_sponsor = game_form.cleaned_data.get('sponsor')
            new_award = game_form.cleaned_data.get('award')
            game_form.save()
            created_game = Game.objects.order_by('-id')[0]
            Developer.objects.get_or_create(company=new_developer, game=created_game)
            Publisher.objects.get_or_create(company=new_publisher, game=created_game)
            if new_sponsor is not None:
                Sponsor.objects.get_or_create(company=new_sponsor, game=created_game)
            if new_award is not None:
                for a in new_award:
                    AwardGameRelation.objects.get_or_create(award=a, game=created_game)
            success = True
    # Developer.objects.create(developer=developer, game=)

    context = {
        'game': game.order_by('date'),
        'developer': developer,
        'publisher': publisher,
        'sponsor': sponsor,
        'award': award,
        'game_form': GameForm(),
        'success': success
        # 'developer_form': developer_form,
        # 'publisher_form': publisher_form,
        # 'sponsor_form': sponsor_form,
    }

    template = 'edit_game.html'

    return render(request, template, context)


# class GameCreateView(CustomSuccessMessageMixin ,CreateView):
#     model = Game
#     template_name = 'edit_game.html'
#     form_class = GameForm
#     success_url = reverse_lazy('edit_game.html')
#     success_message = 'Game Created'
#
#     def get_context_data(self, **kwargs):
#         kwargs['queryset'] = Game.objects.all()
#         return super(GameCreateView, self).get_context_data(**kwargs)


def update_game(request, pk):
    success = False
    get_game = Game.objects.get(pk=pk)
    game_form = GameForm(instance=get_game)

    if request.method == 'POST':
        game_form = GameForm(request.POST, instance=get_game)
        if game_form.is_valid():
            developer = game_form.cleaned_data.get('developer')
            publisher = game_form.cleaned_data.get('publisher')
            sponsor = game_form.cleaned_data.get('sponsor')
            awards = game_form.cleaned_data.get('award')
            # game_form = GameForm(request.POST, instance=get_game, developer=developer, publisher=publisher, sponsor=sponsor)
            # game_form.fields['developer'] = developer
            # game_form.fields['publisher'] = publisher
            # game_form.fields['sponsor'] = sponsor
            Developer.objects.get_or_create(company=developer, game=get_game)
            Publisher.objects.get_or_create(company=publisher, game=get_game)
            if sponsor is not None:
                Sponsor.objects.get_or_create(company=sponsor, game=get_game)
            if sponsor is None:
                try:
                    Sponsor.objects.get(game=get_game).delete()
                except Sponsor.DoesNotExist:
                    pass
            if awards:
                for a in awards:
                    AwardGameRelation.objects.get_or_create(award=a, game=get_game)
            if not awards:
                for a in AwardGameRelation.objects.filter(game=get_game):
                    a.delete()
            success = True
            game_form.save()

    context = {
        'get_game': get_game,
        'update': True,
        'game_form': game_form,
        'success_update': success,
    }

    template = 'edit_game.html'

    return render(request, template, context)


def delete_game(request, pk):
    get_game = Game.objects.get(pk=pk)
    try:
        Developer.objects.get(game=get_game).delete()
    except Developer.DoesNotExist:
        pass

    try:
        Publisher.objects.get(game=get_game).delete()
    except Publisher.DoesNotExist:
        pass

    try:
        Sponsor.objects.get(game=get_game).delete()
    except Sponsor.DoesNotExist:
        pass

    get_game.delete()

    return redirect(reverse('edit_game'))


def create_company(request):
    success = False
    company = Company.objects.all()
    form = CompanyForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            success = True

    context = {
        'company': company.order_by('id'),
        'form': CompanyForm(),
        'success': success,
    }

    template = 'edit_company.html'

    return render(request, template, context)


def update_company(request, pk):
    success = False
    get_company = Company.objects.get(pk=pk)
    form = CompanyForm(instance=get_company)

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=get_company)
        if form.is_valid():
            form.save()
            success = True

    context = {
        'get_company': get_company,
        'update': True,
        'update_form': form,
        'success_update': success,
    }

    template = 'edit_company.html'

    return render(request, template, context)


def delete_company(requst, pk):
    get_company = Company.objects.get(pk=pk)
    get_company.delete()

    return redirect(reverse('edit_company'))


def create_award(request):
    success = False
    award = Award.objects.all()
    form = AwardForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            success = True

    context = {
        'award': award.order_by('id'),
        'form': form,
        'success': success,
    }

    template = 'edit_award.html'

    return render(request, template, context)


def update_award(request, pk):
    success = False
    get_award = Award.objects.get(pk=pk)
    form = AwardForm(instance=get_award)
    if request.method == 'POST':
        form = AwardForm(request.POST, instance=get_award)
        if form.is_valid():
            form.save()
            success = True

    context = {
        'get_award': get_award,
        'update': True,
        'update_form': form,
        'success_update': success,
    }

    template = 'edit_award.html'

    return render(request, template, context)


def delete_award(request, pk):
    get_award = Award.objects.get(pk=pk)
    get_award.delete()

    return redirect(reverse('edit_award'))

"""
update
                        {% for group in request.user.groups.all %}
                            {% if group.name == 'Manager'%}
                                <td><a href="{% url 'update_game' i.pk %}">Edit</a></td>
                                <td><a href="{% url 'delete_game' i.pk %}">Delete</a></td>
                            {% endif %}
                        {% endfor %}
"""


