from django.test import TestCase, Client as TestClient
from ii_app.models import Client, Project, Resource, Position, Contract, Assignment
from ii_app.models import Booking, Invoice, Risk
from django.contrib.auth.models import User

class ModelTestCase (TestCase):
    def setUp(self):
        self.client = Client.objects.create(name='Network Rail')
        self.project = Project.objects.create(client=self.client, code='CO2010', title='Streams')
        self.resource = Resource.objects.create(project=self.project, name='John Smith', 
        amey_position='Principal Consultant', skillset='Data Architect', cone_rate=1)
        self.position = Position.objects.create(project=self.project, name='Data Architect')
        self.contract = Contract.objects.create(project=self.project, name='Streams CF', 
        start='2022-01-01', end='2022-01-01')
        self.assignment = Assignment.objects.create(resource=self.resource, 
        position=self.position, contract=self.contract, rate=1, start='2022-01-01', end='2022-01-01')
        self.booking = Booking.objects.create(assignment=self.assignment, day='2022-01-01', hours=1)
        self.invoice = Invoice.objects.create(project=self.project, start='2022-01-01', 
        end='2022-01-01', value=1, document='')
        self.risk = Risk.objects.create(project=self.project, resource=self.resource, 
        description='To be resolved', impact='High', probability='High', 
        mitigation='Negotiate Contract', owner='Serena Haak', status='Open', 
        date_opened='2022-01-01')

    def test_1_client(self):
        self.assertEqual(self.client.name, 'Network Rail')
    
    def test_2_project(self):
        self.assertEqual(self.project.code, 'CO2010')
        self.assertEqual(self.project.title, 'Streams')
        self.assertEqual(self.project.client.name, 'Network Rail')
    
    def test_3_resource(self):
        self.assertEqual(self.resource.name, 'John Smith')
        self.assertEqual(self.resource.amey_position, 'Principal Consultant')
        self.assertEqual(self.resource.skillset, 'Data Architect')
        self.assertEqual(self.resource.cone_rate, 1)
        self.assertEqual(self.resource.project.code, 'CO2010')
    
    def test_4_position(self):
        self.assertEqual(self.position.project.code, 'CO2010')
        self.assertEqual(self.position.name, 'Data Architect')
    
    def test_5_contract(self):
        self.assertEqual(self.contract.project.code, 'CO2010')
        self.assertEqual(self.contract.name, 'Streams CF')
        self.assertEqual(self.contract.start, '2022-01-01')
        self.assertEqual(self.contract.end, '2022-01-01')
    
    def test_6_assignment(self):
        self.assertEqual(self.assignment.resource.name, 'John Smith')
        self.assertEqual(self.assignment.position.name, 'Data Architect')
        self.assertEqual(self.assignment.contract.name, 'Streams CF')
        self.assertEqual(self.assignment.rate, 1)
        self.assertEqual(self.assignment.start, '2022-01-01')
        self.assertEqual(self.assignment.end, '2022-01-01')
      
    def test_7_booking(self):
        self.assertEqual(self.booking.day, '2022-01-01')
        self.assertEqual(self.booking.hours, 1)
    
    def test_8_risk(self):
        self.assertEqual(self.risk.impact, 'High')
        self.assertEqual(self.risk.description, 'To be resolved')
        self.assertEqual(self.risk.probability, 'High')
        self.assertEqual(self.risk.mitigation, 'Negotiate Contract')
        self.assertEqual(self.risk.owner, 'Serena Haak')
        self.assertEqual(self.risk.status, 'Open')

# for each route, are you able to access the page
class PagesTestCase (TestCase):
    def setUp(self):
        self.c = TestClient()
        self.user = User.objects.create_user("romidhillon", 
        "romidhillon_13@hotmail.co.uk", "admin")
        self.c.force_login(self.user)

    def test_1(self):
        res = self.c.get("/sign_in/")
        self.assertEqual(res.status_code,200)

    def test_2(self):
        res = self.c.get("/ii_app/")
        self.assertEqual(res.status_code,200)

    def test_3(self):
        res = self.c.get("/ii_app/resources/")
        self.assertEqual(res.status_code,200)

    def test_4(self):
        client = Client.objects.create(name='a')
        project = Project.objects.create(client=client, code='a', title='a')
        resource = Resource.objects.create(project=project, name='a', 
        amey_position='a', skillset='a', cone_rate=1, image='', cv='')
        res = self.c.get(f'/ii_app/resources/{resource.name}/')
        self.assertEqual(res.status_code, 200)

    def test_5(self):
        res = self.c.get('/ii_app/addrisks/')
        self.assertEqual(res.status_code, 200)

    def test_8(self):
        res = self.c.get('/ii_app/riskregister/')
        self.assertEqual(res.status_code, 200)

    def test_9(self):
        res = self.c.get('/ii_app/margin/')
        self.assertEqual(res.status_code, 200)

    def test_10(self):
        res = self.c.get('/ii_app/finances/')
        self.assertEqual(res.status_code, 200)

    def test_11(self):
        client = Client.objects.create(name='a')
        project = Project.objects.create(client=client, code='a', title='a')
        res = self.c.get(f'/ii_app/finances/{project.code}/')
        self.assertEqual(res.status_code, 200)
    
    def test_99(self):
        res = self.c.get(f'/ii_app/finances/jnsjncoins/')
        self.assertEqual(res.status_code, 404)

    def test_12(self):
        res = self.c.get('/ii_app/cv/')
        self.assertEqual(res.status_code, 200)

    def test_14(self):
        res = self.c.get('/ii_app/bookings/')
        self.assertEqual(res.status_code, 200)

    def test_15(self):
        client = Client.objects.create(name='a')
        project = Project.objects.create(client=client, code='a', title='a')
        position = Position.objects.create(project= project ,name= 'a')
        resource = Resource.objects.create(project=project, name='a', amey_position='a', 
        skillset='a', cone_rate=1, image='', cv='')
        contract = Contract.objects.create(project=project, name = 'a', start = '2022-02-01', 
        end = '2022-02-01', document = '')
        assignment = Assignment.objects.create(resource = resource, contract = contract, 
        position = position, start= '2022-02-01', end= '2022-02-01', rate = 1)
        res = self.c.get(f'/ii_app/bookings/{assignment.id}/')
        self.assertEqual(res.status_code, 200)

    def test_16(self):
        res = self.c.get(f'/ii_app/bookings/123/')
        self.assertEqual(res.status_code, 404)