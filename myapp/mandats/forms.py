from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
import logging
from contact_form.forms import ContactForm
from django.db import transaction

from .models import Fournisseurs


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True)
    fournisseur = forms.ModelChoiceField(
        queryset=Fournisseurs.objects.all(),
        widget=forms.Select,
        required=True
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'fournisseur', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        fournisseur = self.cleaned_data.get('fournisseur')
        user = super().save()
        #fournisseur = Fournisseurs.objects.get(ide_tiers=fournisseur)
        user.fournisseurs_set.add(fournisseur)
        user.save()
        return user



class EditProfileForm(UserChangeForm):
    template_name = '/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )


''# logger = logging.getLogger(__name__)


class BaseContactForm(ContactForm):
    message_subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'required', 'placeholder': 'Message subject'}),
        label='Message subject',
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'required', 'placeholder': 'E-mail'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'required', 'placeholder': 'Name'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'required', 'placeholder': 'Your message'}))

    def subject(self):
        # Strip all linebreaks from the subject string.
        subject = ''.join(self.cleaned_data["message_subject"].splitlines())
        return "[Contact form] " + subject

    def message(self):
        return "From: {name} <{email}>\n\n{body}".format(**self.cleaned_data)

    """def clean_body(self):
        
        # Check spam against Akismet.

        # Backported from django-contact-form pre-1.0; 1.0 dropped built-in
        # Akismet support.
        
        if 'body' in self.cleaned_data and getattr(settings, 'AKISMET_API_KEY', None):
            try:
                akismet_api = Akismet(
                    api_key=settings.AKISMET_API_KEY,
                    blog_url='http://%s/' % Site.objects.get_current().domain,
                    user_agent='Django {}.{}.{}'.format(*django.VERSION)
                )

                akismet_data = {
                    'user_ip': self.request.META.get('REMOTE_ADDR', ''),
                    'user_agent': self.request.META.get('HTTP_USER_AGENT', ''),
                    'referrer': self.request.META.get('HTTP_REFERER', ''),
                    'comment_content': force_bytes(self.cleaned_data['body']),
                    'comment_author': self.cleaned_data.get('name', ''),
                }
                if getattr(settings, 'AKISMET_TESTING', None):
                    # Adding test argument to the request in order to tell akismet that
                    # they should ignore the request so that test runs affect the heuristics
                    akismet_data['test'] = 1
                if akismet_api.check(akismet_data):
                    raise forms.ValidationError("Akismet thinks this message is spam")
            except AkismetServerError:
                logger.error('Akismet server error')
        return self.cleaned_data['body']
    """


class FoundationContactForm(BaseContactForm):
    recipient_list = ["gouvtresor@gmail.com"]

"""
class FournisseurForm(forms.Form):
    FORMAT_CHOICES = (
        ('pdf', 'PDF'),
        ('docx', 'MS Word'),
        ('html', 'HTML'),
    )
    number = forms.CharField(label='Fournisseur #')
    fournisseur = forms.ModelChoiceField(queryset=Fournisseurs.objects.all())
    subject = forms.CharField()
    amount = forms.DecimalField()
    format = forms.ChoiceField(choices=FORMAT_CHOICES)
"""