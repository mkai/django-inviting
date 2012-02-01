from django.dispatch import Signal


invitation_added = Signal(providing_args=['user', 'count'])

invitation_sent = Signal(providing_args=['invitation'])

invitation_accepted = Signal(providing_args=['invitation', 'inviting_user', 'new_user'])
