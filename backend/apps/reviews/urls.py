from django.urls import path

from . import views

urlpatterns = [
    path(
        "my-reviews/",
        views.CustomerReviewListCreateView.as_view(),
        name="customer-reviews",
    ),
    path(
        "my-reviews/<int:pk>/",
        views.CustomerReviewDetailView.as_view(),
        name="customer-review-detail",
    ),
    path(
        "packages/<int:package_id>/",
        views.PublicPackageReviewListView.as_view(),
        name="public-package-reviews",
    ),
    path(
        "manager/",
        views.ManagerReviewListView.as_view(),
        name="manager-reviews",
    ),
]
