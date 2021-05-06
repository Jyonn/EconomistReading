from SmartDjango import models, E
from django.utils.crypto import get_random_string


@E.register(id_processor=E.idp_cls_prefix)
class EconomistError:
    GET = E('找不到阅读', hc=404)
    CREATE = E('添加阅读失败', hc=401)
    PARAGRAPH_CREATE = E("添加阅读章节失败", hc=401)


class Economist(models.Model):
    news_id = models.CharField(
        max_length=4,
        min_length=4,
    )

    date = models.CharField(
        max_length=10,
        min_length=10,
    )

    category = models.TextField()

    sub_headline = models.TextField()

    headline = models.TextField()

    description = models.TextField()

    image = models.TextField()

    url = models.TextField(default=None)

    @classmethod
    def get(cls, news_id):
        try:
            return cls.objects.get(news_id=news_id)
        except cls.DoesNotExist:
            raise EconomistError.GET

    @classmethod
    def generate_id(cls):
        while True:
            news_id = get_random_string(length=4)
            try:
                cls.get(news_id)
            except E as e:
                assert e.eis(EconomistError.GET)
                return news_id

    @classmethod
    def create(cls, **kwargs):
        try:
            return cls.objects.create(
                news_id=cls.generate_id(),
                **kwargs,
            )
        except Exception:
            raise EconomistError.CREATE

    def d_list(self):
        return self.dictify('news_id', 'date', 'category', 'headline', 'sub_headline', 'description', 'image')

    def d(self):
        d_ = self.d_list()
        d_.update(dict(paragraph=Paragraph.get(self)))
        return d_


class Paragraph(models.Model):
    content = models.TextField()

    section = models.BooleanField()

    economist = models.ForeignKey(
        Economist,
        on_delete=models.CASCADE,
    )

    words = models.IntegerField(
        default=0,
    )

    @classmethod
    def create(cls, content: str, **kwargs):
        try:
            return cls.objects.create(
                content=content,
                words=len(content.split(' ')),
                **kwargs
            )
        except Exception:
            raise EconomistError.PARAGRAPH_CREATE

    @classmethod
    def get(cls, economist: Economist):
        return cls.objects.filter(economist=economist).order_by('pk')

    def d(self):
        return self.dictify('content', 'section')
