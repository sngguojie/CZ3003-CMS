import requests
import logging


url = "https://crisismanagement.herokuapp.com/emailApp/create/"
r=requests.post(url,json={"start": "start"})


