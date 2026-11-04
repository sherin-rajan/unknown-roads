from django.urls import path

from .views import (
    PackageCategoryListView,
    PublishedPackageListView,
    PublishedPackageDetailView,
    ManagerPackageListCreateView,
    ManagerPackageDetailView,
)

urlpatterns = [
    # Public APIs
    path(
        "categories/",
        PackageCategoryListView.as_view(),
        name="package-category-list",
    ),
    path(
        "",
        PublishedPackageListView.as_view(),
        name="published-package-list",
    ),
    path(
        "<int:pk>/",
        PublishedPackageDetailView.as_view(),
        name="published-package-detail",
    ),

    # Manager APIs
    path(
        "manager/",
        ManagerPackageListCreateView.as_view(),
        name="manager-package-list-create",
    ),
    path(
        "manager/<int:pk>/",
        ManagerPackageDetailView.as_view(),
        name="manager-package-detail",
    ),
]