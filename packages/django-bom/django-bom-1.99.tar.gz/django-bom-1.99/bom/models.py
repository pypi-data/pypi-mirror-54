from __future__ import unicode_literals

import logging

from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .utils import increment_str
from .validators import alphanumeric, numeric

from social_django.models import UserSocialAuth

logger = logging.getLogger(__name__)


class Organization(models.Model):
    name = models.CharField(max_length=255, default=None)
    subscription = models.CharField(max_length=1, choices=(('F', 'Free'), ('P', 'Pro'),))
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    google_drive_parent = models.CharField(max_length=128, blank=True, default=None, null=True)

    def __str__(self):
        return u'%s' % (self.name)


class UserMeta(models.Model):
    user = models.OneToOneField(User, db_index=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.PROTECT)
    role = models.CharField(max_length=1, choices=(('A', 'Admin'), ('V', 'Viewer'),))

    def google_authenticated(self):
        try:
            self.user.social_auth.get(provider='google-oauth2')
            return True
        except UserSocialAuth.DoesNotExist:
            return False


def _user_meta(self, organization=None):
    return UserMeta.objects.get_or_create(
        user=self, defaults={
            'organization': organization})[0]


User.add_to_class('bom_profile', _user_meta)


class PartClass(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255, default=None)
    comment = models.CharField(max_length=255, default=None, blank=True)

    def __str__(self):
        return u'%s' % (self.code + ': ' + self.name)


class Manufacturer(models.Model):
    name = models.CharField(max_length=128, default=None)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u'%s' % (self.name)


