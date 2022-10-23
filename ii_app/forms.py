from django import forms 
from .models import Booking, Risk
from attr import attrs
from .choices import status_choices
from .choices import risk_impact_choices
from .choices import risk_probability_choices
from .choices import risk_owner_choices

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk 
        fields = ['project', 'resource','description','impact','probability',
                  'mitigation','owner','status','date_opened']
        widgets = {
            'project':forms.Select(attrs={'class':'form-control'}),
            'resource':forms.Select(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs = {'class':'form-control', 'rows': '3'}),
            'impact': forms.Select(attrs = {'class':'form-control'}, choices= risk_impact_choices),
            'probability': forms.Select(attrs = {'class':'form-control'}, choices= risk_probability_choices),
            'mitigation': forms.Textarea(attrs = {'class':'form-control','rows': '3'}),
            'owner': forms.Select(attrs = {'class':'form-control rows-3'}, choices= risk_owner_choices),
            'status': forms.Select(attrs = {'class':'form-control'}, choices= status_choices ),
            'date_opened': forms.TextInput(attrs = {'class':'form-control'}),
            },
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['day','hours']

        widgets = {
                'day':forms.Select(attrs={'class':'form-control'}),
                'hours': forms.Select(attrs = {'class':'form-control'}, choices= status_choices ),
                
                 },
    



  

  