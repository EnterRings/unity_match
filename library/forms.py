from django import forms

from .models import Book, Mousepad

'''
書籍登録フォーム
BookAddForm
'''
class BookAddForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'product_name',
            'hardness',
            'planing_speed',
            'control',
            'speed_of_start',
            'bottom',
            'roll',
            'edge',
            'durability',
            'mouse',
            'sole',
            'review',
        )
        widgets = {
            'review': forms.Textarea(attrs={'rows': 5, 'cols': 40}),  # 'rows'と'cols'でサイズを指定
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mousepadモデルから製品名の選択肢を取得し、重複を除外する
        mousepad_product_names = Mousepad.objects.values_list('product', flat=True).distinct()

        # 選択肢を更新
        self.fields['product_name'].widget = forms.Select(choices=[(name, name) for name in mousepad_product_names])
        
        for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'




'''
書籍検索フォーム
BookSearchForm
'''
class BookSearchForm(forms.Form):
  # 製品名

  # 硬度
  HARDNESS_CHOICES = [
    ("", "選択してください"),
    ("柔らかい", "柔らかい"),
    ("普通", "普通"),
    ("硬い", "硬い"),
  ]

  # 滑走速度
  PLANING_SPEED_CHOICES = [
    ("", "選択してください"),
    ("かなり滑らない", "かなり滑らない"),
    ("滑らない", "滑らない"),
    ("普通", "普通"),
    ("滑る", "滑る"),
    ("かなり滑る", "かなり滑る"),
  ]

  # コントロール性
  CONTROL_CHOICES = [
    ("", "選択してください"),
    ("止めやすい", "止めやすい"),
    ("普通", "普通"),
    ("止めにくい", "止めにくい"),
  ]

  # 滑り出しの速さ
  SPEED_OF_START_CHOICES = [
    ("", "選択してください"),
    ("非常に軽い", "非常に軽い"),
    ("軽い", "軽い"),
    ("標準", "標準"),
    ("鈍い", "鈍い"),
    ("非常に鈍い", "非常に鈍い"),
  ]

  # 底面
  BOTTOM_CHOICES = [
    ("", "選択してください"),
    ("滑る", "滑る"),
    ("滑らない", "滑らない"),
    ("吸着する", "吸着する"),
  ]

  # 巻き癖
  ROLL_CHOICES = [
    ("", "選択してください"),
    ("なし", "なし"),
    ("中程度", "中程度"),
    ("あり", "あり"),
  ]

  # ステッチ加工
  EDGE_CHOICES = [
    ("", "選択してください"),
    ("なし", "なし"),
    ("低い", "低い"),
    ("高い", "高い"),
  ]

  # 耐久性
  DURABILITY_CHOICES = [
    ("", "選択してください"),
    ("低い", "低い"),
    ("普通", "普通"),
    ("高い", "高い"),
  ]
  
  # フォームのフィールドをクラス変数として定義
  """
  product_name = forms.ChoiceField(
    label='製品名', 
    widget=forms.widgets.Select, 
    choices=PRODUCT_NAME_CHOICES,
    required=False,
  )
  """
  product_name = forms.ModelChoiceField(
    label='製品名',
    # queryset=Book.objects.none(),
    queryset=Mousepad.objects.all(),
    widget=forms.widgets.Select,
    required=False,
  )


  hardness = forms.ChoiceField(
    label='硬度',
    widget=forms.widgets.Select,
    choices=HARDNESS_CHOICES,
    required=False,
  )
  planing_speed = forms.ChoiceField(
    label='滑走速度',
    widget=forms.widgets.Select,
    choices=PLANING_SPEED_CHOICES,
    required=False,
  )
  control = forms.ChoiceField(
    label='コントロール性',
    widget=forms.widgets.Select,
    choices=CONTROL_CHOICES,
    required=False,
  )
  speed_of_start = forms.ChoiceField(
    label='滑り出しの速さ',
    widget=forms.widgets.Select,
    choices=SPEED_OF_START_CHOICES,
    required=False,
  )
  bottom = forms.ChoiceField(
    label='底面',
    widget=forms.widgets.Select,
    choices=BOTTOM_CHOICES,
    required=False,
  )
  roll = forms.ChoiceField(
    label='巻き癖',
    widget=forms.widgets.Select,
    choices=ROLL_CHOICES,
    required=False,
  )
  edge = forms.ChoiceField(
    label='エッジ加工',
    widget=forms.widgets.Select,
    choices=EDGE_CHOICES,
    required=False,
  )
  durability = forms.ChoiceField(
    label='耐久性',
    widget=forms.widgets.Select,
    choices=DURABILITY_CHOICES,
    required=False,
  )
  mouse = forms.CharField(label='使用マウス', max_length=40, required=False)
  sole = forms.CharField(label='使用ソール', max_length=40, required=False)
  
  # BookSearchFromのコンストラクタ
  def __init__(self, *args, **kwargs):
    #
    FORM_FIELD_DICT = {
      'product_name' : '製品名を選択',
      'hardness' : '硬度を選択',
      'planing_speed' : '滑走速度を選択',
      'control' : 'コントロール性を選択',
      'speed_of_start' : '滑り出しの速さを選択',
      'bottom' : '底面を選択',
      'roll' : '巻き癖を選択',
      'edge' : 'ステッチ加工を選択',
      'durability' : '耐久性を選択',
      'mouse' : '使用マウスを入力',
      'sole' : '使用ソールを入力',
    }
    # フィールドの初期化を行う
    super().__init__(*args, **kwargs)

    # 全フォームのフィールドに一括でBootstrapのform-controlクラスを追加する
    for key, value in FORM_FIELD_DICT.items():
      # <input>タグのclass属性を設定
      self.fields[key].widget.attrs['class'] = 'form-control'
      # placeholderにメッセージを登録
      self.fields[key].widget.attrs['placeholder'] = value




# 管理者側
'''
製品情報登録フォーム
AdminProductAddForm
'''
class AdminProductAddForm(forms.ModelForm):
  class Meta:
    model = Mousepad
    fields = (
      'product',        # 製品名
      'maker',          # メーカー
      'material',       # 材質
      'size',           # サイズ
      'price',          # 値段
      'summary',        # 概要
      'image',          # 画像 imageフォルダ内の画像へのパス
      'link',           # 公式ページのリンク
    )

  # 全フォームのフィールドに一括でBootstrapのform-controlクラスを追加する
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

'''
製品情報検索フォーム
BookSearchForm
'''
class AdminProductSearchForm(forms.Form):  
  # フォームのフィールドをクラス変数として定義
  product = forms.CharField(label='製品名', max_length=40, required=False)
  maker = forms.CharField(label='メーカー', max_length=40, required=False)
  
  # AdminProductSearchFormのコンストラクタ
  def __init__(self, *args, **kwargs):
    #
    FORM_FIELD_DICT = {
      'product' : '製品名を入力',
      'maker' : 'メーカーを入力',
    }
    # フィールドの初期化を行う
    super().__init__(*args, **kwargs)

    # 全フォームのフィールドに一括でBootstrapのform-controlクラスを追加する
    for key, value in FORM_FIELD_DICT.items():
      # <input>タグのclass属性を設定
      self.fields[key].widget.attrs['class'] = 'form-control'
      # placeholderにメッセージを登録
      self.fields[key].widget.attrs['placeholder'] = value
