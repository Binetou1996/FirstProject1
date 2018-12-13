from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Mandat, CompteBancaire, Fournisseurs, Reglement, Virement
from django.contrib.auth import login, authenticate
from .forms import SignupForm, EditProfileForm, FournisseurForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from contact_form.views import ContactFormView
from .forms import FoundationContactForm



def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_mandats = Mandat.objects.all().count()
    num_virements = Virement.objects.all().count()

    # Available books (status = 'a')
    num_virements_available = Virement.objects.filter(traite=4).count()

    # The 'all()' is implied by default.
    num_fournisseurs = Fournisseurs.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_mandats': num_mandats,
        'num_virements': num_virements,
        'num_virements_available': num_virements_available,
        'num_fournisseurs': num_fournisseurs,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class MandatListView(generic.ListView):
    model = Mandat
    paginate_by = 2


class MandatDetailView(generic.DetailView):
    model = Mandat


class FournisseurListView(generic.ListView):
    model = Fournisseurs
    paginate_by = 2
    template_name = 'mandats/fournisseur_list.html'


class FournisseurDetailView(generic.DetailView):
    model = Fournisseurs
    template_name = 'mandats/fournisseur_detail.html'


class VirementListView(generic.ListView):
    model = Virement
    paginate = 2
    template_name = 'mandats/virement_list.html'


class VirementDetailView(generic.DetailView):
    model = Virement
    template_name = 'mandats/virement_detail.html'


class LoanedMandatByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Mandat
    template_name = 'mandats/mandat_list_utilisateur_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Mandat.objects.filter(utilisateur=self.request.user).order_by('date_emis')


class LoanedVirementByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Virement
    template_name = 'mandats/virement_list_utilisateur_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Virement.objects.filter(utilisateur=self.request.user).filter(traite=4).order_by('date_ordre')


"""def home(request):
    template = loader.get_template('mandats/login1.html')
    return HttpResponse(template.render(request=request))
    """


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activer votre compte de consultation mandat'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # return HttpResponse('S’il vous plaît confirmer votre adresse e-mail pour terminer l’enregistrement.')
            return redirect('account_activation_sent')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


def activation_complete(request):
    return render(request, 'registration/activation_complete.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('activation_complete')
        """return HttpResponse('Merci pour votre confirmation de courrier électronique. Maintenant, vous pouvez vous '
                            'connecter à votre compte.')"""
    else:
        return HttpResponse('Le lien d’activation est invalide!')


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'registration/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'registration/edit_profile.html', args)


class ContactFoundation(ContactFormView):
    form_class = FoundationContactForm
    template_name = 'mandats/foundation.html'

    def get_success_url(self):
        return reverse('contact_form_sent')


def invoice_view(request):
    form = FournisseurForm(request.POST or None)

    if form.is_valid():
        doctype = form.cleaned_data['format']
        filename = fill_template(
            'mandats/fournisseur.odt', form.cleaned_data,
            output_format=doctype)
        visible_filename = 'fournisseur.{}'.format(doctype)

        return FileResponse(filename, visible_filename)
    else:
        return render(request, 'mandats/form.html', {'form': form})