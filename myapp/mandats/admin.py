from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Fournisseurs, Mandat, CompteBancaire, Reglement, Virement, User, UserProfile


# Register your models here.
# admin.site.register(Mandat)
# Define the admin class

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_info', 'city', 'phone')

    def user_info(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-phone', 'user')
        return queryset

    user_info.short_description = 'Info'


admin.site.register(UserProfile, UserProfileAdmin)


@admin.register(Mandat)
class MandatAdmin(admin.ModelAdmin):
    list_display = ('ide_piece', 'objet', 'cod_statut', 'fournisseur', 'date_emis', 'date_reception')


class MandatInline(admin.TabularInline):
    model = Mandat


# admin.site.register(Fournisseurs)
@admin.register(Fournisseurs)
class FournisseursAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'utilisateur', 'date_creation', 'date_fin_validite')
    inlines = [MandatInline]


# admin.site.register(CompteBancaire)
@admin.register(CompteBancaire)
class CompteBancaireAdmin(admin.ModelAdmin):
    list_display = (
        'nom_banque', 'cpt_banque', 'fournisseur', 'utilisateur', 'date_debut_validite', 'date_fin_validite')


class VirementInline(admin.TabularInline):
    model = Virement


# admin.site.register(Reglement)
@admin.register(Reglement)
class ReglementBAdmin(admin.ModelAdmin):
    list_filter = ('ide_mod_reglt', 'utilisateur', 'date_echeance')
    inlines = [VirementInline]


# admin.site.register(Virement)
@admin.register(Virement)
class VirementAdmin(admin.ModelAdmin):
    list_display = (
        'mandat', 'reference', 'montant', 'utilisateur', 'nom_donneur', 'fournisseur', 'traite', 'date_ordre',
        'date_paiement')
