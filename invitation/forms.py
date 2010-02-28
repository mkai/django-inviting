from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationForm


def save_user(form_instance, profile_callback=None):
    """Creates a new **active** user from form data.

    This method is intended to replace the ``save`` of
    ``django-registration``s ``RegistrationForm``. Calls
    ``profile_callback`` if provided. Required form fields
    are ``username``, ``email`` and ``password1``.
    """
    username = form_instance.cleaned_data['username']
    email = form_instance.cleaned_data['email']
    password = form_instance.cleaned_data['password1']
    new_user = User.objects.create_user(username, email, password)
    new_user.save()
    if profile_callback is not None:
        profile_callback(user=new_user)
    return new_user


class InvitationForm(forms.Form):
    email = forms.EmailField()


class RegistrationFormInvitation(RegistrationForm):
    """
    Subclass of ``registration.RegistrationForm`` that creates an active user.
    """
    save = save_user