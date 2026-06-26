from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI() #instance of FASTAPI

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
# list[dict] -> list of dictionaries can be expected



#fastapi uses decoraters for routes
#Home route that responds to get requests to the root URL


@app.get("/posts", response_class=HTMLResponse, include_in_schema=False) # / -> path: root/posts, 
@app.get("/", response_class=HTMLResponse) # / -> path: root, 
def home():
    return f"<h1>{posts[1]["title"]}</h1>" 
#this dict will be automatically convert this to JSON by fast api
#uv run fastapi dev main.py -> automatically reruns updates, 
#fastapi run -> more optimised but doesn't rerun
#Think of curl as: A browser without a graphical interface.
#what does api end point actually mean here?
#if we want an HTML responses rather than JSON, we will add response class
#if we want /posts also show above line only, stack the decorater on the top of it both will point same function
#include in schema = False if any api is not nessesary in JSON APIs

@app.get("/api/posts", response_class=HTMLResponse) #we changed the route
def get_posts():
    return f"<h2>{posts[1]}</h2>"