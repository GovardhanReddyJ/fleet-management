from flask import Flask,request,jsonify
from .arms_models import db,Employee,Deployed,PrincipalConsultant
from flask_migrate import Migrate
from datetime import date
# from flask_restx import Api,Resource
# from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/flask_arms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)
migrate=Migrate(app,db)
# api=Api(app,version=1.0,title='Deployed Api',description='Api | post data into deployed table')

# ns=api.namespace('deployed',description='Deployed operations')

@app.route('/get')
def sample():
    return {"status":"ok"}

@app.route('/add_employee',methods=['POST'])
def Add_employee():
    data=request.json
    try:
        new_employee=Employee(
            first_name=data.get('first_name',None),
            last_name=data.get('last_name',None),
            email=data.get('email',None),
            date_of_join=data.get('date_of_join', date.today()),
            technology_cat=data.get('technology_cat'),
            designation=data['designation'],
            employee_status=data['employee_status'],
            graduation=data['graduation'],
            ug_year_of_passout=data.get('ug_year_of_passout', date.today()),
            pg_education=data.get('pg_education'),
            pg_education_passout_year=data.get('pg_education_passout_year',date.today()),
            pg_stream=data.get('pg_stream'),
            mobile_no=data['mobile_no'],
            alternate_mobile_no=data['alternate_mobile_no']
        )
        new_employee.validate_consistency()
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"status":"employee successfully added"})
    except ValueError as e:
        return jsonify({"status":str(e)})

@app.route('/deployed_data',methods=['POST'])
def EnterDataIntoDeployed():
    data=request.json
    try:
        from pdb import set_trace
        set_trace()
        employee_id=data['employee_id']
        ppl_id=data['principal_consultant_id']
        employee_instance=Employee.query.get_or_404(employee_id)
        ppl_instance=PrincipalConsultant.query.get_or_404(ppl_id)
        new_employee=Deployed(
            employee_id=employee_instance,
            # employee=data.get('employee')
            date_of_deploy=data.get('date_of_deploy',date.today()),
            designation=data.get('designation',"Software Engineer"),
            resource_type=data.get('resource_type',"Contract Based"),
            client=data.get('client'),
            project_start_date=data.get('project_start_date',date.today()),
            project_end_date=data.get('project_end_date'),
            billstatus=data.get('billstatus'),
            bill_rate_per_month=data['bill_rate_per_month'],
            candidate_ctc=data['candidate_ctc'],
            work_mode=data['work_mode'],
            work_location=data['work_location'],
            # principal_consultant_id=data['principal_consultant_id'],
            principal_consultant_id=ppl_id,
            remarks=data['remarks']         
        )
        new_employee.validate_project_dates()
        # employee_id=Employee.model.
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({'status':"successfully added into deployed table"})
    except Exception as e:
        return {'Error':str(e)},400
# @ns.route('/')
# class DeployedResource(Resource):
#     @ns.expect(deployed_model)
#     def post(self):
#         data=request.json
#         try:
#             new_employee = Deployed(
#                 employee_id=data['employee_id'],
#                 date_of_deploy=data.get('date_of_deploy', date.today()),
#                 designation=data.get('designation', "Software Engineer"),
#                 resource_type=data.get('resource_type', "Contract Based"),
#                 client=data.get('client'),
#                 project_start_date=data.get('project_start_date', date.today()),
#                 project_end_date=data.get('project_end_date'),
#                 billstatus=data['billstatus'],
#                 bill_rate_per_month=data['bill_rate_per_month'],
#                 candidate_ctc=data['candidate_ctc'],
#                 work_mode=data['work_mode'],
#                 work_location=data['work_location'],
#                 principal_consultant_id=data['principal_consultant_id'],
#                 remarks=data['remarks']
#             )
#             db.session.add(new_employee)
#             db.session.commit()
#             return {'status': "Successfully added into deployed table"}, 201
#         except Exception as e:
#             return {'error':str(e)},400 

@app.route('/add_principle_consultants',methods=['POST',"GET"])
def AddPrincipleConsultants():
    data=request.json
    try:
        new_principle_consultants = PrincipalConsultant(
            employee_id=data.get('employee_id'),
            consultant_name=data.get('consultant_name'),
            clients=data.get('clients')
        )
        db.session.add(new_principle_consultants)
        db.session.commit()
        return jsonify({'status':"suucessfully added into principle consutants"})
    except Exception as e:
        return jsonify({'error':str(e)})
    
if __name__=='__main__':
    app.run(port=3000,debug=True)
