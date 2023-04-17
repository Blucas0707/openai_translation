from medium import Client

from settings import MEDIUM_API_TOKEN, MEDIUM_APPLICATION_ID, MEDIUM_APPLICATION_SECRET

# Go to http://medium.com/me/applications to get your application_id and application_secret.
client = Client(application_id=MEDIUM_APPLICATION_ID, application_secret=MEDIUM_APPLICATION_SECRET)

# Build the URL where you can send the user to obtain an authorization code.
auth_url = client.get_authorization_url(
    'secretstate',
    'https://www.google.com/',
    ['basicProfile', 'publishPost']
)

# (Send the user to the authorization URL to obtain an authorization code.)

# Exchange the authorization code for an access token.
auth = client.exchange_authorization_code(
    'f610ee389ea0',
    'https://www.google.com/',
)

# The access token is automatically set on the client for you after
# a successful exchange, but if you already have a token, you can set it
# directly.
client.access_token = auth['access_token']

# Get profile details of the user identified by the access token.
user = client.get_current_user()
print('>>>>>> user:', user)

# Create a draft post.
post = client.create_post(
    user_id=user['id'],
    title='Title',
    content='<h2>Title</h2><p>Content</p>',
    content_format='html',
    publish_status='draft',
)

# When your access token expires, use the refresh token to get a new one.
client.exchange_refresh_token(auth['refresh_token'])
