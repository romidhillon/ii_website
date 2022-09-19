from django import forms 
from .models import Risk

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk 
        fields = ["risk_description","risk_impact","risk_probability",
                  "risk_mitigation","risk_owner","risk_status","date_opened"]
  
   