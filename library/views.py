from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookAddForm, BookSearchForm, AdminProductAddForm, AdminProductSearchForm
from .models import Book, Mousepad, Report
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

class indexView(generic.TemplateView):
  template_name = 'index.html'

'''
書籍一覧ビュー
BookListView
'''

def book_list(request):
    print("Function view book_list")
    search_query = request.GET.get('search_query', '')

    if search_query:
        mousepads = Mousepad.objects.filter(product__icontains=search_query)
    else:
        mousepads = Mousepad.objects.all()

    context = {
        'mousepads': mousepads,
    }

    return render(request, 'book_list.html', context)
  

'''
個人一覧ビュー
PrivateListView
'''
# 書籍一覧を表示するのでListViewクラスを継承
class PrivateListView(LoginRequiredMixin, generic.ListView):
  # 操作の対象はBookモデル
  model = Book
  # book_list.htmlをレンダリング
  template_name = 'private_list.html'
  # 1ページに表示するレコードの件数を設定
  # paginate_by = 2

  # get_querysetをオーバーライド
  def get_queryset(self):
    # モデルBookのオブジェクトに
    # order_byを適用して書籍情報作成日時の降順で並べる
    books = Book.objects.filter(create_user=self.request.user)
    #books = Book.objects.filter(create_user_id=self.request.user).values('product_name')
    # ログアウト時にlistを表示するとエラーになるけど多分使う機会ないから関係ないかも
    # ログインしてないときは一覧表示しないからーー全体のLISTも作らないといけない
    # books = Book.objects.order_by('id')
    return books



'''
書籍詳細ビュー
BookDetailView
'''
def get_most_common_choice(product_name, field_name):
    most_common_choice = Book.objects.filter(product_name=product_name).values(field_name).annotate(count=Count(field_name)).order_by('-count').first()
    if most_common_choice:
        return most_common_choice[field_name]
    else:
        return None

def book_detail(request, product_name):
    # 指定された製品名に対して、各項目ごとの最も選択された項目を取得
    most_common_hardness = get_most_common_choice(product_name, 'hardness')
    most_common_planing_speed = get_most_common_choice(product_name, 'planing_speed')
    most_common_control = get_most_common_choice(product_name, 'control')
    most_common_speed_of_start = get_most_common_choice(product_name, 'speed_of_start')
    most_common_bottom = get_most_common_choice(product_name, 'bottom')
    most_common_roll = get_most_common_choice(product_name, 'roll')
    most_common_edge = get_most_common_choice(product_name, 'edge')
    most_common_durability = get_most_common_choice(product_name, 'durability')

    # Mousepad モデルのインスタンスを取得
    mousepad = get_object_or_404(Mousepad, product=product_name)

    context = {
        'product_name': product_name,
        'most_common_hardness': most_common_hardness,
        'most_common_planing_speed': most_common_planing_speed,
        'most_common_control': most_common_control,
        'most_common_speed_of_start': most_common_speed_of_start,
        'most_common_bottom': most_common_bottom,
        'most_common_roll': most_common_roll,
        'most_common_edge': most_common_edge,
        'most_common_durability': most_common_durability,
        'mousepad': mousepad,
    }

    return render(request, 'book_detail.html', context)


