from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class KaomojiCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        # Optionally, ensure that each category name is unique within its parent category
        unique_together = ('parent', 'name',)
        # Verbose name plural can be more friendly for the admin interface
        verbose_name_plural = "categories"

    class Meta:
        verbose_name_plural = "kaomoji_categories"
    def __str__(self):
        return self.name
    def is_subcategory(self):
        return self.parent is not None
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    featured_image = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # categories = models.ManyToManyField("Category", related_name="posts")

    def __str__(self):
        return self.title

class Kaomoji(models.Model):
    kaomoji = models.CharField(max_length=255)
    category = models.ForeignKey("KaomojiCategory", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.kaomoji} in '{self.category}'"
