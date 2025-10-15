from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    # should return the activities mapping
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_and_prevent_duplicate():
    activity = 'Chess Club'
    email = 'test_student@example.com'

    # ensure email is not already in participants
    if email in activities[activity]['participants']:
        activities[activity]['participants'].remove(email)

    # signup should succeed
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]['participants']

    # signing up again should return 400
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

    # cleanup
    if email in activities[activity]['participants']:
        activities[activity]['participants'].remove(email)


def test_remove_participant():
    activity = 'Programming Class'
    email = 'remove_test@example.com'

    # ensure participant exists
    if email not in activities[activity]['participants']:
        activities[activity]['participants'].append(email)

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]['participants']
