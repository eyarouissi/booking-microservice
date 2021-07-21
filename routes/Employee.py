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
router = APIRouter()


#Returns the project 
@router.get("/get_booking/{project_code}", response_description="project retrieved")
async def get_project_data(project_code: str):

    doc = list ( Projects_collection.find({ "project_code" : project_code}))
    return ResponseModel("the project  is : {}  ".format(doc), "Project retrieved successfully")
    

#Receives a post request from WIX containing a booked session. 
@router.post("/receive_booking")
async def receive_booking( employee : dict):
        
        wix_data = jsonable_encoder(employee)
        Employee = wix_data['data']
        print(Employee['project_code'])
        code = Employee['project_code'].strip()
        email = Employee['email'].strip()
        
        Projects_collection.update_one({ "project_code" : code, "Employees.email"  : email },
        {"$set" : {"Employees.$.scheduled_session"  : Employee['start_timestamp'] +" to "+ Employee['end_timestamp']}},True )
      
        return ResponseModel("the data of this employee who booked : {} is updated successfully".format(Employee), "Project updated successfully") \
        