from django import forms 
from .models import Risk
from attr import attrs

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk 
        fields = ['risk_description','risk_impact','risk_probability',
                  'risk_mitigation','risk_owner','risk_status','date_opened']
        widgets = {
            'risk_description': forms.Textarea(attrs = {'class':'form-control', 'rows': '3'}),
            'risk_impact': forms.NumberInput(attrs = {'class':'form-control', 'placeholder':'add a score between 0 and 100'}),
            'risk_probability': forms.NumberInput(attrs = {'class':'form-control','placeholder':'add a score between 0 and 100'}),
            'risk_mitigation': forms.Textarea(attrs = {'class':'form-control','rows': '3'}),
            'risk_owner': forms.TextInput(attrs = {'class':'form-control rows-3'}),
            'risk_status': forms.TextInput(attrs = {'class':'form-control'}),
            'date_opened': forms.TextInput(attrs = {'class':'form-control'}),
            }
  
   

