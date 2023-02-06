from django.conf import settings
from django.core.files.storage import default_storage
# coding: utf-8

# imports
import os
import re

from django import forms
from django.utils.translation import gettext as _

from filebrowser_safe.settings import FOLDER_REGEX

ALLOWED_CHARS_MSG = (
    "Only letters, numbers, underscores, spaces and hyphens are allowed."
)

alnum_name_re = re.compile(FOLDER_REGEX)


class MakeDirForm(forms.Form):
    """
    Form for creating Folder.
    """

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super().__init__(*args, **kwargs)

    dir_name = forms.CharField(
        widget=forms.TextInput(
            attrs=dict({"class": "vTextField"}, max_length=50, min_length=3)
        ),
        label=_("Name"),
        help_text=_(ALLOWED_CHARS_MSG),
        required=True,
    )

    def clean_dir_name(self):
        if self.cleaned_data["dir_name"]:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not alnum_name_re.search(self.cleaned_data["dir_name"]):
                raise forms.ValidationError(_(ALLOWED_CHARS_MSG))
            # Folder must not already exist.
            if os.path.isdir(os.path.join(self.path, self.cleaned_data["dir_name"])):
                raise forms.ValidationError(_("The Folder already exists."))
        return self.cleaned_data["dir_name"]


class RenameForm(forms.Form):
    """
    Form for renaming Folder/File.
    """

    def __init__(self, path, file_extension, *args, **kwargs):
        self.path = path
        if re.match("^https?://", settings.MEDIA_ROOT):
            self.path = re.sub("^" + settings.MEDIA_ROOT, "", self.path)
        self.file_extension = file_extension
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(
            attrs=dict({"class": "vTextField"}, max_length=50, min_length=3)
        ),
        label=_("New Name"),
        help_text=_(ALLOWED_CHARS_MSG),
        required=True,
    )

    def clean_name(self):
        if self.cleaned_data["name"]:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not alnum_name_re.search(
                self.cleaned_data["name"]
            ) or not alnum_name_re.search(self.path):
                raise forms.ValidationError(_(ALLOWED_CHARS_MSG))
            #  folder/file must not already exist.
            if default_storage.isdir(os.path.join(self.path, self.cleaned_data['name'])):
                raise forms.ValidationError(_(u'The Folder already exists.'))
            elif default_storage.isfile(os.path.join(self.path, self.cleaned_data['name'] + self.file_extension)):
                raise forms.ValidationError(_(u'The File already exists.'))
        return self.cleaned_data['name']
