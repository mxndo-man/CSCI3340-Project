from django.core.exceptions import PermissionDenied
from django.db import transaction

from apps.accounts.models import CustomUser

from .models import Board, Membership
from .permissions import is_owner


@transaction.atomic
def create_user_board(user: CustomUser, name: str, description: str = "") -> Board:
    """Creates a user board for when the board is created.

    Attributes:
        user: The user creating the board.
        name: name of the board.
        description: a description of the board.
    Returns:
        object type board

    """
    board = Board.objects.create(created_by=user, name=name, description=description)
    Membership.objects.create(board=board, user=user, role=Membership.Role.OWNER)

    return board


def join_by_code(user: CustomUser, join_code: str = "") -> Board:
    """Join the member by the code give by the Owner.

    Attributes:
        user: The user that is joining.
        join_code: The code given by the owner.
    Returns:
        A board to determine what board the user joined

    """
    board = Board.objects.get(join_code=join_code.strip())
    Membership.objects.get_or_create(
        board=board, user=user, defaults={"role": Membership.Role.MEMBER}
    )
    return board


def remove_member(actor: CustomUser, target_user: CustomUser, board: Board) -> None:
    """To remove ta member from the board.

    Attributes:
        actor: The owner committing the action.
        target_user: The user leaving.
        board: The board associated to the action.
    Raise:
        A 404/403 page if the actor does not have permission.
        A ValueError if the owner tries to remove themselves.

    """
    if not is_owner(user=actor, board=board):
        raise PermissionDenied()

    target = Membership.objects.get(board=board, user=target_user)

    if target.role == Membership.Role.OWNER:
        raise ValueError("Owner cannot be removed.")

    target.delete()


def leave_board(user: CustomUser, board: Board) -> None:
    """If a member wants to leaves the board they are in.

    Attributes:
        user: The user leaving the board.
        board: The board that the user is leaving.
    Raise:
        A value error if the owner tries to leave.


    """
    target = Membership.objects.get(board=board, user=user)

    if target.role == Membership.Role.OWNER:
        raise ValueError("Owner Cannot leave the board")

    target.delete()
