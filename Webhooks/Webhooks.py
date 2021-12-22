import asyncio

from fastapi import FastAPI, Response
from uvicorn import Server, Config
import uvicorn
from robot.api.deco import keyword, library



@library(scope='GLOBAL')
class Webhooks:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.server : Server = None
        self.ROBOT_LIBRARY_LISTENER = self
        pass

    @keyword("Startup webhooks")
    def startup_webhooks(self):
        config = Config(app, host='0.0.0.0', port=8000, debug=True)
        self.server = Server(config)
        asyncio.run(self.start_server())

    def _end_suite(self, name, attrs):
        #asyncio.run(self.server.shutdown())
        pass

    async def start_server(self):
        asyncio.run_coroutine_threadsafe(self.server.serve(), asyncio.get_event_loop())


app = FastAPI()

webhook_call = {}

@app.get('/all')
async def get_all():
    return webhook_call

@app.delete('/all', status_code=204)
async def delete_all():
    webhook_call.clear()
    return ''

@app.get('/')
async def index():
    return "Hello Webhook!"

@app.get('/{endpoint:path}')
async def main(endpoint, response: Response):
    try:
        return webhook_call[endpoint]
    except KeyError as identifier:
        response.status_code = 404
        return 'No Payload for this App'

@app.post('/{endpoint:path}', status_code=201)
async def post(endpoint, request=None):
    try:
        webhook_call[endpoint].append(request)
    except KeyError:
        webhook_call[endpoint] = []
        webhook_call[endpoint].append(request)
    return request

@app.delete('/{endpoint:path}', status_code=204)
async def delete_endpoint_data(endpoint=None):
    del webhook_call[endpoint]
    return ''
