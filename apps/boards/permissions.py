# This file will be for authentication.
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.shortcuts import get_object_or_404

from apps.accounts.models import CustomUser

from .models import Board, Membership


def is_member(user: CustomUser | AnonymousUser, board: Board) -> bool:
    """Helper function to determine a members auth.
    Attributes:
        user: The user that is trying to access the page.
        board: The board that the user is trying to access.
    Returns:
        boolean type.

    """
    if not user.is_authenticated:
        return False
    return Membership.objects.filter(user=user, board=board).exists()


def is_owner(user: CustomUser | AnonymousUser, board: Board) -> bool:
    """Helper function to determine if a user is the Owner.

    Attributes:
        user: A CustomUser or AnonymousUser
        board: The board that the user is trying to access.
    Returns:
        boolea type.

    """
    if not user.is_authenticated:
        return False
    return Membership.objects.filter(
        user=user, board=board, role=Membership.Role.OWNER
    ).exists()


def get_board(user: CustomUser | AnonymousUser, board_id: int) -> Board:
    """A helper function to get the board.

    Attributes:
        user: A CustomUser or AnonymousUser that is trying to access the page.
        board_id: The id of the board.
    Returns:
        A board type object.
    """
    board = get_object_or_404(Board, pk=board_id)
    if not is_member(user=user, board=board):
        raise Http404("Board not found.")
    return board
