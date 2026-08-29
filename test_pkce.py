import os
import google_auth_oauthlib.flow

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/drive.file']
)
flow.redirect_uri = 'https://filesaver.deathwolftech.site/google/callback'
auth_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true', prompt='consent')
print("has code_verifier:", hasattr(flow, 'code_verifier'))
if hasattr(flow, 'code_verifier'):
    print("code_verifier:", flow.code_verifier)
