import google_auth_oauthlib.flow

print("fetch_token kwargs:", google_auth_oauthlib.flow.Flow.fetch_token.__code__.co_varnames)
print("authorization_url kwargs:", google_auth_oauthlib.flow.Flow.authorization_url.__code__.co_varnames)
