from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import CustomUser
from apps.boards.models import Board, Membership

from .models import Notification


@receiver(post_save, sender=CustomUser)
def create_welcome_notification(sender, instance, created, **kwargs):
    if not created:
        return

    Notification.objects.create(
        user=instance,
        kind=Notification.Kind.WELCOME,
        title="Welcome!",
        message="Your account has been created successfully. Make connections and find opportunities!",
        dedupe_key=f"WELCOME:{instance.pk}",
    )


@receiver(post_save, sender=Board)
def notify_board_created(sender, instance, created, **kwargs):
    if not created or instance.created_by is None:
        return

    Notification.objects.create(
        user=instance.created_by,
        kind=Notification.Kind.NEW_BOARD,
        title="Nice Board!",
        message=f'You created a board called "{instance.name}". Great Job!',
        dedupe_key=f"NEW_BOARD:{instance.pk}",
    )


@receiver(post_save, sender=Membership)
def notify_member_joined(sender, instance, created, **kwargs):
    if not created or instance.role != Membership.Role.MEMBER:
        return

    Notification.objects.create(
        user=instance.user,
        kind=Notification.Kind.MEMBER_JOINED,
        title="A Step Towards Success!",
        message=f'You joined a board called "{instance.board.name}". Great Job!',
        dedupe_key=f"MEMBER_JOINED:{instance.pk}:JOINER",
    )

    owner = instance.board.created_by
    if owner is not None:
        Notification.objects.create(
            user=owner,
            kind=Notification.Kind.MEMBER_JOINED,
            title="A Member Joined Your Board",
            message=f'{instance.user.username} joined your board "{instance.board.name}". Welcome them!',
            dedupe_key=f"MEMBER_JOINED:{instance.pk}:OWNER",
        )
