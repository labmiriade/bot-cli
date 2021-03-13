from unittest.mock import MagicMock

import requests_mock
from fcache.cache import FileCache

from src.repositories.bot import Bot


def test_commesse(requests_mock):
    commesse = [{"a": 1}, {"a": 2}]
    current_user = {'userId': '1234567890'}
    current_res = {'resId': '0987654321'}
    requests_mock.get(
        "https://bot.miriade.it/api/jsonws/rapportini.rapportino/find-active-commessa-with-residuo-by-res-id",
        json=commesse,
    )
    requests_mock.get(
        "https://bot.miriade.it/api/jsonws/user/get-current-user",
        json=current_user,
    )
    requests_mock.get(
        "https://bot.miriade.it/api/jsonws/anagrafichecore.tecnico/find-by-user",
        json=current_res,
    )
    # init Bot
    bot = Bot(username='pippo', password='clarabella')
    bot.cache = {}
    # test the commesse are the one provided by the API
    assert bot.commesse == commesse
    # test the cache has been updated
    assert len(bot.cache) == 3
    values = list(bot.cache.values())
    assert commesse in values
    assert '1234567890' in values
    assert '0987654321' in values
    # ask again for commesse but before reset mock
    requests_mock.reset_mock()
    assert bot.commesse == commesse
