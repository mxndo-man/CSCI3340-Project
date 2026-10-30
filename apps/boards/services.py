from .models import Board, Membership
from django.db import transaction

# from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser


@transaction.atomic
def create_user_board(
    user: AbstractBaseUser, name: str, description: str = ""
) -> Board:
    """Creates a user board for when the board is created.

    Attributes:
        user: should be user but for what we have right now its AbstractBaseUser
        name: name of board
        description: a description of the board.
    Returns:
        object type board

    """
    board = Board.objects.create(created_by=user, name=name, description=description)
    Membership.objects.create(board=board, user=user, role=Membership.Role.OWNER)

    return board


def join_by_code(user: AbstractBaseUser, join_code: str = "") -> Board:
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
