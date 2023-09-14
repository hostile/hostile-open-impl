import asyncio
import httpx
import json
import os

from flask import Blueprint
from flask import Response
from flask import request

from ghunt.apis.peoplepa import PeoplePaHttp
from ghunt.helpers import gmail
from ghunt.objects import encoders
from ghunt.objects.base import GHuntCreds

blueprint = Blueprint("ghunt_blueprint", __name__)

credentials_file = 'ghunt-creds.txt'

credentials_stream = open(credentials_file, 'w')
credentials_stream.write(os.getenv('GHUNT_BASE64_COOKIES'))
credentials_stream.close()

ghunt_creds = GHuntCreds(credentials_file)
ghunt_creds.load_creds(silent=False)

@blueprint.route('/open-source/ghunt')
def find_email():
    query = request.args.to_dict()

    if 'email' not in query:
        return Response(json.dumps({
            'status': 'failed',
            'message': 'Missing email parameters!'
        }))

    target_email = query['email']
    as_client = httpx.AsyncClient()

    if asyncio.run(gmail.is_email_registered(as_client, target_email)) == 0:
        return Response(json.dumps({
            'status': 'failed',
            'message': 'No Google account found!'
        }), status=400)

    as_client = httpx.AsyncClient()
    people_api = PeoplePaHttp(ghunt_creds)

    found, person = asyncio.run(people_api.people_lookup(as_client, target_email, params_template='max_details'))

    if not found or 'PROFILE' not in person.names:
        return Response(json.dumps({
            'status': 'failed',
            'message': 'No Google account found!'
        }), status=400)

    response = json.loads(json.dumps(person, cls=encoders.GHuntEncoder))

    info = {
        'id': response['personId'],
        'last_updated': response['sourceIds']['PROFILE']['lastUpdated'],
        'maps_url': 'https://www.google.com/maps/contrib/' + response['personId'],
        'pfp_url': response['profilePhotos']['PROFILE']['url'],
        'cover_url': response['coverPhotos']['PROFILE']['url'],
        'name': response['names']['PROFILE']['fullname'],
        'emails': response['emails']['PROFILE']
    }

    return Response(json.dumps({
        'status': 'success',
        'data': info
    }), status=200)
