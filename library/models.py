from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

# Create your models here.
# マウスパッドモデル
class Mousepad(models.Model):
  # 製品名
  product = models.CharField(
    verbose_name='製品名', # フィールドのタイトル
    max_length=80
  )
  # メーカー名
  maker = models.CharField(
    verbose_name='メーカー名', # フィールドのタイトル 
    max_length=80, 
  )
  # 材質
  material = models.CharField(
    verbose_name='材質', # フィールドのタイトル 
    max_length=80, 
    blank=True, null=True
  )
  # サイズ
  size = models.CharField(
    verbose_name='サイズ', # フィールドのタイトル 
    max_length=80, 
    blank=True, null=True
  )
  # 値段
  price = models.PositiveIntegerField(
    verbose_name='値段', # フィールドのタイトル 
    blank=True, null=True
  )
  # 概要
  summary = models.TextField(
    verbose_name='概要', # フィールドのタイトル
    blank=True, null=True
  )
  # 画像
  image = models.ImageField(
    verbose_name='画像', # フィールドのタイトル
    upload_to='static/assets/img',
    blank=True, null=True
  )
  # リンク
  link = models.CharField(
    verbose_name='公式サイトリンク', # フィールドのタイトル
    max_length=80, 
    blank=True, null=True
  )
  # 作成日時
  created_at = models.DateTimeField(
    verbose_name='作成日時', # フィールドのタイトル 
    auto_now_add=True
  )
  # 更新日時
  updated_at = models.DateTimeField(
    verbose_name='更新日時', # フィールドのタイトル 
    auto_now=True
  )

  class Meta:
    verbose_name_plural = 'Mousepad'

  def __str__(self):
    return self.product

# 書籍情報モデル
class Book(models.Model):
  # 製品名
  product_name = models.CharField(
    verbose_name='製品名', # フィールドのタイトル
    max_length=30,
    default="",
    blank=True,
    null=True,
  )

  # 硬度
  HARDNESS_CHOICES = [
    ("柔らかい", "柔らかい"),
    ("普通", "普通"),
    ("硬い", "硬い"),
  ]
  hardness = models.CharField(
    verbose_name='硬度', # フィールドのタイトル
    max_length=4,
    choices=HARDNESS_CHOICES,
    default="",
  )

  # 滑走速度
  PLANING_SPEED_CHOICES = [
    ("かなり滑らない", "かなり滑らない"),
    ("滑らない", "滑らない"),
    ("普通", "普通"),
    ("滑る", "滑る"),
    ("かなり滑る", "かなり滑る"),
  ]
  planing_speed = models.CharField(
    verbose_name='滑走速度', # フィールドのタイトル
    max_length=8,
    choices=PLANING_SPEED_CHOICES,
    default="",
  )

  # コントロール性
  CONTROL_CHOICES = [
    ("止めやすい", "止めやすい"),
    ("普通", "普通"),
    ("止めにくい", "止めにくい"),
  ]
  control = models.CharField(
    verbose_name='コントロール性', # フィールドのタイトル
    max_length=5,
    choices=CONTROL_CHOICES,
    default="",
  )

  # 滑り出しの速さ
  SPEED_OF_START_CHOICES = [
    ("非常に軽い", "非常に軽い"),
    ("軽い", "軽い"),
    ("標準", "標準"),
    ("鈍い", "鈍い"),
    ("非常に鈍い", "非常に鈍い"),
  ]
  speed_of_start = models.CharField(
    verbose_name='滑り出しの速さ', # フィールドのタイトル
    max_length=5,
    choices=SPEED_OF_START_CHOICES,
    default="",
  )

  # 底面
  BOTTOM_CHOICES = [
    ("滑る", "滑る"),
    ("滑らない", "滑らない"),
    ("吸着する", "吸着する"),
  ]
  bottom = models.CharField(
    verbose_name='底面', # フィールドのタイトル
    max_length=4,
    choices=BOTTOM_CHOICES,
    default="",
  )

  # 巻き癖
  ROLL_CHOICES = [
    ("なし", "なし"),
    ("中程度", "中程度"),
    ("あり", "あり"),
  ]
  roll = models.CharField(
    verbose_name='巻き癖', # フィールドのタイトル
    max_length=3,
    choices=ROLL_CHOICES,
    default="",
  )

  # ステッチ加工
  EDGE_CHOICES = [
    ("なし", "なし"),
    ("低い", "低い"),
    ("高い", "高い"),
  ]
  edge = models.CharField(
    verbose_name='ステッチ加工', # フィールドのタイトル
    max_length=2,
    choices=EDGE_CHOICES,
    default="",
  )

  # 耐久性
  DURABILITY_CHOICES = [
    ("低い", "低い"),
    ("普通", "普通"),
    ("高い", "高い"),
  ]
  durability = models.CharField(
    verbose_name='耐久性', # フィールドのタイトル
    max_length=2,
    choices=DURABILITY_CHOICES,
    default="",
  )

  # 使用しているマウス
  mouse = models.CharField(
    verbose_name='マウス', # フィールドのタイトル
    max_length=40,
    blank=True, null=True
  )
  # 使用しているソール
  sole = models.CharField(
    verbose_name='ソール', # フィールドのタイトル
    max_length=40,
    blank=True, null=True
  )
  # レビュー
  review = models.CharField(
    verbose_name='レビュー', # フィールドのタイトル 
    blank=True, null=True
  )

  # レポートされた回数
  report_count = models.PositiveIntegerField(default=0)

  # レポートのレベル
  REPORT_LEVEL_CHOICES = [
      (1, "低"),
      (2, "中"),
      (3, "高"),
      (4, "非常に高"),
      (5, "極めて高"),
  ]
  report = models.PositiveIntegerField(
      verbose_name='報告レベル',
      choices=REPORT_LEVEL_CHOICES,
      default=1,
  )

  # on_delete=models.CASCADE
  create_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, null=True, blank=True)

  class Meta:
    verbose_name_plural = 'Book'

  def __str__(self):
    return self.product_name
  
# 報告モデル
class Report(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reports",)
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'book'], name='unique_report_per_user')
        ]