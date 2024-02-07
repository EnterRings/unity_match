from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from .forms import BookAddForm, BookSearchForm
from .models import Book

'''
書籍一覧ビュー
BookListView
'''
# 書籍一覧を表示するのでListViewクラスを継承
class BookListView(generic.ListView):
  # 操作の対象はBookモデル
  model = Book
  # book_list.htmlをレンダリング
  template_name = 'book_list.html'
  # 1ページに表示するレコードの件数を設定
  # paginate_by = 2

  # get_querysetをオーバーライド
  def get_queryset(self):
    # モデルBookのオブジェクトに
    # order_byを適用して書籍情報作成日時の降順で並べる
    books = Book.objects.order_by('-created_at')
    return books


'''
書籍詳細ビュー
BookDetailView
'''
# 書籍情報の詳細を表示するのでDetailViewを継承する
# DetailViewは、pkに格納されたid値を使ってクエリ：
# queryset = queryset.filter(pk=pk)
# を内部で実行するため、DetailViewでクエリ（queryset）を実装する必要はない
# 抽出されたレコードはContextオブジェクトのobjectキーの値として格納されるので、
# 詳細ページのテンプレート「book_detail.html」では、objectキーを指定して
# 各フィールドのデータを取り出すことができる
class BookDetailView(generic.DetailView):
  # クラス変数modelにbookを設定
  model = Book
  # book_detail.htmlをレンダリング
  template_name = 'book_detail.html'


'''
書籍登録ビュー
BookAddView
'''
class BookAddView(generic.CreateView):
  # クラス変数modelにBookを設定
  model = Book
  # book_add.htmlをレンダリング
  template_name = 'book_add.html'
  # クラス変数 form_class をオーバーライド
  # フォーム（BookAddForm）を利用する
  form_class = BookAddForm
  # クラス変数 success_url をオーバーライド
  # 正常に処理が完了したときは、book_list.html に遷移する
  # URLが固定のページに遷移させる
  success_url = reverse_lazy('library:book_list')

  # オーバーライド
  # フォームのバリデーションに問題がなければ実行される
  '''
  具体的な処理内容は以下の通り：

  form.save(commit=False):
  commit=Falseを指定することで、まだデータベースには保存せずに、フォームの入力値をもとにPythonオブジェクトを作成。
  これにより、book変数にはBookモデルのインスタンスが代入される。

  diary.save():
  データベースに実際に保存される前に、変更を加えたbookオブジェクトをデータベースに保存する。
  データベースへの保存が行われる。

  messages.success(self.request, '書籍情報を作成しました。'):
  ユーザーに対して、書籍情報の作成が成功したことを伝える成功メッセージを表示。
  これにより、画面上でユーザーに成功メッセージが表示される。

  return super().form_valid(form):
  super()を使用して、親クラス（generic.CreateView）のform_validメソッドを呼び出す。これにより、通常の処理が継続されます。

  要するに、form_validメソッドは、フォームのデータを取得し、それをデータベースに保存する前に追加の操作を行う。例えば、追加のフィールドを設定する、特定のユーザーに関連付けるなどのカスタムロジックを実行。そして最終的に、データベースへの保存を行い、成功メッセージをユーザーに表示する。
  '''
  def form_valid(self, form):
    # commit=FalseにしてPOSTされたデータを取得
    book = form.save(commit=False)
    # 実際に日記データベースに保存
    book.save()
    messages.success(self.request, '書籍情報を作成しました。')
    return super().form_valid(form)

  # オーバーライド
  # フォームバリデーションが失敗したときに実行される
  def form_invalid(self, form):
    # エラーメッセージを画面に表示する
    messages.error(self.request, "書籍情報の作成に失敗しました。")
    return super().form_invalid(form)


'''
書籍更新ビュー
BookUpdateView
'''
class BookUpdateView(generic.UpdateView):
  model = Book
  # diary_update.htmlをレンダリング
  template_name = 'book_update.html'
  form_class = BookAddForm

  # オーバーライド
  # URLが動的に変化するページに遷移させる
  def get_success_url(self):
    return reverse_lazy('library:book_detail', kwargs={'pk': self.kwargs['pk']})

  # バリデーションが成功したときに呼び出され、モデルへの更新処理が実行される。
  def form_valid(self, form):
    messages.success(self.request, '書籍情報を更新しました。')
    return super().form_valid(form)

  # バリデーションが失敗したときに呼び出される。
  def form_invalid(self, form):
    messages.error(self.request, "書籍情報の更新に失敗しました。")
    return super().form_invalid(form)
  

'''
書籍削除ビュー
BookDeleteView
'''
class BookDeleteView(generic.DeleteView):
  model = Book
  # book_delete.htmlをレンダリング
  template_name = 'book_delete.html'
  success_url = reverse_lazy('library:book_list')

  def delete(self, request, *args, **kwargs):
    messages.success(self.request, "書籍を削除しました。")
    return super().delete(request, *args, **kwargs)


'''
書籍検索ビュー
BookSearchView
'''
# 検索結果一覧を表示するのでListViewクラスを継承
class BookSearchView(generic.FormView):
  # フォーム（BookSearchForm）とBookSearchViewを紐づけるために
  # クラス変数（form_class）をオーバーライド
  form_class = BookSearchForm
  # book_search.htmlをレンダリング
  template_name = 'book_search.html'

  # 検索実行
  def post(self, request):
    form = BookSearchForm(request.POST)
    if form.is_valid():
      query_filters = Q()
      title = form.cleaned_data.get('title')
      author = form.cleaned_data.get('author')
      field = form.cleaned_data.get('field')
      publisher = form.cleaned_data.get('publisher')
      pub_year = form.cleaned_data.get('pub_year')
      page_number = form.cleaned_data.get('page_number')
      price = form.cleaned_data.get('price')
      isbn = form.cleaned_data.get('isbn')

      if title:
        #
        print('title = ', title)
        query_filters &= Q(title__icontains=title)
      if author:
        #
        print('author = ', author)
        query_filters &= Q(author__icontains=author)
      if field:
        #
        print('field = ', field)
        query_filters &= Q(field=field)
      if publisher:
        #
        print('publisher = ', publisher)
        query_filters &= Q(publisher__icontains=publisher)
      if pub_year:
        #
        print('pub_year = ', pub_year)
        query_filters &= Q(pub_year__lte=int(pub_year))
      if page_number:
        #
        print('page_number = ', page_number)
        query_filters &= Q(page_number__lte=int(page_number))
      if price:
        #
        print('price = ', price)
        query_filters &= Q(price__lte=int(price))
      if isbn:
        #
        print('isbn = ', isbn)
        query_filters &= Q(isbn=isbn)

      # Debug
      print('query_filters = ', query_filters)
      # AND検索の実行
      book_list = Book.objects.filter(query_filters)
      return render(request, 'book_list.html', {'book_list': book_list})

    return render(request, 'book_search.html', {'form': form})
