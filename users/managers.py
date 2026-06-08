from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_account(self, email, password, **extra_fields):
        normalized_email = self.normalize_email(email)
        account = self.model(email=normalized_email, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        return self._create_account(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self._create_account(email, password, **extra_fields)
