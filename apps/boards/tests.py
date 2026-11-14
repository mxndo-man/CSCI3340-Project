from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import CustomUser

from .models import Board, Membership
from .services import create_user_board, join_by_code, leave_board, remove_member


class BoardTests(TestCase):
    """Tests for creating, joining, leaving, and removing members from boards."""

    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            username="owner", email="owner@example.com", password="pass12345"
        )
        self.member = CustomUser.objects.create_user(
            username="member", email="member@example.com", password="pass12345"
        )
        self.outsider = CustomUser.objects.create_user(
            username="outsider", email="outsider@example.com", password="pass12345"
        )
        self.board = create_user_board(self.owner, "Test Board")
        join_by_code(self.member, self.board.join_code)

    def test_create_makes_owner(self):
        membership = Membership.objects.get(board=self.board, user=self.owner)
        self.assertEqual(membership.role, Membership.Role.OWNER)
        self.assertTrue(self.board.join_code)

    def test_join_by_code(self):
        membership = Membership.objects.get(board=self.board, user=self.member)
        self.assertEqual(membership.role, Membership.Role.MEMBER)

        join_by_code(self.member, self.board.join_code)
        self.assertEqual(
            Membership.objects.filter(board=self.board, user=self.member).count(), 1
        )

    def test_join_bad_code(self):
        self.client.force_login(self.outsider)
        response = self.client.post(reverse("boards:join"), {"join_code": "nope"})
        self.assertContains(response, "Invalid join code.")
        self.assertFalse(
            Membership.objects.filter(board=self.board, user=self.outsider).exists()
        )

    def test_leave(self):
        leave_board(self.member, self.board)
        self.assertFalse(
            Membership.objects.filter(board=self.board, user=self.member).exists()
        )

        with self.assertRaises(ValueError):
            leave_board(self.owner, self.board)

    def test_remove_member(self):
        remove_member(self.owner, self.member, self.board)
        self.assertFalse(
            Membership.objects.filter(board=self.board, user=self.member).exists()
        )

        with self.assertRaises(ValueError):
            remove_member(self.owner, self.owner, self.board)

    def test_non_owner_cannot_remove(self):
        with self.assertRaises(PermissionDenied):
            remove_member(self.member, self.owner, self.board)

    def test_detail_404_for_non_member(self):
        url = reverse("boards:detail", kwargs={"pk": self.board.pk})

        self.client.force_login(self.outsider)
        self.assertEqual(self.client.get(url).status_code, 404)

        self.client.force_login(self.member)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_list_shows_only_my_boards(self):
        other_board = create_user_board(self.outsider, "Other Board")

        self.client.force_login(self.member)
        response = self.client.get(reverse("boards:list"))
        self.assertContains(response, self.board.name)
        self.assertNotContains(response, other_board.name)
        self.assertEqual(Board.objects.count(), 2)
