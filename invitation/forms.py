from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from invitation.models import Invitation, InvitationRequest


def save_user(form_instance, profile_callback=None):
    """
    Create a new **active** user from form data.

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


class InvitationRequestForm(forms.ModelForm):
    """
    A form that lets users enter their email address to request an invitation.
    """
    class Meta:
        fields = ('email',)
        model = InvitationRequest

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Invitation.objects.valid().get(email=email)
        except Invitation.DoesNotExist:
            return email
        raise forms.ValidationError(_('An invitation has already been sent'
                                      ' to this email address.'))


class RegistrationFormInvitation(RegistrationForm):
    """
    Subclass of ``registration.RegistrationForm`` that create an **active**
    user.

    Since registration is (supposedly) done via invitation, no further
    activation is required. For this reason ``email`` field always return
    the value of ``email`` argument given the constructor.
    """
    def __init__(self, email, *args, **kwargs):
        super(RegistrationFormInvitation, self).__init__(*args, **kwargs)
        self._make_email_immutable(email)

    def _make_email_immutable(self, email):
        self._email = self.initial['email'] = email
        if 'email' in self.data:
            self.data = self.data.copy()
            self.data['email'] = email
        self.fields['email'].widget.attrs.update({'readonly': True})

    def clean_email(self):
        return self._email

    save = save_user
