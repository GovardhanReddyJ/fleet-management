# from main import app
from sqlalchemy.orm import validates
from datetime import date,datetime
from flask_sqlalchemy import SQLAlchemy
from flask_restx import fields
# from main import api
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/flask_arms'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy()

class Employee(db.Model): 
    __tabalename__='employee'
    employee_id=db.Column(db.Integer,nullable=False,primary_key=True)
    first_name=db.Column(db.String(100),nullable=False)
    last_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(30),nullable=False)
    date_of_join=db.Column(db.Date,default=date.today())
    technology_cat=db.Column(db.String(100)) 
    designation=db.Column(db.String(100),nullable=False)
    employee_status=db.Column(db.String(100),nullable=False)
    graduation=db.Column(db.String(200),nullable=False)
    ug_year_of_passout=db.Column(db.Date,default=date.today())
    pg_education=db.Column(db.String(200))
    pg_education_passout_year=db.Column(db.Date,nullable=True)
    pg_stream =db.Column(db.String(100),nullable=True)
    mobile_no=db.Column(db.BigInteger)
    alternate_mobile_no=db.Column(db.BigInteger)
    test_varible=db.Column(db.String(200))
    

    @validates('pg_education_passout_year')
    def validate_pg_passout_year(self, key, value):
        if value and self.ug_year_of_passout:
            value = datetime.strptime(value, '%Y-%m-%d').date()
            ugpass_year=datetime.strptime(self.ug_year_of_passout, '%Y-%m-%d').date()
            days_difference = (value - ugpass_year).days
            if days_difference < 365:
                raise ValueError("The difference between UG and PG pass-out years should be at least 1 year.")
        return value

    @validates('mobile_no', 'alternate_mobile_no')
    def validate_mobile_numbers(self, key, value):
        print(self.alternate_mobile_no,'     ',value)
        print(self.mobile_no,'     ',value)
        if key == 'mobile_no' and value == self.alternate_mobile_no:
            raise ValueError("Mobile number and alternative mobile number should not be the same.")
        if key == 'alternate_mobile_no' and value == self.mobile_no:
            raise ValueError("Mobile number and alternative mobile number should not be the same.")
        return value
    def validate_consistency(self):
        print(self.mobile_no,self.alternate_mobile_no)
        print(self.ug_year_of_passout,self.pg_education_passout_year)
        if self.alternate_mobile_no == self.mobile_no:
            raise ValueError('the contact numbers should not be the same')

    # def __str__(self):
    #     return f'--> {self.first_name}'


class PrincipalConsultant(db.Model):
    __tablename__ = 'principal_consultant'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    consultant_name = db.Column(db.String(50))
    clients = db.Column(db.String(50))
    
    def __str__(self):
        return self.consultant_name


class Deployed(db.Model):
    __tablename__ = 'deployed'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    employee=db.relationship('Employee',backref=db.backref('deployed',uselist=False))
    date_of_deploy = db.Column(db.Date, default=date.today)
    designation = db.Column(db.String(150))
    resource_type = db.Column(db.String(250), nullable=False)    
    client = db.Column(db.String(150))
    project_start_date = db.Column(db.Date, default=date.today)
    project_end_date = db.Column(db.Date)
    billstatus = db.Column(db.Boolean, nullable=False)    
    bill_rate_per_month = db.Column(db.Integer)
    candidate_ctc = db.Column(db.Integer)
    work_mode = db.Column(db.String(200), nullable=False)
    work_location = db.Column(db.String(200), nullable=False)
    principal_consultant_id = db.Column(db.Integer, db.ForeignKey('principal_consultant.id'))
    principal_consultant = db.relationship('PrincipalConsultant', backref=db.backref('deployed', uselist=False))
    remarks = db.Column(db.Text)

    
    def validate_project_dates(self):
        if self.project_end_date <= self.project_start_date:
            raise ValueError("The project_end_date should be in future of project_start_date")
        

    def __str__(self):
        return f'{self.date_of_deploy}'

