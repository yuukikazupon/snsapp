# Generated by Django 3.1.2 on 2021-02-22 12:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='ユーザー名')),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(150)], verbose_name='年齢')),
                ('sex', models.CharField(choices=[['男性', '男性'], ['女性', '女性']], max_length=10, verbose_name='性別')),
                ('address', models.CharField(choices=[['北海道', '北海道'], ['青森県', '青森県'], ['秋田県', '秋田県'], ['岩手県', '岩手県'], ['山形県', '山形県'], ['宮城県', '宮城県'], ['新潟県', '新潟県'], ['福島県', '福島県'], ['栃木県', '栃木県'], ['茨城県', '茨城県'], ['石川県', '石川県'], ['富山県', '富山県'], ['群馬県', '群馬県'], ['埼玉県', '埼玉県'], ['千葉県', '千葉県'], ['長野県', '長野県'], ['山梨県', '山梨県'], ['東京都', '東京都'], ['神奈川県', '神奈川県'], ['福井県', '福井県'], ['岐阜県', '岐阜県'], ['静岡県', '静岡県'], ['京都府', '京都府'], ['滋賀県', '滋賀県'], ['愛知県', '愛知県'], ['三重県', '三重県'], ['鳥取県', '鳥取県'], ['兵庫県', '兵庫県'], ['大阪府', '大阪府'], ['奈良県', '奈良県'], ['島根県', '島根県'], ['岡山県', '岡山県'], ['和歌山県', '和歌山県'], ['広島県', '広島県'], ['香川県', '香川県'], ['徳島県', '徳島県'], ['山口県', '山口県'], ['愛媛県', '愛媛県'], ['高知県', '高知県'], ['福岡県', '福岡県'], ['大分県', '大分県'], ['佐賀県', '佐賀県'], ['熊本県', '熊本県'], ['宮崎県', '宮崎県'], ['長崎県', '長崎県'], ['鹿児島県', '鹿児島県'], ['沖縄県', '沖縄県']], max_length=10, verbose_name='都道府県')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('profileid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True, verbose_name='メッセージ')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/media/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('recievemessageid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.profile')),
                ('sendmessageid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Keijiban',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toukou', models.TextField(verbose_name='投稿内容')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/media/', verbose_name='画像')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('good', models.IntegerField(blank=True, default=0, null=True)),
                ('goodtext', models.CharField(blank=True, default='👍', max_length=10000, null=True)),
                ('authorid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentfield', models.TextField(verbose_name='コメント')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('commentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.keijiban')),
                ('commentprofileid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.profile')),
            ],
        ),
    ]
