from django.urls import path

from .views import (
    PackageCategoryListView,
    PublishedPackageListView,
    PublishedPackageDetailView,
    ManagerPackageListCreateView,
    ManagerPackageDetailView,
    ManagerPackageItineraryListCreateView,
    ManagerPackageItineraryDetailView,
    ManagerPackageDepartureListCreateView,
    ManagerPackageDepartureDetailView,
    GroupSizeListView,
    CustomerPackageEnquiryCreateView,
    ManagerPackageEnquiryListView,
    ManagerPackageEnquiryDetailView,    
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
    path(
    "manager/<int:package_id>/itinerary/",
    ManagerPackageItineraryListCreateView.as_view(),
    name="manager-package-itinerary-list-create",
    ),
    path(
        "manager/<int:package_id>/itinerary/<int:day_id>/",
        ManagerPackageItineraryDetailView.as_view(),
        name="manager-package-itinerary-detail",
    ),
    path(
    "manager/<int:package_id>/departures/",
    ManagerPackageDepartureListCreateView.as_view(),
    name="manager-package-departure-list-create",
    ),
    path(
        "manager/<int:package_id>/departures/<int:departure_id>/",
        ManagerPackageDepartureDetailView.as_view(),
        name="manager-package-departure-detail",
    ),
    path(
    "group-sizes/",
    GroupSizeListView.as_view(),
    name="group-size-list",
    ),
    
    # Customer enquiry
    path(
        "<int:package_id>/enquiries/",
        CustomerPackageEnquiryCreateView.as_view(),
        name="customer-package-enquiry-create",
    ),

    # Manager enquiry management
    path(
        "manager/enquiries/",
        ManagerPackageEnquiryListView.as_view(),
        name="manager-package-enquiry-list",
    ),
    path(
        "manager/enquiries/<int:pk>/",
        ManagerPackageEnquiryDetailView.as_view(),
        name="manager-package-enquiry-detail",
    ),
]