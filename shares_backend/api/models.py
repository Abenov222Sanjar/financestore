from django.db import models

def upload_path(instance, filename):
    return '/'.join(['media', str(instance.name), filename])

# managers:
class StatusCompleted(models.Manager):
    def get_queryset(self):
        return super(StatusCompleted, self).get_queryset().filter(status='completed')

class StatusDeclined(models.Manager):
    def get_queryset(self):
        return super(StatusDeclined, self).get_queryset().filter(status='declined')

class StatusInProgress(models.Manager):
    def get_queryset(self):
        return super(StatusInProgress, self).get_queryset().filter(status='in_progress')

class NeedToFire(models.Manager):
    def get_queryset(self):
        return super(NeedToFire, self).get_queryset().filter(amount_of_trades=0)

# abstract model:
class Base(models.Model):
    name = models.CharField(max_length=120)
    class Meta:
        abstract = True

# models:
class Category(models.Model):
    name = models.CharField(max_length=120)

class SubCategory(Base):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

class Broker(Base):
    phone = models.CharField(max_length=12)
    amount_of_trades = models.IntegerField()
    need_to_fire = NeedToFire()

class Company(models.Model):
    name = models.CharField(max_length=32)
    
class Share(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)    
    description = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to=upload_path)
    price = models.FloatField()

class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    status = models.CharField(max_length=20)
    share = models.ForeignKey(Share, on_delete=models.CASCADE, blank=True, null=True)
    attached_broker = models.ForeignKey(Broker, on_delete=models.CASCADE, blank=True, null=True)

    completed = StatusCompleted()
    declined = StatusDeclined()
    in_progress = StatusInProgress()