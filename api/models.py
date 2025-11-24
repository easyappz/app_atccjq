from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Member(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'members'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password is correct"""
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        """Always return True for authenticated members"""
        return True

    @property
    def is_anonymous(self):
        """Always return False for members"""
        return False

    def has_perm(self, perm, obj=None):
        """Check if member has a specific permission"""
        return True

    def has_module_perms(self, app_label):
        """Check if member has permissions to view the app"""
        return True


class Message(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['member', 'created_at']),
        ]

    def __str__(self):
        return f"{self.member.username}: {self.text[:50]}"
