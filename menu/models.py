
from django.db import models
from django.contrib.auth.models import User

# To store different categories (e.g. Burgers, sides, drinks and so on)
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True) # Assuming each category has a unique name
    sort_order = models.IntegerField()
    is_active = models.BooleanField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



# The individual items that are sold
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True) # Assuming each product has a unique name
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField()
    is_featured = models.BooleanField(default=False)
    image_url = models.ImageField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
   
# Provides options (e.g. to choose amount of patties the customer wants) 
class OptionGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)    
    selection_type = models.CharField(max_length=255)
    min_select = models.IntegerField(default=0)
    max_select = models.IntegerField(default=1)
    is_active = models.BooleanField()

    class Meta:
        verbose_name_plural = "Option Groups"
    
    def __str__(self):
        return self.name

# ALTERNATIVE for the above if ever needed

#     SELECTION_CHOICES = [
#       ('SINGLE', 'Single Selection (Radio)'),
#       ('MULTIPLE', 'Multiple Selection (Checkbox)'),
#    ]
#    selection_type = models.CharField(max_length=255, choices=SELECTION_CHOICES, default='Single')


# Choices to make between e.g. beef, chicken or vegan burger
class Option(models.Model):
    name = models.CharField(max_length=255, unique=True)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField()
    option_group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Options"

    def __str__(self):
        return self.name
    

# Stores a group for each product since some items may not have the same group (e.g. A drink can have different sizes which can be grouped into one,
# but a classic burger would not have the same group as the choices are not given on size but the "patty temperature").
# It also allows us to set a custom price for an option group that only applies to a specific product.
class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(OptionGroup, on_delete=models.CASCADE)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)