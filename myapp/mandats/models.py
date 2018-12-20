from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse

# Used to generate URLs by reversing the URL patterns


# Create your models here.
"""class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='Dakar')
"""


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(default=0)

    # london = UserProfileManager()

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Fournisseurs(models.Model):
    CODE_CAT_SOCIO = (
        ('Mltr', 'Millitaire'),
        ('DCG', 'Directeurs, cadres de direction et gérants'),
        ('PIS', 'Professions intellectuelles et scientifiques'),
        ('PI', 'Professions intermédiares'),
        ('ETA', 'Employés de type administratif'),
        ('PCV', 'Personnel des services directs aux particuliers, commerçants et vendeurs '),
        ('Cmrct', 'Agriculteurs et ouvriers qualifiés de l’agriculture, de la sylviculture et de la pêche '),
        ('IA', 'Métiers qualifiés de l’industrie et de l’artisanat '),
        ('CO', 'Conducteurs d installations et de machines et ouvriers de l’assemblage'),
        ('PE', 'Professions élémentaires'),
    )
    CODE_SECTEUR = (
        ('AEAcS', 'Agriculteur, élevage et activités de stockage des produits d’origine végétale, animale ou '
                  'halieutique'),
        ('AMPT', 'Activités manufacturières de production et de transformation'),
        ('SM', 'Extraction ou transformation de substances minérales'),
        ('TAI', 'Tourisme, aménagements et industries touristiques, autres activités hôtelières'),
        ('IndCult', 'Industries culturelles (livre, disque, cinéma, centres de documentation, centre de production '
                    'audio visuelle, etc'),
        ('Services', 'Services exercés dans les sous - secteurs suivants: santé, éducation et formation montage et '
                     'maintenance d’équipements industriels, télé - services, transports aériens et maritimes'),
        ('Ipaf', 'infrastructures portuaires, aéroportuaires et ferroviaires'),
        ('RCPZCyCa', 'réalisation de complexes commerciaux, parcs industriels, zones touristiques, cybervillages et '
                     'centres artisanaux'),
    )
    CODE_TYP_TIERS = (
        ('M', 'Morale'),
        ('P', 'Physique'),
    )
    ide_tiers = models.CharField(max_length=20, primary_key=True)
    code_cat_socio = models.CharField(max_length=5, choices=CODE_CAT_SOCIO, help_text="code catégorie social")
    code_secteur = models.CharField(max_length=10, choices=CODE_SECTEUR)
    nom_contrib = models.CharField(max_length=20)
    code_typ_tiers = models.CharField(max_length=1, choices=CODE_TYP_TIERS)
    nom = models.CharField(max_length=45, null=False)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prenom = models.CharField(max_length=45)
    date_fin_validite = models.DateField()
    adresse = models.CharField(max_length=32)
    ville = models.CharField(max_length=32)
    code_postal = models.CharField(max_length=10)
    boite_postal = models.CharField(max_length=10)
    pays = models.CharField(max_length=32)
    telephone = models.CharField(max_length=15)
    date_creation = models.DateField()

    class Meta:
        ordering = ['nom']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.prenom}, {self.nom}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this provider."""
        return reverse('fournisseur-detail', args=[str(self.ide_tiers)])


class Mandat(models.Model):
    COD_STATUT = (
        ('SA', 'En saisie'),
        ('AC', 'Accepté'),
        ('VI', 'Visé'),
        ('RJ', 'Rejetté'),
        ('RF', 'Refusé'),
        ('RC', 'Reçu'),
    )
    ide_piece = models.CharField(max_length=20, primary_key=True)
    cod_statut = models.CharField(max_length=2, choices=COD_STATUT, verbose_name="Le statut du mandat")
    objet = models.TextField(max_length=240)
    fournisseur = models.ForeignKey(Fournisseurs, on_delete=models.SET_NULL, null=True)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_emis = models.DateField()
    date_reception = models.DateField()
    montant = models.IntegerField()
    motif_rejet = models.CharField(max_length=45, blank=True)

    class Meta:
        ordering = ['ide_piece']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.ide_piece}, {self.objet}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this mandat."""
        return reverse('mandat-detail', args=[str(self.ide_piece)])

    """def was_received_recently(self):
        return self.date_reception >= timezone.now() - datetime.timedelta(days=1)"""


class CompteBancaire(models.Model):
    num_banque = models.IntegerField(primary_key=True)
    nom_banque = models.CharField(max_length=45)
    cpt_banque = models.CharField(max_length=45)
    fournisseur = models.ForeignKey(Fournisseurs, on_delete=models.CASCADE, verbose_name="identifiant proprietaire")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_debut_validite = models.DateField()
    date_fin_validite = models.DateField()

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.cpt_banque}, {self.num_banque}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this compte bancaire."""
        return reverse('comptebancaire-detail', args=[str(self.num_banque)])


class Reglement(models.Model):
    MOTIF_INCIDENT = (
        ('O', 'Oui'),
        ('N', 'Non'),
    )
    CODE_ETAT_RGLT = (
        ('RG', 'Réglé'),
    )
    IDE_MOD_RGLT = (
        ('Vi', 'Virement'),
        ('Au', 'Autres'),
    )
    num_reglt = models.IntegerField()
    id_reglt = models.IntegerField(primary_key=True)
    ide_mod_reglt = models.CharField(max_length=5, choices=IDE_MOD_RGLT)
    mandat = models.OneToOneField(Mandat, on_delete=models.CASCADE, verbose_name="référence mandat")
    fournisseur = models.ForeignKey(Fournisseurs, on_delete=models.CASCADE, verbose_name="identifiant fournisseurs")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    compte_bancaire = models.ForeignKey(CompteBancaire, on_delete=models.CASCADE, verbose_name="référence compte "
                                                                                               "bancaire")
    num_bank = models.CharField(max_length=32)
    nom_bank = models.CharField(max_length=20)
    montant = models.IntegerField(null=False)
    date_ref = models.DateField()
    date_echeance = models.DateField()
    code_etat_reglt = models.CharField(max_length=15, choices=CODE_ETAT_RGLT)
    motif_incident = models.CharField(max_length=45, choices=MOTIF_INCIDENT)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id_reglt}, {self.ide_mod_reglt}'


class Virement(models.Model):
    TRAITE = (
        (0, 'Génération d’un paiement'),
        (1, 'Envoie du paiement à la Trésorie Générale'),
        (4, 'Envoie du paiement à la compensation'),
    )
    reference = models.CharField(max_length=8, primary_key=True)
    reglement = models.OneToOneField(Reglement, on_delete=models.CASCADE,
                                     verbose_name="Informations sur le réglement")
    typ_operation = models.CharField(max_length=3)
    typ_rib_donneur = models.CharField(max_length=1)
    rib_donneur = models.CharField(max_length=24)
    typ_rib_beneficiaire = models.CharField(max_length=1)
    rib_beneficiaire = models.CharField(max_length=24)
    montant = models.IntegerField()
    nom_donneur = models.CharField(max_length=35)
    adresse_donneur = models.CharField(max_length=50)
    fournisseur = models.ForeignKey(Fournisseurs, on_delete=models.CASCADE, verbose_name="références au bénéficiaire")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordre = models.DateField()
    mandat = models.ForeignKey(Mandat, on_delete=models.CASCADE)
    traite = models.IntegerField(choices=TRAITE)
    date_paiement = models.DateField()

    class Meta:
        ordering = ['date_paiement']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.reference}, {self.montant}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this virement."""
        return reverse('virement-detail', args=[str(self.reference)])
