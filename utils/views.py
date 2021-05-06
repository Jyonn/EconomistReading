import datetime

from django.views import View

from Config.models import CI, Config
from Economist.models import Economist, Paragraph
from utils.configuration import SPIDER


class GrabView(View):
    @staticmethod
    def get(_):
        today = datetime.datetime.now().date().strftime('%Y-%m-%d')
        update_date = Config.get_value_by_key(CI.UPDATE_DATE, '1900-01-01')
        # update_date = datetime.datetime.strptime(update_date, '%Y-%m-%d').date()

        if today == update_date:
            return 0

        news = SPIDER.grab_today_news()

        economist = Economist.create(
            date=today,
            **news.d(),
        )

        for content, section in zip(news.body, news.section):
            Paragraph.create(
                content=content,
                section=section,
                economist=economist,
            )

        Config.update_value(CI.UPDATE_DATE, today)

        return 0
