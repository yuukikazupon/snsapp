from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator



GENDER_CHOICE=[["男性","男性"],["女性","女性"]]
ADDRESS_CHOICE=[["北海道","北海道"],["青森県","青森県"],["秋田県","秋田県"],["岩手県","岩手県"],["山形県","山形県"],\
["宮城県","宮城県"],["新潟県","新潟県"],["福島県","福島県"],["栃木県","栃木県"],["茨城県","茨城県"],["石川県","石川県"],\
["富山県","富山県"],["群馬県","群馬県"],["埼玉県","埼玉県"],["千葉県","千葉県"],["長野県","長野県"],["山梨県","山梨県"],\
["東京都","東京都"],["神奈川県","神奈川県"],["福井県","福井県"],["岐阜県","岐阜県"],["静岡県","静岡県"],["京都府","京都府"],\
["滋賀県","滋賀県"],["愛知県","愛知県"],["三重県","三重県"],["鳥取県","鳥取県"],["兵庫県","兵庫県"],["大阪府","大阪府"],\
["奈良県","奈良県"],["島根県","島根県"],["岡山県","岡山県"],["和歌山県","和歌山県"],["広島県","広島県"],["香川県","香川県"],\
["徳島県","徳島県"],["山口県","山口県"],["愛媛県","愛媛県"],["高知県","高知県"],["福岡県","福岡県"],["大分県","大分県"],\
["佐賀県","佐賀県"],["熊本県","熊本県"],["宮崎県","宮崎県"],["長崎県","長崎県"],["鹿児島県","鹿児島県"],["沖縄県","沖縄県"]]



class Profile(models.Model):
    profileid=models.OneToOneField('accounts.CustomUser',on_delete=models.CASCADE)
    username=models.CharField('ユーザー名',max_length=30)
    age = models.PositiveIntegerField('年齢',validators=[MinValueValidator(0),MaxValueValidator(150)])
    sex = models.CharField('性別',
        max_length=10,
        choices = GENDER_CHOICE,
    )
    address = models.CharField('都道府県',
        max_length=10,
        choices = ADDRESS_CHOICE,
        )
    icon = models.ImageField(upload_to="media/",null=True,blank=True)



class Keijiban(models.Model) :
    authorid = models.ForeignKey('accounts.CustomUser',on_delete=models.CASCADE)
    toukou = models.TextField('投稿内容')
    image = models.ImageField('画像',upload_to="media/media/",null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    good = models.IntegerField(null=True,blank=True,default=0)
    goodtext = models.CharField(max_length=10000,null=True,blank=True,default="👍")


class Comment(models.Model):
    commentid=models.ForeignKey(Keijiban,on_delete=models.CASCADE)
    commentprofileid=models.ForeignKey(Profile,on_delete=models.CASCADE)
    commentfield=models.TextField('コメント')
    created_at = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    sendmessageid = models.ForeignKey('accounts.CustomUser',on_delete=models.CASCADE)
    recievemessageid = models.ForeignKey(Profile,on_delete=models.CASCADE)
    message = models.TextField('メッセージ',null=True,blank=True)
    image = models.ImageField(upload_to = "media/media/",null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
