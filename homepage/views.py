from django.http import HttpResponse


def index(request):
    htmlstr = """
        <h1>This is a Django Twitter Project</h1>
        <h2>It is made up of a series of APIs</h2>
        <h3>Contact: hxutech@gmail.com </h3>
        <h4>for additional info:</h4>
        
        <h4>please visit: https://twitternow.ml/admin</h4>
        
        <h5>username: admin</h5>
        
        <h5>password: admin</h5>
        
        
    """
    return HttpResponse(htmlstr)
