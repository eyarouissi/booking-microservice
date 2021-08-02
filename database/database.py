from pymongo.mongo_client import MongoClient
from models.Employee import Employee, ErrorResponseModel, ResponseModel
import motor.motor_asyncio
from bson import ObjectId
from pydantic.networks import EmailStr
import ssl
import pymongo 
from models import  * 


client = pymongo.MongoClient('mongodb+srv://hamdouch:lVRrNs9787uLgVkW@cls0.gd2gs.mongodb.net/devdb?retryWrites=true&w=majority', ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
database = client.devdb

Projects_collection = database.get_collection('Projects')





   
   









