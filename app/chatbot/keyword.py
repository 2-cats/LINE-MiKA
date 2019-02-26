from linebot.models import TextSendMessage

from .. import db
from ..models import Keyword


def keyword_query(keyword):
    keyword = Keyword.query.filter_by(
        keyword=keyword
    ).first()
    if keyword:
        return TextSendMessage(text=keyword.reply)
    return 0
