from django.urls import path
from .views import * 

urlpatterns =[
    path("approved_info/",approved_info,name="approved_info"),
    path("go_to_dashboard/",approved_info,name="go_to_dashboard"),
    path("search/",search_product,name="search"),
    path("list_all/",List_all_products.as_view(),name="list_all"),
    path("update_product/<int:pk>/", Update_product.as_view(), name="update_product"),
    path("add_product/",create_product.as_view(),name="add_product"),
    path("insights/<str:query_name>/", Dashboard.as_view(), name="insights"),
]