import os

from geosafe.tasks.analysis import filter_impact_function

__author__ = 'ismailsunni'

import logging

from django.forms import models
from django import forms

from geonode.layers.models import Layer

from geosafe.models import Analysis
from django.conf import settings

LOG = logging.getLogger(__name__)


class AnalysisCreationForm(models.ModelForm):
    """A form for creating an event."""

    class Meta:
        model = Analysis
        fields = (
            'exposure_layer',
            'hazard_layer',
            'aggregation_layer',
            'impact_function_id',
            'extent_option'
        )

    exposure_layer = forms.ModelChoiceField(
        label='Exposure Layer',
        required=True,
        queryset=Layer.objects.filter(metadata__layer_purpose='exposure'),
        widget=forms.Select(
            attrs={'class': 'form-control'})
    )

    hazard_layer = forms.ModelChoiceField(
        label='Hazard Layer',
        required=True,
        queryset=Layer.objects.filter(metadata__layer_purpose='hazard'),
        widget=forms.Select(
            attrs={'class': 'form-control'})
    )

    aggregation_layer = forms.ModelChoiceField(
        label='Aggregation Layer',
        required=False,
        queryset=Layer.objects.filter(metadata__layer_purpose='aggregation'),
        widget=forms.Select(
            attrs={'class': 'form-control'})
    )

    print settings.CELERY_ALWAYS_EAGER

    if_id_list = filter_impact_function.delay().get()

    impact_function_id = forms.ChoiceField(
        label='Impact Function ID',
        required=True,
        choices=[(id, id) for id in if_id_list]
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AnalysisCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AnalysisCreationForm, self).save(commit=False)
        instance.user = self.user
        instance.save()
        return instance
