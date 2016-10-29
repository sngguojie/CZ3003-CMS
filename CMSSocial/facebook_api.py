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
        return graph
    
    def post_status(self, message):
        status = self.api.put_wall_post(message)
        return status
    
if __name__ == "__main__":
    facebookApp = FacebookApp(env.FB_PAGE_ID, env.FB_PAGE_ACCESS_TOKEN)
    message = 'Crisis Update! '+str(datetime.datetime.now())
    status = facebookApp.post_status(message)
    print status