"""Tests for the Mergington High School Activities API."""
import pytest
from src.app import activities


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all available activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_has_required_fields(self, client):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignup:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client):
        """Test successful signup for an activity."""
        email = "test@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_duplicate_email_fails(self, client):
        """Test that signing up with duplicate email fails."""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client):
        """Test that signing up for non-existent activity fails."""
        email = "test@mergington.edu"
        activity = "Nonexistent Activity"
        
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_signup_multiple_activities(self, client):
        """Test that a student can sign up for multiple activities."""
        email = "newstudent@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify both signups
        response = client.get("/activities")
        data = response.json()
        assert email in data["Chess Club"]["participants"]
        assert email in data["Programming Class"]["participants"]


class TestUnregister:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_successful(self, client):
        """Test successful unregistration from an activity."""
        email = "test@mergington.edu"
        activity = "Chess Club"
        
        # First sign up
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Then unregister
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        
        # Verify removal
        response = client.get("/activities")
        data = response.json()
        assert email not in data[activity]["participants"]

    def test_unregister_not_registered_fails(self, client):
        """Test that unregistering a non-registered email fails."""
        email = "notregistered@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_nonexistent_activity_fails(self, client):
        """Test that unregistering from non-existent activity fails."""
        email = "test@mergington.edu"
        activity = "Nonexistent Activity"
        
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]


class TestRootPath:
    """Tests for the root path redirect."""

    def test_root_redirects_to_static_html(self, client):
        """Test that root path redirects to static HTML."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307  # Temporary redirect


class TestActivityData:
    """Tests for activity data integrity."""

    def test_all_activities_have_participants_list(self, client):
        """Test that all activities have a participants list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_participants_not_exceed_max(self, client):
        """Test that participant count doesn't exceed max_participants."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert len(activity_data["participants"]) <= activity_data["max_participants"]

    def test_max_participants_is_positive(self, client):
        """Test that max_participants is a positive integer."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0