# Numbering scheme is hard coded for now, may want to change this to a
# setting depending on a part numbering scheme
# Part contains the root information for a component. Parts have attributes that can be changed over time
# (see PartRevision). Part numbers can be changed over time, but these cannot be tracked, as it is not a practice
# that should be done often.
class Part(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    number_class = models.ForeignKey(PartClass, default=None, related_name='number_class', on_delete=models.PROTECT)
    number_item = models.CharField(max_length=4, default=None, blank=True, validators=[numeric])
    number_variation = models.CharField(max_length=2, default=None, blank=True, validators=[alphanumeric])
    primary_manufacturer_part = models.ForeignKey('ManufacturerPart', default=None, null=True, blank=True,
                                                  on_delete=models.SET_NULL, related_name='primary_manufacturer_part')
    google_drive_parent = models.CharField(max_length=128, blank=True, default=None, null=True)

    class Meta():
        unique_together = ['number_class', 'number_item', 'number_variation', 'organization', ]

    def full_part_number(self):
        return "{0}-{1}-{2}".format(self.number_class.code, self.number_item, self.number_variation)

    def description(self):
        return self.latest().description if self.latest() is not None else ''

    def latest(self):
        return self.revisions().order_by('-id').first()

    def revisions(self):
        return PartRevision.objects.filter(part=self)

    def seller_parts(self):
        manufacturer_parts = ManufacturerPart.objects.filter(part=self)
        return SellerPart.objects.filter(manufacturer_part__in=manufacturer_parts) \
            .order_by('seller', 'minimum_order_quantity')

    def manufacturer_parts(self):
        manufacturer_parts = ManufacturerPart.objects.filter(part=self)
        return manufacturer_parts

    def where_used(self):
        revisions = PartRevision.objects.filter(part=self)
        used_in_subparts = Subpart.objects.filter(part_revision__in=revisions)
        used_in_assembly_ids = AssemblySubparts.objects.filter(subpart__in=used_in_subparts).values_list('assembly',
                                                                                                         flat=True)
        used_in_prs = PartRevision.objects.filter(assembly__in=used_in_assembly_ids)
        return used_in_prs

    def where_used_full(self):
        def where_used_given_part(used_in_parts, part):
            where_used = part.where_used()
            used_in_parts.update(where_used)
            for p in where_used:
                where_used_given_part(used_in_parts, p)
            return used_in_parts

        used_in_parts = set()
        where_used_given_part(used_in_parts, self)
        return list(used_in_parts)

    def indented(self, part_revision=None):
        if part_revision is None:
            return self.latest().indented() if self.latest() is not None else None
        else:
            return part_revision.indented()

    def optimal_seller(self, quantity=None):
        if quantity is None:
            qty_cache_key = str(self.id) + '_qty'
            quantity = int(cache.get(qty_cache_key, 100))

        manufacturer_parts = ManufacturerPart.objects.filter(part=self)
        sellerparts = SellerPart.objects.filter(manufacturer_part__in=manufacturer_parts)
        return SellerPart.optimal(sellerparts, quantity)

    def save(self, **kwargs):
        no_part_revision = kwargs.get('no_part_revision', False)
        if self.number_item is None or self.number_item == '':
            last_number_item = Part.objects.filter(
                number_class=self.number_class,
                organization=self.organization).order_by('number_item').last()
            if not last_number_item:
                self.number_item = '0001'
            else:
                self.number_item = "{0:0=4d}".format(
                    int(last_number_item.number_item) + 1)
        if self.number_variation is None or self.number_variation == '':
            last_number_variation = Part.objects.all().filter(
                number_class=self.number_class,
                number_item=self.number_item).order_by('number_variation').last()

            if not last_number_variation:
                self.number_variation = '01'
            else:
                try:
                    self.number_variation = "{0:0=2d}".format(int(last_number_variation.number_variation) + 1)
                except ValueError as e:
                    self.number_variation = "{}".format(increment_str(last_number_variation.number_variation))
        super(Part, self).save()
        if self.latest() is None and not no_part_revision:
            PartRevision.objects.create(part=self, revision='1')

    def __str__(self):
        return u'%s' % (self.full_part_number())


# Below are attributes of a part that can be changed, but it's important to trace the change over time
class PartRevision(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, db_index=True)
    timestamp = models.DateTimeField(default=timezone.now)
    configuration = models.CharField(max_length=1, choices=(('R', 'Released'), ('W', 'Working'),), default='W')
    description = models.CharField(max_length=255, default="")
    revision = models.CharField(max_length=4, db_index=True)
    attribute = models.CharField(max_length=255, default=None, null=True, blank=True)
    value = models.CharField(max_length=255, default=None, null=True, blank=True)
    assembly = models.ForeignKey('Assembly', default=None, null=True, on_delete=models.PROTECT, db_index=True)

    class Meta:
        unique_together = (('part', 'revision'),)

    def save(self, **kwargs):
        if self.assembly is None:
            assy = Assembly.objects.create()
            self.assembly = assy
        if self.id:
            previous_configuration = PartRevision.objects.get(id=self.id).configuration
            if self.configuration != previous_configuration:
                self.timestamp = timezone.now()
        super(PartRevision, self).save()

    def indented(self):
        def indented_given_bom(bom, part_revision, parent=None, qty=1, parent_qty=1, indent_level=0, subpart=None,
                               reference=''):
            if part_revision is None:  # hopefully this never happens
                logger.warning("Indented bom part_revision is None, this shouldn't happen, parent "
                               "part_revision id: {}".format(parent.id))
                return

            bom.append({
                'part': part_revision.part,
                'part_revision': part_revision,
                'quantity': qty,
                'parent_quantity': parent_qty,
                'total_quantity': parent_qty * qty,
                'indent_level': indent_level,
                'parent_id': parent.id if parent is not None else None,
                'subpart': subpart,
                'reference': reference,
            })

            indent_level = indent_level + 1
            if part_revision is None or part_revision.assembly is None or part_revision.assembly.subparts.count() == 0:
                return
            else:
                parent_qty *= qty
                for sp in part_revision.assembly.subparts.all():
                    qty = sp.count
                    reference = sp.reference
                    indented_given_bom(bom, sp.part_revision, parent=part_revision, qty=qty, parent_qty=parent_qty,
                                       indent_level=indent_level, subpart=sp, reference=reference)

        bom = []
        indented_given_bom(bom, self)
        return bom

    def flat(self):
        def flat_given_bom(bom, part_revision, parent=None, qty=1, parent_qty=1, subpart=None, reference=''):
            if part_revision is None:  # hopefully this never happens
                logger.warning("Indented bom part_revision is None, this shouldn't happen, parent "
                               "part_revision id: {}".format(parent.id))
                return

            if part_revision.id in bom:
                bom[part_revision.id]['quantity'] += parent_qty * qty
                ref = ', ' + reference if reference != '' else ''
                bom[part_revision.id]['references'] += ref
            else:
                bom[part_revision.id] = {
                    'part': part_revision.part,
                    'part_revision': part_revision,
                    'quantity': qty,
                    'references': reference,
                }

            if part_revision is None or part_revision.assembly is None or part_revision.assembly.subparts.count() == 0:
                return
            else:
                parent_qty *= qty
                for sp in part_revision.assembly.subparts.all():
                    qty = sp.count
                    reference = sp.reference
                    flat_given_bom(bom, sp.part_revision, parent=part_revision, qty=qty, parent_qty=parent_qty,
                                   subpart=sp, reference=reference)

        bom = {}
        flat_given_bom(bom, self)
        return bom

    def where_used(self):
        # Where is a part_revision used???
        # it gets used by being a subpart to an assembly of a part_revision
        # so we can look up subparts, then their assemblys, then their partrevisions
        used_in_subparts = Subpart.objects.filter(part_revision=self)
        used_in_assembly_ids = AssemblySubparts.objects.filter(subpart__in=used_in_subparts).values_list('assembly',
                                                                                                         flat=True)
        used_in_pr = PartRevision.objects.filter(assembly__in=used_in_assembly_ids)
        return used_in_pr

    def where_used_full(self):
        def where_used_given_part(used_in_parts, part):
            where_used = part.where_used()
            used_in_parts.update(where_used)
            for p in where_used:
                where_used_given_part(used_in_parts, p)
            return used_in_parts

        used_in_parts = set()
        where_used_given_part(used_in_parts, self)
        return list(used_in_parts)

    def next_revision(self):
        try:
            return int(self.revision) + 1
        except ValueError:
            return increment_str(self.revision)

    def __str__(self):
        return u'{}, Rev {}'.format(self.part.full_part_number(), self.revision)


class AssemblySubparts(models.Model):
    assembly = models.ForeignKey('Assembly', models.CASCADE)
    subpart = models.ForeignKey('Subpart', models.CASCADE)

    class Meta:
        db_table = 'bom_assembly_subparts'
        unique_together = (('assembly', 'subpart'),)


class Subpart(models.Model):
    part_revision = models.ForeignKey('PartRevision', related_name='assembly_subpart', null=True,
                                      on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    reference = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return u'{} {}'.format(self.part_revision, self.count)


class Assembly(models.Model):
    subparts = models.ManyToManyField(Subpart, related_name='assemblies', through='AssemblySubparts')


class ManufacturerPart(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    manufacturer_part_number = models.CharField(
        max_length=128, default='', blank=True)
    manufacturer = models.ForeignKey(
        Manufacturer, default=None, blank=True, null=True, on_delete=models.PROTECT)

    class Meta():
        unique_together = [
            'part',
            'manufacturer_part_number',
            'manufacturer']

    def seller_parts(self):
        return SellerPart.objects.filter(manufacturer_part=self).order_by('seller', 'minimum_order_quantity')

    def optimal_seller(self, quantity=None):
        if quantity is None:
            qty_cache_key = str(self.part.id) + '_qty'
            quantity = int(cache.get(qty_cache_key, 100))
        sellerparts = SellerPart.objects.filter(manufacturer_part=self)
        return SellerPart.optimal(sellerparts, quantity)

    def __str__(self):
        return u'%s' % (self.manufacturer_part_number)


class Seller(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default=None)

    def __str__(self):
        return u'%s' % (self.name)


class SellerPart(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    manufacturer_part = models.ForeignKey(ManufacturerPart, on_delete=models.CASCADE)
    minimum_order_quantity = models.IntegerField(default=1)
    minimum_pack_quantity = models.IntegerField(default=1)
    data_source = models.CharField(max_length=32, default=None, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=8, decimal_places=4)
    lead_time_days = models.IntegerField(null=True, blank=True)
    nre_cost = models.DecimalField(max_digits=8, decimal_places=4)
    ncnr = models.BooleanField(default=False)

    class Meta():
        unique_together = [
            'seller',
            'manufacturer_part',
            'minimum_order_quantity',
            'unit_cost']

    @staticmethod
    def optimal(sellerparts, quantity):
        seller = None
        for sellerpart in sellerparts:
            if seller is None:
                seller = sellerpart
            else:
                new_quantity = quantity if sellerpart.minimum_order_quantity < quantity else sellerpart.minimum_order_quantity
                new_total_cost = new_quantity * sellerpart.unit_cost
                old_quantity = quantity if seller.minimum_order_quantity < quantity else seller.minimum_order_quantity
                old_total_cost = old_quantity * seller.unit_cost
                if new_total_cost < old_total_cost:
                    seller = sellerpart
        return seller

    def __str__(self):
        return u'%s' % (self.manufacturer_part.part.full_part_number() + ' ' + self.seller.name)