'''
個人詳細ビュー
BookDetailView
'''
# 書籍情報の詳細を表示するのでDetailViewを継承する
# DetailViewは、pkに格納されたid値を使ってクエリ：
# queryset = queryset.filter(pk=pk)
# を内部で実行するため、DetailViewでクエリ（queryset）を実装する必要はない
# 抽出されたレコードはContextオブジェクトのobjectキーの値として格納されるので、
# 詳細ページのテンプレート「book_detail.html」では、objectキーを指定して
# 各フィールドのデータを取り出すことができる
class PrivateDetailView(generic.DetailView):
  # クラス変数modelにbookを設定
  model = Book
  # book_detail.htmlをレンダリング
  template_name = 'private_detail.html'


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
  success_url = reverse_lazy('library:private_list')

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
    # 追加しました
    book.create_user=self.request.user
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
    return reverse_lazy('library:private_detail', kwargs={'pk': self.kwargs['pk']})

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
      product_name = form.cleaned_data.get('product_name')
      hardness = form.cleaned_data.get('hardness')
      planing_speed = form.cleaned_data.get('planing_speed')
      control = form.cleaned_data.get('control')
      speed_of_start = form.cleaned_data.get('speed_of_start')
      bottom = form.cleaned_data.get('bottom')
      roll = form.cleaned_data.get('roll')
      edge = form.cleaned_data.get('edge')
      durability = form.cleaned_data.get('durability')
      mouse = form.cleaned_data.get('mouse')
      sole = form.cleaned_data.get('sole')

      if product_name:
        #
        print('product_name = ', product_name)
        query_filters &= Q(product_name=product_name)
      if hardness:
        #
        print('hardness = ', hardness)
        query_filters &= Q(hardness=hardness)
      if planing_speed:
        #
        print('planing_speed = ', planing_speed)
        query_filters &= Q(planing_speed=planing_speed)
      if control:
        #
        print('control = ', control)
        query_filters &= Q(control=control)
      if speed_of_start:
        #
        print('speed_of_start = ', speed_of_start)
        query_filters &= Q(speed_of_start=speed_of_start)
      if bottom:
        #
        print('bottom = ', bottom)
        query_filters &= Q(bottom=bottom)
      if roll:
        #
        print('roll = ', roll)
        query_filters &= Q(roll=roll)
      if edge:
        #
        print('edge = ', edge)
        query_filters &= Q(edge=edge)
      if durability:
        #
        print('durability = ', durability)
        query_filters &= Q(durability=durability)
      if mouse:
        #
        print('mouse = ', mouse)
        query_filters &= Q(mouse__icontains=mouse)
      if sole:
        #
        print('sole = ', sole)
        query_filters &= Q(sole__icontains=sole)

      # Debug
      print('query_filters = ', query_filters)
      # AND検索の実行
      book_list = Book.objects.filter(query_filters)
      return render(request, 'private_list.html', {'book_list': book_list})

    return render(request, 'book_search.html', {'form': form})


