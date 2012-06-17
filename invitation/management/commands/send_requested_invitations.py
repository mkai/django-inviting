"""
A management command that creates and sends invitations to users that have
requested an invitation before.

"""
from optparse import make_option
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.auth.models import User
from invitation.models import Invitation, InvitationRequest


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--count', '-c', default=0, dest='count',
            help='How many invitations to send.'),
        make_option('--from-username', '-u', default=None,
            dest='from_username',
            help='A username from whom the invitations are sent.'),
        make_option('--subject-template', '-s', default=None,
            dest='subject_template_name',
            help='Path to a template to use for the email subject.'),
        make_option('--message-template', '-m', default=None,
            dest='message_template_name',
            help='Path to a template to use for the email body.'),
        make_option('-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help='Don\'t send anything, just show who would be invited.'),
    )
    help = 'Send an invitation to users that requested one'

    def handle_noargs(self, *args, **options):
        count = options.get('count')
        from_username = options.get('from_username')
        subject_template_name = options.get('subject_template_name')
        message_template_name = options.get('message_template_name')
        dry_run = options.get('dry_run')
        verbose = int(options.get('verbosity')) > 1
        if not count or not from_username:
            self.stderr.write('Usage example: send_requested_invitations '
                              '--count=100 --from_username=admin\n')
            return
        try:
            from_user = User.objects.get(username=from_username)
        except User.DoesNotExist:
            raise CommandError('User "%s" does not exist.' % from_username)
        requests =\
            InvitationRequest.objects.order_by('date_requested')[:count]
        # this works around the "maximum invitations per user" limit by raising
        # the from_user's number of available invitations
        actual_count = requests.count()
        if not dry_run:
            from_user.invitation_stats.add_available(count=actual_count)
        if verbose:
            self.stdout.write('Raised %s\'s available invitations by %d\n' % (
                from_user.username, actual_count))
        for request in requests:
            if verbose:
                self.stdout.write('Will invite %s\n' % request.email)
            if dry_run:
                continue
            invitation = Invitation.objects.invite(user=from_user, 
                                                   email=request.email)
            invitation.send_email(subject_template_name=subject_template_name,
                                  message_template_name=message_template_name)
        if not dry_run:
            self.stdout.write('%d invitations were sent.\n' % requests.count())
