from django import forms

from .models import SurveyAnswer, SurveyQuestion, WaitingListEntry
from .signals import answered_survey


class WaitingListEntryForm(forms.ModelForm):

    referrer = forms.CharField(required=False, widget=forms.HiddenInput())
    campaign = forms.CharField(required=False, widget=forms.HiddenInput())
    email = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    car_type = forms.CharField(required=False)
    class Meta:
        model = WaitingListEntry
        fields = [
            "email",
            "phone_number",
            "car_type",
            "campaign",
            "referrer"
        ]

    def clean_email(self):
        value = self.cleaned_data["email"]
        try:
            entry = WaitingListEntry.objects.get(email=value)
        except WaitingListEntry.DoesNotExist:
            return value
        else:
            raise forms.ValidationError(
                "The email address {email} already registered on {date}.".format(
                    email=value,
                    date=entry.created.strftime("%m/%d/%y"),
                )
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "your@email.com"
        self.fields["email"].label = "Email Address"
        self.fields["phone_number"].widget.attrs["placeholder"] = "08023456789"
        self.fields["car_type"].widget.attrs["placeholder"] = "Toyota Corolla, Honda Accord, etc."


class SurveyForm(forms.ModelForm):

    class Meta:
        model = SurveyQuestion
        fields = []  # no automatic validation required

    def __init__(self, *args, **kwargs):
        """
        Build form fields on the fly.
        """
        self.survey = kwargs.pop("survey")
        super().__init__(*args, **kwargs)
        for question in self.survey.questions.all():
            self.fields[question.name] = question.form_field()

    def save(self, instance):
        for question in self.survey.questions.all():
            answer = SurveyAnswer.objects.create(instance=instance, question=question)
            value = self.cleaned_data[question.name]
            if value:
                if question.kind == SurveyQuestion.RADIO_CHOICES:
                    answer.value = value.label
                elif question.kind == SurveyQuestion.CHECKBOX_FIELD:
                    answer.value = ", ".join([x.label for x in value])
                elif question.kind == SurveyQuestion.BOOLEAN_FIELD:
                    answer.value_boolean = value
                else:
                    answer.value = value
            answer.save()
        answered_survey.send(sender=self, instance=instance)
