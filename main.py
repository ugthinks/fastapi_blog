from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
 
# from fastapi.responses import HTMLResponse (not used when template)
#jinja tool is a templating engine used by fastapi.
#templating engine allows us to write full html in and let json api endpoint saperate for developers


app = FastAPI()                                                 #instance of FASTAPI

app.mount("/static", StaticFiles(directory = "static"), name="static")


#1st argument => path, 
# 2nd => staticFiles INSTANCE POINTING TOWARDS static directory, 
# 3rd=> it is a name that will be used to point in our template


templates = Jinja2Templates(directory="templates")              #telling fastapi where to find our templates

posts: list[dict] = [   
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


# post -> is the variable name
# : -> type hint it tells what type of values you will get
#list[dict] -> list of dictionaries can be expected
#fastapi uses decoraters for routes
#Home route that responds to get requests to the root URL


@app.get("/posts", include_in_schema=False, name = "posts")                                         # / -> path: root/posts, response_class=HTMLResponse (used if template wasn't used)
@app.get("/", include_in_schema=False, name = "home")                                                                     # / -> path: root, response_class=HTMLResponse
def home(request: Request):                                                         #JINJA 2 needs Request as a parameter
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})       #f"<h1>{posts[1]["title"]}</h1>" 


#At first home takes Request then returns home.html as response
#{"posts": posts} -> The dictionary contains all the variable that wil be used in that template. 
#"posts" is the variable name : posts -> gives all the value here in this page to that variable name posts
#request contiain a lo of info with it. like URL generation and template context

#the dict will be automatically convert this to JSON by fast api
#uv run fastapi dev main.py -> automatically reruns updates, 
#fastapi run -> more optimised but doesn't rerun
#Think of curl as: A browser without a graphical interface.
#what does api end point actually mean here?
#if we want an HTML responses rather than JSON, we will add response class
#if we want /posts also show above line only, stack the decorater on the top of it both will point same function
#include in schema = False if any api is not nessesary in JSON APIs


@app.get("/api/posts")                                          #we changed the route,     response_class=HTMLResponse
def get_posts():
    return f"<h2>{posts[1]}</h2>"