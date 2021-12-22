*** Settings ***
Library   ../Webhooks/Webhooks.py
Library    RequestsLibrary


*** Test Cases ***
Startup Webhooks
    Startup webhooks
    Sleep    1 s
    GET    http://localhost:8000/all