class ReviewListView(generic.ListView):
    model = Book
    template_name = 'review_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        # 製品に関連するレビューのみを取得
        product_name = self.kwargs['product_name']
        # マウス、ソール、およびレビューがすべてnullでないものだけをフィルタリング
        queryset = Book.objects.filter(product_name=product_name).exclude(mouse__isnull=True, sole__isnull=True, review__isnull=True)
        # idで昇順にソート
        queryset = queryset.order_by('id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # コンテキストにproduct_nameを追加
        context['product_name'] = self.kwargs['product_name']
        return context


@login_required
def report_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        user = request.user
        # ユーザーがすでにこの本を報告しているかどうかを確認
        if not Report.objects.filter(user=user, book=book).exists():
            # まだ報告されていない場合は新しい報告を作成
            Report.objects.create(user=user, book=book)
            # 本の報告カウントを増やす
            book.report_count += 1
            book.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Already reported'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

# 管理者側
  
class AdminIndexView(generic.TemplateView):
    template_name = "admin_index.html"
  
'''
管理者製品一覧ビュー
AdminProductListView
'''
# 書籍一覧を表示するのでListViewクラスを継承
class AdminProductListView(generic.ListView):
  # 操作の対象はBookモデル
  model = Mousepad
  # book_list.htmlをレンダリング
  template_name = 'product_list.html'
  # 1ページに表示するレコードの件数を設定
  # paginate_by = 2
  context_object_name = 'product_list'

  # get_querysetをオーバーライド
  def get_queryset(self):
    # モデルBookのオブジェクトに
    # order_byを適用して書籍情報作成日時の降順で並べる
    products = Mousepad.objects.order_by('-created_at')
    print("products = ", products)
    return products
  
'''
管理者製品詳細ビュー
AdminProductDetailView
'''
# 書籍情報の詳細を表示するのでDetailViewを継承する
# DetailViewは、pkに格納されたid値を使ってクエリ：
# queryset = queryset.filter(pk=pk)
# を内部で実行するため、DetailViewでクエリ（queryset）を実装する必要はない
# 抽出されたレコードはContextオブジェクトのobjectキーの値として格納されるので、
# 詳細ページのテンプレート「mousepad_detail.html」では、objectキーを指定して
# 各フィールドのデータを取り出すことができる
class AdminProductDetailView(generic.DetailView):
  # クラス変数modelにMousepadを設定
  model = Mousepad
  # book_detail.htmlをレンダリング
  template_name = 'product_detail.html'

'''
製品登録ビュー
AdminProductAddView
'''
class AdminProductAddView(generic.CreateView):
  # クラス変数modelにMouseを設定
  model = Mousepad
  # product_add.htmlをレンダリング
  template_name = 'product_add.html'
  # クラス変数 form_class をオーバーライド
  # フォーム（AdminProductAddForm）を利用する
  form_class = AdminProductAddForm
  # クラス変数 success_url をオーバーライド
  # 正常に処理が完了したときは、product_list.html に遷移する
  # URLが固定のページに遷移させる
  success_url = reverse_lazy('library:product_list')

  # オーバーライド
  # フォームのバリデーションに問題がなければ実行される
  def form_valid(self, form):
    # commit=FalseにしてPOSTされたデータを取得
    mousepad = form.save(commit=False)
    # 実際にデータベースに保存
    mousepad.save()
    messages.success(self.request, '製品情報を作成しました。')
    return super().form_valid(form)

  # オーバーライド
  # フォームバリデーションが失敗したときに実行される
  def form_invalid(self, form):
    # エラーメッセージを画面に表示する
    messages.error(self.request, "製品情報の作成に失敗しました。")
    return super().form_invalid(form)
  
'''
製品更新ビュー
AdminProductUpdateView
'''
class AdminProductUpdateView(generic.UpdateView):
  model = Mousepad
  # diary_update.htmlをレンダリング
  template_name = 'product_update.html'
  form_class = AdminProductAddForm

  # オーバーライド
  # URLが動的に変化するページに遷移させる
  def get_success_url(self):
    return reverse_lazy('library:product_detail', kwargs={'pk': self.kwargs['pk']})

  # バリデーションが成功したときに呼び出され、モデルへの更新処理が実行される。
  def form_valid(self, form):
    messages.success(self.request, '製品情報を更新しました。')
    return super().form_valid(form)

  # バリデーションが失敗したときに呼び出される。
  def form_invalid(self, form):
    messages.error(self.request, "製品情報の更新に失敗しました。")
    return super().form_invalid(form)

'''
製品情報削除ビュー
AdminProductDeleteView
'''
class AdminProductDeleteView(generic.DeleteView):
  model = Mousepad
  # book_delete.htmlをレンダリング
  template_name = 'product_delete.html'
  success_url = reverse_lazy('library:product_list')

  def delete(self, request, *args, **kwargs):
    messages.success(self.request, "製品情報を削除しました。")
    return super().delete(request, *args, **kwargs)

'''
製品情報検索ビュー
AdminProductSearchView
'''
# 検索結果一覧を表示するのでListViewクラスを継承
class AdminProductSearchView(generic.FormView):
  # フォーム（BookSearchForm）とBookSearchViewを紐づけるために
  # クラス変数（form_class）をオーバーライド
  form_class = AdminProductSearchForm
  # book_search.htmlをレンダリング
  template_name = 'product_search.html'

  # 検索実行
  def post(self, request):
    form = AdminProductSearchForm(request.POST)
    if form.is_valid():
      query_filters = Q()
      product = form.cleaned_data.get('product')
      maker = form.cleaned_data.get('maker')
      if product:
        #
        print('product = ', product)
        query_filters &= Q(product__icontains=product)
      if maker:
        #
        print('maker = ', maker)
        query_filters &= Q(maker__icontains=maker)

      # Debug
      print('query_filters = ', query_filters)
      # AND検索の実行
      product_list = Mousepad.objects.filter(query_filters)
      return render(request, 'product_list.html', {'product_list': product_list})

    return render(request, 'product_search.html', {'form': form})