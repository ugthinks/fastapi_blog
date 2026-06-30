from fastapi import FastAPI, Request
from fastapi import HTTPException, status #for raising errors
from fastapi.exceptions import RequestValidationError   #these are for printing exception in proper webpage
from fastapi.responses import JSONResponse  #this one too
from starlette.exceptions import HTTPException as StarletteHTTPException #fastapi exceptions are based on this only and this allow to handel many exceptions even if it is not handeled manually
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from schemas import PostCreate, PostResponse 

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
        "author": "Jane Doen",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


# post -> is the variable name
# : -> type hint it tells what type of values you will get
# list[dict] -> list of dictionaries can be expected
# fastapi uses decoraters for routes
# Home route that responds to get requests to the root URL


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


@app.get("/posts/{post_id}", include_in_schema= False)
def post_page(request: Request, post_id : int):
    for post in posts:
        if(post.get("id") == post_id):
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": post["title"]})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="POST was not found")
# HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="POST was not found")


@app.get("/api/posts", response_model=list[PostResponse])                                          #we changed the route,     response_class=HTMLResponse
def get_posts():
    return posts


## Create Post
@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
    "id": new_id,
    "author": post.author,
    "title": post.title,
    "content": post.content,
    "date_posted": "April 23, 2025",
    }
    posts.append(new_post)
    return new_post


# printing individual post through id
# so we set the path keeping post id for each unque posts
# we ran a loop to get the actual post matching the id given and ids of posts we have
# otherwise raise an error


@app.get("/api/posts/{post_id}", response_model=PostResponse)      #Think of response_model as a filter, "I'll only keep these fields."
def get_post(post_id : int):
    for post in posts:
        if(post.get("id") == post_id):
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="POST was not found")
#it let's find terminal readers that it's is an error not just another string to ptint
# 422: forbidden -> it happens if any input is not allowed as you type string in post id (type hint -> int)


## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )  

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )