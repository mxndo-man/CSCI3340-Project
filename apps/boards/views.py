# Create your views here.


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.accounts.models import CustomUser

from .forms import BoardForm, JoinBoardForm
from .models import Board, Membership
from .permissions import get_board, is_owner
from .services import create_user_board, join_by_code, leave_board, remove_member


@login_required
def create_board_view(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = create_user_board(
                request.user,
                form.cleaned_data["name"],
                form.cleaned_data["description"],
            )
            return redirect("boards:detail", pk=board.pk)
    else:
        form = BoardForm()

    return render(request, "boards/create.html", {"form": form})


@login_required
def join_board_view(request):
    if request.method == "POST":
        form = JoinBoardForm(request.POST)
        if form.is_valid():
            try:
                board = join_by_code(request.user, form.cleaned_data["join_code"])
            except Board.DoesNotExist:
                form.add_error("join_code", "Invalid join code.")
            else:
                return redirect("boards:detail", pk=board.pk)
    else:
        form = JoinBoardForm()

    return render(request, "boards/join.html", {"form": form})


@login_required
@require_POST
def leave_board_view(request, board_id: int):
    board = get_board(request.user, board_id)
    try:
        leave_board(request.user, board)
    except ValueError as e:
        messages.error(request, f"An Error occured {e}")
        return redirect("boards:detail", pk=board.pk)
    messages.success(request, f"You left {board.name}.")
    return redirect("boards:list")


@login_required
@require_POST
def remove_member_view(request, board_id, user_id):
    board = get_board(request.user, board_id=board_id)
    target = get_object_or_404(CustomUser, pk=user_id)
    try:
        remove_member(request.user, target, board)
    except (ValueError, Membership.DoesNotExist) as e:
        messages.error(request, f"An Error {e}")
        return redirect("boards:detail", pk=board.pk)
    messages.success(request, f"Removed {target.username} from the board.")
    return redirect("boards:detail", pk=board.pk)


@login_required
def board_list_view(request):
    boards = (
        Board.objects.filter(membership__user=request.user)
        .prefetch_related("membership_set__user")
        .order_by("-created_at")
    )
    return render(request, "boards/list.html", {"boards": boards})


@login_required
def board_detail_view(request, pk: int):
    """Getting the details of the board.

    Args:
        request: request
        pk: board id
    Returns:
        A render of the page.

    """
    board = get_board(request.user, pk)
    members = board.membership_set.select_related("user").order_by("joined_at")
    return render(
        request,
        "boards/detail.html",
        {
            "board": board,
            "members": members,
            "is_owner": is_owner(request.user, board),
        },
    )
