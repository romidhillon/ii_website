from django import forms 
from .models import Risk
from attr import attrs
from .choices import status_choices
from .choices import risk_impact_choices
from .choices import risk_probability_choices
from .choices import risk_owner_choices

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk 
        fields = ['risk_description','risk_impact','risk_probability',
                  'risk_mitigation','risk_owner','risk_status','date_opened']
        widgets = {
            'risk_description': forms.Textarea(attrs = {'class':'form-control', 'rows': '3'}),
            'risk_impact': forms.Select(attrs = {'class':'form-control'}, choices= risk_impact_choices),
            'risk_probability': forms.Select(attrs = {'class':'form-control'}, choices= risk_probability_choices),
            'risk_mitigation': forms.Textarea(attrs = {'class':'form-control','rows': '3'}),
            'risk_owner': forms.Select(attrs = {'class':'form-control rows-3'}, choices= risk_owner_choices),
            'risk_status': forms.Select(attrs = {'class':'form-control'}, choices= status_choices ),
            'date_opened': forms.TextInput(attrs = {'class':'form-control'}),
            }
  
   

