import uuid
from io import BytesIO

import pytest
from sqlalchemy import select

from src.infrastructure.models import StoredFile


@pytest.mark.asyncio
@pytest.mark.parametrize("route_template, object_name, expected_status", [
    pytest.param("/api/v1/files/{id}", "file", 200, id="get-file_success"),
    pytest.param("/api/v1/files/{id}", None, 404, id="get-file_not-found"),
    pytest.param("/api/v1/alerts/{id}", "alert", 200, id="get-alert_success"),
    pytest.param("/api/v1/alerts/{id}", None, 404, id="get-alert_not-found"),
])
async def test_get_endpoints(client, route_template, object_name, expected_status, alert_dep):
    objects = {
        "file": alert_dep.file_id,
        "alert": alert_dep.id
    }
    resource_id = objects.get(object_name, "not-found")
    url = route_template.format(id=resource_id)

    response = await client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize("route, limit, page, expected_len", [
    pytest.param("/api/v1/files/", 5, 2, 5, id="files_second_page"),
    pytest.param("/api/v1/files/", 12, 1, 10, id="files_correct_expected_len"),
    pytest.param("/api/v1/files/", 10, 5, 0, id="files_empty_page"),
    pytest.param("/api/v1/alerts/", 5, 2, 5, id="alerts_second_page"),
    pytest.param("/api/v1/alerts/", 12, 1, 10, id="alerts_correct_expected_len"),
    pytest.param("/api/v1/alerts/", 10, 5, 0, id="alerts_empty_page"),
])
async def test_list_endpoints(db_session, client, ten_alerts_dep, route, limit, page, expected_len):
    response = await client.get("/api/v1/files/", params={"limit": limit, "page": page})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get("total") == 10
    assert response_json.get("has_next") == (limit * page < 10)
    assert len(response_json.get("items")) == expected_len


@pytest.mark.asyncio
async def test_send_file(file_dep, client, mock_storage, mock_scheduler, db_session):
    file_content = b"fake image data"
    file_name = "test_image.png"
    user_file_name = "user_file_name"

    files = {"file": (file_name, BytesIO(file_content), "image/png")}
    form_data = {
        "title": user_file_name
    }

    response = await client.post(
        f"/api/v1/files/",
        data=form_data,
        files=files,
    )

    statement = select(StoredFile).filter_by(title="user_file_name")
    result = await db_session.execute(statement)
    db_obj = result.scalars().first()
    assert db_obj is not None

    mock_scheduler.schedule_file_analysis.assert_called_once_with(db_obj.id)

    assert response.status_code == 201
    content = response.json()
    assert content.get("title") == user_file_name
    assert content.get("original_name") == file_name
    assert db_obj.stored_name not in {content.get("title"), content.get("original_name")}
