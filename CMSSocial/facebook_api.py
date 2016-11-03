import facebook
import datetime
import env

class FacebookApp:
    
    def __init__(self, page_id, access_token):
        self.page_id = page_id
        self.access_token = access_token
        self.api = self.get_api()
    
    def get_api(self):
        graph = facebook.GraphAPI(self.access_token)
        # Get page token to post as the page. You can skip 
        # the following if you want to post as yourself. 
        resp = graph.get_object('me/accounts')
        page_access_token = None
        for page in resp['data']:
            if page['id'] == self.page_id:
                page_access_token = page['access_token']
        graph = facebook.GraphAPI(page_access_token)
        return graph
    
    def post_status(self, message):
        status = self.api.put_wall_post(message)
        return status
    
if __name__ == "__main__":
    facebookApp = FacebookApp(env.FB_PAGE_ID, env.FB_PAGE_ACCESS_TOKEN)
    message = 'Crisis Update! '+str(datetime.datetime.now())
    status = facebookApp.post_status(message)
    print status