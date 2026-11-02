import secrets
from typing import ClassVar

from django.conf import settings
from django.db import IntegrityError, models, transaction


class Board(models.Model):
    """The board where the users are able to configure their friend space/board

    Attributes:
        name: a char field of max length 100.
        description: a description of the user's board.
        join_code: a secret url code for the user's to communicate in private board.
        created_by: Links the board to the users by db.
        created_at: A timestamp of the board when it was created.
        updated_at: A timestamp of the board when it was updated.

    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    join_code = models.CharField(max_length=12, unique=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Function to save join_code

        token_urlsafe(9) is in bytes so it will use the correct amount of max_length of 12.

        Args:
            *args: Tuple of annoymous values
            **kwargs: Keyword argurments that is a dict

        Returns:
            updates join_code:
        Raises:
            An error if the function could not generate a join_code.
        """
        if self.join_code:
            return super().save(*args, **kwargs)
        for _ in range(5):  # some random value tbh
            self.join_code = secrets.token_urlsafe(9)
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                continue
        raise IntegrityError("Error Generating the join code. ")


class Membership(models.Model):
    class Role(models.TextChoices):
        """A role class to determine the users rights.
        Attributes:
            OWNER: the owner of the board
            MEMBER: the member of the board

        """

        OWNER = "OWNER"
        MEMBER = "MEMBER"

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                fields=["board", "user"], name="one_membership_per_user"
            ),
        ]
