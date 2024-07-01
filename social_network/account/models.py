from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d", blank=True)


    def __str__(self):
        return self.user.username


class Contact(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"],
    user_from = models.ForeignKey("auth.User", related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey("auth.User", related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"

user_model = get_user_model()
user_model.add_to_class("following", models.ManyToManyField("self", through=Contact, related_name="followers", symmetrical=False))