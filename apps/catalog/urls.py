from django.urls import path, re_path

from .views import (ActionCategoryList, BrandDetail,  # ProductsJSONTemplate,
                    BrandsList, CardTypeView, CatalogList, CategoryJSONDetail,
                    CategoryList, DirectionCategoryList, ProductDatail,
                    ProductsJSONTemplateDebug, SearchView)

urlpatterns = [
    path("product-category/", CatalogList.as_view(), name="catalog"),
    path("products-debug/", ProductsJSONTemplateDebug.as_view(), name="products-debug"
         ),
    path("products/", ProductsJSONTemplateDebug.as_view(), name="products"),
    # path("products/", ProductsJSONTemplate.as_view(), name="products"),
    path("brands/<slug>/", BrandDetail.as_view(), name="brand"),
    path("brands/", BrandsList.as_view(), name="brands"),
    path("product-category/<slug>/",
         CategoryJSONDetail.as_view(),
         name="product-category",
         ),
    path("product/<slug>/",
         ProductDatail.as_view(), name="product"),
    re_path(r"tags/([\w-]+)/$", DirectionCategoryList.as_view(), name="tags"),
    path("actions/", ActionCategoryList.as_view(), name="actions"),
    path("category-list/<type>/",
         CategoryList.as_view(),
         name="category-list",
         ),
    # Поиск по товарам и услугам
    path("api/catalog/search/", SearchView.as_view(), name="search"),
    path("api/catalog/card-type/", CardTypeView.as_view(), name="card-type"),
]
