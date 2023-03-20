from django.db import models
from django_random_id_model import RandomIDModel
## alternatively can try UUID, very big integers are not supported by SQLite

## contains three recursive relationships but old one (using fields legacy_parent, sal_latname, sal_authors)
## is not supported anymore; fields aren't removed (if alternative classification would be needed)
## standard classification (fixed hierarchy) used fields: level, and parent
class Name (models.Model):
    pnid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, blank=True, default="vascular") ## FIXME: error prone 
    latname = models.CharField(max_length=150, blank=True)  ## when entirely normalized, must be one word
    authors = models.CharField(max_length=150, blank=True)
    colnames = models.CharField(max_length=150, blank=True) ## separated by comma, only most common ones to be shown in views, 
    longname = models.CharField(max_length=250, blank=True) ## is it in use? Could it be removed?
    note = models.TextField(blank=True)                 ## for private usage (admins)
    caption = models.TextField(blank=True, default="")  ## for public view, both should accept XHTML fragments, i.e. may contain <i>...</i>
    excluded = models.BooleanField(default=False) ## i.e, the taxon could to be deleted
    disabled = models.BooleanField(default=False, verbose_name="legacy only") ## similar to excluded, perhaps one of them could be deleted in future versions

    ## flexible hierarchy:
    rank = models.CharField(max_length=50, blank=True, verbose_name="actual rank") ## by mistake was called level in very first versions
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    ## fixed hierarchy:
    level = models.CharField(max_length=50, blank=True) ## group, etc = elementName , was called rank in very first versions
    upper = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="Fid_Gid") ## 
    
    ## legacy classification:
    legacy_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="legacy_upper")
    sal_latname = models.CharField(max_length=150, blank=True) ## sal name if not  = ccss
    sal_authors = models.CharField(max_length=150, blank=True)    

    ## technicall, auto filled
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uid = models.CharField(max_length=10, blank=True, default="") ## auto filled if empty: see admin.py

    def __str__(self):
        return("%s: %s / %s" % (self.pnid, self.latname, self.sal_latname))

    class Meta:
        verbose_name_plural = 'NameRecords'

class CommonName(models.Model):
    ref_name = models.ForeignKey(Name, on_delete=models.RESTRICT)
    colname = models.CharField(max_length=150, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return("%s: %s [%s]" % (self.ref_name.latname, self.colname, self.created))

    class Meta:
        unique_together = ('ref_name', 'colname')

class NameAnnotation(RandomIDModel):
    ## with RandomIDModel id appears in form ! Set exclude in admin
    plant = models.ForeignKey(Name, on_delete=models.RESTRICT)
    note = models.TextField(max_length=520, blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    page = models.TextField(max_length=520, blank=True, null=True) ## link to salicicola page must be started with /
    cached = models.CharField(max_length=255, blank=True, null=True, help_text="saved filename") ## applied only if kind = photo
    ## slugField should not contains period though "the value in the SlugField is only checked in forms, not in the database." ## could add custom save() [see below example] but hardly needed
    kind = models.CharField(max_length=50, choices = (
            ('', ''),
            ('note', 'note without photo'),
            ('photo', 'photo'),
            ('sample', 'to sample'),
            ('check', 'relocate'),
            ('invasive_link', 'invasive link'), ## must have page or url non empty
        )) 
    by = models.CharField(max_length=50,  blank=True, null=True) ## AZ , blank=True, default=""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return("%s: [%s] %s %s" % (self.pk, self.plant, self.kind, self.url))
    
## must not be empty: all taxa (at least vascular) at species level must have meta record
class SpeciesMeta (models.Model):
    spid = models.IntegerField(primary_key=True) ## == pnid or ccss ???
    species = models.OneToOneField(Name, blank=True, null=True, unique=True, on_delete=models.RESTRICT)  ## from foreign since it is unique
    evergreen=models.CharField(max_length=150, blank=True)
    introduced=models.CharField(max_length=150, blank=True, verbose_name="NonNative")
    invasive_mipag=models.CharField(max_length=150, blank=True)
    invasive=models.CharField(max_length=150, default="", blank=True)
    origin=models.CharField(max_length=150, blank=True)
    rare=models.CharField(max_length=150, blank=True)
    updated=models.DateTimeField(auto_now=True)
    ## from CCSS
    counties=models.CharField(max_length=150, blank=True, default="* * * * * * * * * * * * * *")
    counties_changed_from = models.CharField(max_length=150, blank=True)
    status=models.CharField(max_length=150, blank=True)
    initial_name = models.CharField(max_length=150, blank=True)
    rank = models.CharField(max_length=150, blank=True, default="species")
    notes = models.TextField(blank=True, null=True, default="")
    
    def __str__(self):
        return str(self.spid)
    class Meta:
        verbose_name_plural = 'SpeciesMeta'
