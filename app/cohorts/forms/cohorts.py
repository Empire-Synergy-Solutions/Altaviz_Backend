from django import forms

from cohorts.models.cohorts import Cohort


class CohortCreateForm(forms.ModelForm):

    class Meta:
        model = Cohort
        fields = ["name"]
