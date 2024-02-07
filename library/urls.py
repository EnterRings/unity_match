from django.urls import path
from . import views
from .views import book_list, book_detail, report_book

app_name = 'library'

urlpatterns = [
  # TOP
  path('', 
       views.indexView.as_view(), name='index'),
  # 書籍一覧
  path('book_list', 
       book_list, name='book_list'),
  # 個人一覧
  path('private_list', 
       views.PrivateListView.as_view(), name='private_list'),
  # 書籍詳細
  path('book_detail/<str:product_name>/', 
       book_detail, name='book_detail'),
  # 個人詳細
  path('private_detail/<int:pk>/', 
       views.PrivateDetailView.as_view(), name='private_detail'),
  # 書籍登録
  path('book_add', 
       views.BookAddView.as_view(), name='book_add'),
  # 書籍更新
  path('book_update/<int:pk>', 
       views.BookUpdateView.as_view(), name='book_update'),
  # 書籍削除
  path('book_delete/<int:pk>',
       views.BookDeleteView.as_view(), name='book_delete'),
  # 書籍検索
  path('book_search', 
       views.BookSearchView.as_view(), name='book_search'),
  # レビュー一覧   
  path('review_list/<str:product_name>/',
       views.ReviewListView.as_view(), name='review_list'),
  # 報告
  path('report_book/<int:book_id>/', views.report_book, name='report_book'),
  # 管理者側  
  path('admin_index', views.AdminIndexView.as_view(), name="admin_index"),
  # 製品一覧
  path('admin_product_list', views.AdminProductListView.as_view(), name="product_list"),
  # 製品詳細
  path('admin_product_detail/<int:pk>/', views.AdminProductDetailView.as_view(), name='product_detail'),
  # 製品登録
  path('admin_product_add', 
       views.AdminProductAddView.as_view(), name='product_add'),
  # 製品更新
  path('admin_product_update/<int:pk>', views.AdminProductUpdateView.as_view(), name='product_update'),
  # 製品削除
  path('admin_product_delete/<int:pk>',views.AdminProductDeleteView.as_view(), name='product_delete'),
  # 製品検索
  path('admin_product_search', views.AdminProductSearchView.as_view(), name='product_search'),
]
