import pytest
import app as portal


@pytest.fixture
def client():
    portal.app.config["TESTING"] = True
    portal.app.config["SECRET_KEY"] = "test-secret-key"
    return portal.app.test_client()


def login_as(client, username):
    with client.session_transaction() as session:
        session["_user_id"] = username
        session["_fresh"] = True


@pytest.mark.parametrize(
    "username, routes",
    [
        ("admin_demo", [
            "/dashboard", "/admin", "/inventory", "/orders", "/reports"
        ]),
        ("inventory_demo", [
            "/dashboard", "/inventory", "/orders"
        ]),
        ("staff_demo", [
            "/dashboard", "/inventory", "/orders"
        ]),
        ("customer_demo", [
            "/dashboard", "/orders"
        ]),
    ],
)
def test_allowed_routes(client, username, routes):
    login_as(client, username)

    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, (
            f"{username} should access {route}"
        )


@pytest.mark.parametrize(
    "username, routes",
    [
        ("inventory_demo", ["/admin", "/reports"]),
        ("staff_demo", ["/admin", "/reports"]),
        ("customer_demo", ["/admin", "/inventory", "/reports"]),
    ],
)
def test_restricted_routes(client, username, routes):
    login_as(client, username)

    for route in routes:
        response = client.get(route)
        assert response.status_code == 403, (
            f"{username} should be denied access to {route}"
        )


@pytest.mark.parametrize(
    "route",
    ["/dashboard", "/admin", "/inventory", "/orders", "/reports"],
)
def test_unauthenticated_access_redirects_to_login(client, route):
    response = client.get(route)

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_homepage_is_public(client):
    response = client.get("/")
    assert response.status_code == 200


def test_invalid_login_is_rejected(client):
    response = client.post(
        "/login",
        data={
            "username": "invalid_demo_user",
            "password": "incorrect-password",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
