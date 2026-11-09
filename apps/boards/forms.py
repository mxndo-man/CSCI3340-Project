from django import forms

from .models import Board


class BoardForm(forms.ModelForm):
    """Meta data for the board form."""

    class Meta:
        model = Board
        fields = ("name", "description")


class JoinBoardForm(forms.Form):
    """Join board code form."""

    join_code = forms.CharField(max_length=12, label="Join Code")
