from re import MULTILINE
from fastapi import APIRouter, Body,  Request
from fastapi.encoders import jsonable_encoder
import pymongo
from starlette.routing import request_response 
from database.database import *
from models.Employee import *
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
import  pymongo
import asyncio
import re
router = APIRouter()


#Returns the project 
@router.get("/get_booking/{project_code}", response_description="project retrieved")
async def get_project_data(project_code: str):

    doc = list ( Projects_collection.find({ "project_code" : project_code}))
    
    if doc == [] :
     return ErrorResponseModel("An error occured.", 404, " The project is not found")
    else :
     return ResponseModel("the project  is : {}  ".format(doc), "Project retrieved successfully")

#Receives a post request from WIX containing a booked session. 
@router.post("/receive_booking")
async def receive_booking( employee : dict):
        
        wix_data = jsonable_encoder(employee)
        Employee = wix_data['data']
        print(Employee['project_code'])
        code = Employee['project_code'].strip()
        email = Employee['email'].strip()
        start_time =Employee['start_timestamp']
        end_time =Employee['end_timestamp']

        match_start = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', start_time)
        match_end = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', end_time)
        start_date = datetime.strptime(match_start.group(), "%Y-%m-%dT%H:%M:%SZ").isoformat()
        
        doc = list ( Projects_collection.find({ "project_code" : code, "Employees.email"  : email}))
        if doc==[] :
            return ErrorResponseModel("An error occured.", 404, " Email is not available in the Employees")
        else:
            Projects_collection.update_one({ "project_code" : code, "Employees.email"  : email },
            {"$set" : {"Employees.$.scheduled_session"  : start_date }},True )
      
            return ResponseModel("the data of this employee who booked : {} is updated successfully".format(Employee), "Project updated successfully") \
        