# deployed_model = api.model('Deployed', {
#     'employee_id': fields.Integer(required=True, description='Employee ID'),
#     'date_of_deploy': fields.Date(description='Date of Deployment'),
#     'designation': fields.String(description='Designation'),
#     'resource_type': fields.String(required=True, description='Resource Type'),
#     'client': fields.String(description='Client'),
#     'project_start_date': fields.Date(description='Project Start Date'),
#     'project_end_date': fields.Date(description='Project End Date'),
#     'billstatus': fields.Boolean(required=True, description='Billing Status'),
#     'bill_rate_per_month': fields.Integer(description='Bill Rate Per Month'),
#     'candidate_ctc': fields.Integer(description='Candidate CTC'),
#     'work_mode': fields.String(required=True, description='Work Mode'),
#     'work_location': fields.String(required=True, description='Work Location'),
#     'principal_consultant_id': fields.Integer(description='Principal Consultant ID'),
#     'remarks': fields.String(description='Remarks')
# })


class OnboardsTable(db.Model):
    __tablename__ = 'onboards_table'

    id = db.Column(db.Integer, primary_key=True)
    application_num = db.Column(db.Integer)
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    graduation = db.Column(db.String(300), nullable=False)    
    graduation_stream = db.Column(db.String(250), nullable=False)    
    graduation_year_of_passout = db.Column(db.Date, nullable=False)
    pg_education = db.Column(db.String(250), nullable=False)
    pg_education_passout_year = db.Column(db.Date, nullable=False)
    pg_stream = db.Column(db.String(250), nullable=False)
    mobile_no = db.Column(db.BigInteger, nullable=False)
    alt_mobile_no = db.Column(db.BigInteger, nullable=False, default=0)

    @validates('pg_education_passout_year', 'graduation_year_of_passout')
    def validate_passout_years(self, key, value):
        if self.graduation_year_of_passout and self.pg_education_passout_year:
            days_difference = (self.pg_education_passout_year - self.graduation_year_of_passout).days
            if days_difference < 365:
                raise ValueError("The difference between UG and PG pass-out years should be at least 1 year.")
        return value

    @validates('mobile_no', 'alt_mobile_no')
    def validate_phone_numbers(self, key, value):
        if len(str(value)) != 10:
            raise ValueError("Phone number must be 10 digits long.")
        if key == 'mobile_no' and self.alt_mobile_no == value:
            raise ValueError("Mobile number and alternative mobile number should not be the same.")
        if key == 'alt_mobile_no' and self.mobile_no == value:
            raise ValueError("Mobile number and alternative mobile number should not be the same.")
        return value

    def __str__(self):
        return str(self.application_num)


class EmployeeExit(db.Model):
    __tablename__ = 'employee_exit'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    employee=db.relationship('Employee',backref=db.backref('employee_exit',uselist=False))
    date_of_exit = db.Column(db.Date, nullable=False)
    exit_reason = db.Column(db.String(250))

    def __str__(self):
        return str(self.employee_id)


class CompanyPropertise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), unique=True)
    employee = db.relationship('Employee', backref=db.backref('company_propertise', uselist=False))
    laptop = db.Column(db.Boolean)
    laptop_description = db.Column(db.String(250))
    mouse = db.Column(db.Boolean)
    mouse_description = db.Column(db.String(250))
    bag = db.Column(db.Boolean)
    adapter = db.Column(db.Boolean)
    adapter_description = db.Column(db.String(250))

class ExitRaise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), unique=True)
    employee = db.relationship('Employee', backref=db.backref('exit_raise', uselist=False))
    exit_raise = db.Column(db.Boolean, default=False)
   





# ForeignKey: employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id')) 
# defines a foreign key constraint linking PrincipalConsultant to Employee.
# Here, employee.employee_id specifies the column (employee_id) in the referenced table (employee).

# Relationship: employee = db.relationship('Employee', backref=db.backref('consultants', lazy=True))
#  establishes a relationship between PrincipalConsultant and Employee.
#  It creates a virtual attribute employee in PrincipalConsultant and consultants in Employee to access related objects.
