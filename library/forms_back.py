from django import forms

from .models import Book

'''
書籍登録フォーム
BookAddForm
'''
class BookAddForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = (
      'title',        # 書名
      'author',       # 著者名
      'field',        # 分野
      'publisher',    # 出版社
      'pub_year',     # 出版年
      'page_number',  # ページ数
      'summary',      # 概要
      'memo',         # メモ
      'price',        # 価格
      'isbn',         # ISBN
    )

  # 全フォームのフィールドに一括でBootstrapのform-controlクラスを追加する
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

'''
書籍検索フォーム
BookSearchForm
'''
class BookSearchForm(forms.Form):
  # 書籍の分野
  BOOK_FIELD_CHOICES = [
    ("", "選択してください"),
    ("00", "総記"),
    ("10", "哲学"),
    ("20", "歴史、世界史、文化史"),
    ("30", "社会科学"),
    ("50", "技術、工学"),
    ("60", "産業"),
    ("70", "芸術、美術"),
    ("80", "言語"),
  ]
  
  # フォームのフィールドをクラス変数として定義
  title = forms.CharField(label='書名', max_length=40, required=False)
  author = forms.CharField(label='著者名', max_length=40, required=False)
  field = forms.ChoiceField(
    label='分野', 
    widget=forms.widgets.Select, 
    choices=BOOK_FIELD_CHOICES,
    required=False,
  )
  publisher = forms.CharField(label='出版社', max_length=40, required=False)
  pub_year = forms.IntegerField(label='出版年', required=False)
  page_number = forms.IntegerField(label='ページ数', required=False)
  price = forms.IntegerField(label='価格', required=False)
  isbn = forms.CharField(label='ISBN', max_length=40, required=False)
  
  # BookSearchFromのコンストラクタ
  def __init__(self, *args, **kwargs):
    #
    FORM_FIELD_DICT = {
      'title' : '書名を入力',
      'author' : '著者名を入力',
      'field' : '分野を選択',
      'publisher' : '出版社を入力',
      'pub_year' : '出版年上限を入力',
      'page_number' : 'ページ数上限を入力',
      'price' : '価格上限を入力',
      'isbn' : 'ISBNを入力',
    }
    # フィールドの初期化を行う
    super().__init__(*args, **kwargs)

    # 全フォームのフィールドに一括でBootstrapのform-controlクラスを追加する
    for key, value in FORM_FIELD_DICT.items():
      # <input>タグのclass属性を設定
      self.fields[key].widget.attrs['class'] = 'form-control'
      # placeholderにメッセージを登録
      self.fields[key].widget.attrs['placeholder'] = value

      # 'product_name',        # 製品名
      # *'hardness',        # 硬度　やわらかい　普通　かたい
      # *'planing_speed',    # 滑走速度　任意　五段階dかなり滑る滑らない
      #　*control コントロール性　止めやすい　普通　止めにくい
      # *speed_​​of_start 滑り出しの速さ　非常に軽い　軽い　標準　鈍い　かなり鈍い
      # *'bottom',     # 底面　吸着する　滑る　滑らない
      # *'roll',      # 巻き癖　ある　中程度　なし
      # *edge, ステッチ　ありなし　高い　低い
      # *durability 耐久性　高い　普通　低い
      # 'compatibility',     # マウス使用してる
      #  sole ソール使用してrう
      # review textarea　レビュー　他のマウスパッドとの比較や机の材質、マウス・ソール相性についての詳細情報などを記入してください。