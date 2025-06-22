from starlite import Starlite, get, post, Request, Response, HTTPException
from starlite.response import Redirect
from starlite.middleware.sessions import SessionMiddleware
import bcrypt

# In-memory user "database"
users = {"admin": bcrypt.hashpw(b"password", bcrypt.gensalt()).decode()}

# Session secret
SECRET = "super-secret-key"

# Middleware to handle sessions
session_middleware = SessionMiddleware(secret=SECRET)


# Helper: Get current user or raise
def get_current_user(request: Request) -> str:
    session = request.session
    if not session or "username" not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return session["username"]


# Login endpoint
@post("/login")
async def login(request: Request) -> Response:
    form_data = await request.body()
    data = dict(item.split("=") for item in form_data.decode().split("&"))
    username = data.get("username")
    password = data.get("password", "").encode()

    if username not in users or not bcrypt.checkpw(password, users[username].encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    request.session["username"] = username
    return Redirect("/protected")


# Logout endpoint
@get("/logout")
def logout(request: Request) -> Response:
    request.session.clear()
    return Redirect("/")


# Protected route
@get("/protected")
def protected_route(request: Request) -> dict:
    user = get_current_user(request)
    return {"message": f"Welcome {user}!"}


# Home route with login form
@get("/")
def index() -> str:
    return """
    <form action="/login" method="post">
      <input name="username" placeholder="Username"/><br>
      <input name="password" type="password" placeholder="Password"/><br>
      <input type="submit" value="Login"/>
    </form>
    """


# Starlite app
app = Starlite(
    route_handlers=[index, login, logout, protected_route],
    middleware=[session_middleware],
)
