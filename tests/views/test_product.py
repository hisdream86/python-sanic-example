from app import App


_PRODUCT_NAME = "sample-product"
_PRODUCT_PRICE = 100
_PRODUCT_DESCRIPTION = "This is a sample product"


def test_product_create(mock_database):
    app = App()

    _, response = app.test_client.post(
        "/api/v1/products",
        json={"name": _PRODUCT_NAME, "price": _PRODUCT_PRICE, "description": _PRODUCT_DESCRIPTION},
    )

    assert response.status == 200
    assert response.json["code"] == 2000
    assert response.json["data"]["name"] == _PRODUCT_NAME
    assert response.json["data"]["price"] == _PRODUCT_PRICE
    assert response.json["data"]["description"] == _PRODUCT_DESCRIPTION


def test_product_list(mock_database):
    app = App()

    total_items = 10

    for i in range(total_items):
        app.test_client.post(
            "/api/v1/products",
            json={
                "name": f"{_PRODUCT_NAME}-{i}",
                "price": _PRODUCT_PRICE + i,
                "description": f"{_PRODUCT_DESCRIPTION} {i}",
            },
        )

    page = 0
    page_size = 5

    _, response = app.test_client.get(f"api/v1/products?page_size={page_size}&page={page}")

    assert response.status == 200
    assert response.json["code"] == 2000
    assert len(response.json["data"]["items"]) == page_size

    for i in range(page_size):
        assert response.json["data"]["items"][i]["name"] == f"{_PRODUCT_NAME}-{i}"
        assert response.json["data"]["items"][i]["price"] == _PRODUCT_PRICE + i
        assert response.json["data"]["items"][i]["description"] == f"{_PRODUCT_DESCRIPTION} {i}"


def test_product_put(mock_database):
    app = App()

    app.test_client.post(
        "/api/v1/products",
        json={"name": _PRODUCT_NAME, "price": _PRODUCT_PRICE, "description": _PRODUCT_DESCRIPTION},
    )

    _, response = app.test_client.put(
        f"/api/v1/products/{_PRODUCT_NAME}",
        json={
            "price": 0,
            "description": "Updated",
        },
    )

    assert response.status == 200
    assert response.json["code"] == 2000
    assert response.json["data"]["price"] == 0
    assert response.json["data"]["description"] == "Updated"


def test_product_delete(mock_database):
    app = App()

    app.test_client.post(
        "/api/v1/products",
        json={"name": _PRODUCT_NAME, "price": _PRODUCT_PRICE, "description": _PRODUCT_DESCRIPTION},
    )

    _, response = app.test_client.delete(f"/api/v1/products/{_PRODUCT_NAME}")
    assert response.status == 200
    assert response.json["code"] == 2000

    _, response = app.test_client.delete(f"/api/v1/products/{_PRODUCT_NAME}")
    assert response.status == 404
