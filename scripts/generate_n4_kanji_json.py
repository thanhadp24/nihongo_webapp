import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests


OUTPUT = Path("database/import/jlpt_n4_kanji_by_topic_db_import.json")
KANJI_API_CACHE = Path("tmp/cache/kanjiapi_n4.json")
ENRICH_KANJI_API = os.environ.get("ENRICH_KANJI_API", "1") != "0"


TOPICS = [
    (1, 1, 1, "家族", "かぞく", "Gia đình", 7, "家族兄弟姉妹私育"),
    (2, 1, 2, "マンション", "マンション", "Căn hộ", 13, "部屋広低緑静近遠"),
    (3, 1, 3, "しごと", "しごと", "Công việc", 19, "会社働作工場始終"),
    (4, 2, 1, "レジ", "レジ", "Quầy tính tiền", 29, "店客親切売当品"),
    (5, 2, 2, "店内", "てんない", "Bên trong cửa hàng", 35, "便利使銀白黒紙"),
    (6, 2, 3, "24時間", "にじゅうよじかん", "Hai mươi bốn giờ", 41, "朝晩昼夜前後午早"),
    (7, 3, 1, "荷物", "にもつ", "Hành lý và gửi đồ", 51, "荷送宅急速遅重軽"),
    (8, 3, 2, "あて先", "あてさき", "Địa chỉ người nhận", 57, "住所様主番地号"),
    (9, 3, 3, "都道府県", "とどうふけん", "Tỉnh thành Nhật Bản", 63, "京都道府県市区村"),
    (10, 4, 1, "デート", "デート", "Hẹn hò", 73, "毎週映画図館公園"),
    (11, 4, 2, "けっこんきねん日", "けっこんきねんび", "Ngày kỷ niệm kết hôn", 79, "夫妻特思料理有"),
    (12, 4, 3, "ファッション", "ファッション", "Thời trang", 85, "洋服衣短毛糸玉光"),
    (13, 5, 1, "駅", "えき", "Nhà ga", 97, "駅鉄乗降開閉発着"),
    (14, 5, 2, "交さてん", "こうさてん", "Giao lộ", 103, "交通台止色赤黄青"),
    (15, 5, 3, "病院", "びょういん", "Bệnh viện", 109, "病院医科薬待合計"),
    (16, 6, 1, "研究", "けんきゅう", "Nghiên cứu", 119, "研究語文英化数心"),
    (17, 6, 2, "合コン", "ごうコン", "Gặp gỡ nhóm", 125, "若集知酒歌声楽"),
    (18, 6, 3, "ラーメン屋", "ラーメンや", "Quán mì ramen", 131, "味油太細皿飯麦"),
    (19, 7, 1, "きせつ", "きせつ", "Bốn mùa", 141, "春夏秋冬空星雲去"),
    (20, 7, 2, "天気", "てんき", "Thời tiết", 147, "天晴雪風強弱暑寒"),
    (21, 7, 3, "旅行", "りょこう", "Du lịch", 153, "旅持世界写真船"),
    (22, 8, 1, "勉強", "べんきょう", "Học tập", 163, "勉漢宿題質問教室"),
    (23, 8, 2, "テスト", "テスト", "Bài kiểm tra", 169, "試験答考正丸不同"),
    (24, 8, 3, "社会科", "しゃかいか", "Môn xã hội", 175, "政治経済歴史国王"),
    (25, 9, 1, "運動", "うんどう", "Vận động", 185, "運動練習走歩泳才"),
    (26, 9, 2, "リゾート", "リゾート", "Khu nghỉ dưỡng", 191, "自然草原湖谷海辺"),
    (27, 9, 3, "いなか", "いなか", "Nông thôn", 197, "里野奥池虫羽鳴馬"),
]


KANJI_ROWS = """
家\tgia\tnhà, gia đình\t家族\tかぞく\tgia đình
族\ttộc\tgia tộc, nhóm\t家族\tかぞく\tgia đình
兄\thuynh\tanh trai\t兄\tあに\tanh trai tôi
弟\tđệ\tem trai\t弟\tおとうと\tem trai tôi
姉\ttỉ\tchị gái\t姉\tあね\tchị gái tôi
妹\tmuội\tem gái\t妹\tいもうと\tem gái tôi
私\ttư\ttôi, riêng tư\t私\tわたし\ttôi
育\tdục\tnuôi dưỡng\t育てる\tそだてる\tnuôi dưỡng
部\tbộ\tbộ phận\t部屋\tへや\tphòng
屋\tốc\tnhà, cửa hàng\t部屋\tへや\tphòng
広\tquảng\trộng\t広い\tひろい\trộng
低\tđê\tthấp\t低い\tひくい\tthấp
緑\tlục\tmàu xanh lá\t緑\tみどり\tmàu xanh lá
静\ttĩnh\tyên tĩnh\t静か\tしずか\tyên tĩnh
近\tcận\tgần\t近い\tちかい\tgần
遠\tviễn\txa\t遠い\tとおい\txa
会\thội\tgặp, hội\t会社\tかいしゃ\tcông ty
社\txã\tcông ty, đền thờ\t会社\tかいしゃ\tcông ty
働\tđộng\tlàm việc\t働く\tはたらく\tlàm việc
作\ttác\tlàm, tạo ra\t作る\tつくる\tlàm, tạo ra
工\tcông\tcông nghiệp, thợ\t工場\tこうじょう\tnhà máy
場\ttrường\tnơi, địa điểm\t工場\tこうじょう\tnhà máy
始\tthuỷ\tbắt đầu\t始まる\tはじまる\tbắt đầu
終\tchung\tkết thúc\t終わる\tおわる\tkết thúc
店\tđiếm\tcửa hàng\t店\tみせ\tcửa hàng
客\tkhách\tkhách hàng\tお客さん\tおきゃくさん\tkhách hàng
親\tthân\tcha mẹ, thân thiết\t親切\tしんせつ\ttử tế
切\tthiết\tcắt, thiết tha\t親切\tしんせつ\ttử tế
売\tmại\tbán\t売る\tうる\tbán
当\tđương\ttrúng, đúng\t弁当\tべんとう\tcơm hộp
品\tphẩm\tsản phẩm\t品物\tしなもの\thàng hóa
便\ttiện\ttiện lợi\t便利\tべんり\ttiện lợi
利\tlợi\tlợi ích, tiện\t便利\tべんり\ttiện lợi
使\tsử\tsử dụng\t使う\tつかう\tsử dụng
銀\tngân\tbạc\t銀行\tぎんこう\tngân hàng
白\tbạch\tmàu trắng\t白い\tしろい\ttrắng
黒\thắc\tmàu đen\t黒い\tくろい\tđen
紙\tchỉ\tgiấy\t紙\tかみ\tgiấy
朝\ttriều\tbuổi sáng\t朝\tあさ\tbuổi sáng
晩\tvãn\tbuổi tối\t晩\tばん\tbuổi tối
昼\ttrú\tbuổi trưa\t昼\tひる\tbuổi trưa
夜\tdạ\tban đêm\t夜\tよる\tban đêm
前\ttiền\ttrước\t前\tまえ\tphía trước
後\thậu\tsau\t後\tあと\tsau đó
午\tngọ\tbuổi trưa\t午前\tごぜん\tbuổi sáng
早\ttảo\tsớm\t早い\tはやい\tsớm
荷\thà\thành lý, hàng hóa\t荷物\tにもつ\thành lý
送\ttống\tgửi, tiễn\t送る\tおくる\tgửi
宅\ttrạch\tnhà\t自宅\tじたく\tnhà riêng
急\tcấp\tgấp, nhanh\t急ぐ\tいそぐ\tvội
速\ttốc\tnhanh\t速い\tはやい\tnhanh
遅\ttrì\tmuộn, chậm\t遅い\tおそい\tmuộn, chậm
重\ttrọng\tnặng\t重い\tおもい\tnặng
軽\tkhinh\tnhẹ\t軽い\tかるい\tnhẹ
住\ttrú\tsống, cư trú\t住む\tすむ\tsống
所\tsở\tnơi chốn\t住所\tじゅうしょ\tđịa chỉ
様\tdạng\tngài, dáng vẻ\t様\tさま\tngài
主\tchủ\tchủ yếu, chủ nhà\t主人\tしゅじん\tchồng, chủ nhà
番\tphiên\tsố lượt, thứ tự\t番号\tばんごう\tsố
地\tđịa\tđất, nơi\t番地\tばんち\tsố đất, địa chỉ
号\thiệu\tsố hiệu\t番号\tばんごう\tsố hiệu
京\tkinh\tkinh đô\t東京\tとうきょう\tTokyo
都\tđô\tthủ đô\t京都\tきょうと\tKyoto
道\tđạo\tđường\t道路\tどうろ\tđường bộ
府\tphủ\tphủ, đơn vị hành chính\t大阪府\tおおさかふ\tphủ Osaka
県\thuyện\ttỉnh\t県\tけん\ttỉnh
市\tthị\tthành phố\t市\tし\tthành phố
区\tkhu\tquận, khu\t区\tく\tquận
村\tthôn\tlàng\t村\tむら\tlàng
毎\tmỗi\tmỗi\t毎日\tまいにち\tmỗi ngày
週\tchu\ttuần\t毎週\tまいしゅう\tmỗi tuần
映\tánh\tchiếu, phản chiếu\t映画\tえいが\tphim
画\thoạ\ttranh, phim\t映画\tえいが\tphim
図\tđồ\tbản vẽ, sơ đồ\t地図\tちず\tbản đồ
館\tquán\ttoà nhà lớn\t図書館\tとしょかん\tthư viện
公\tcông\tcông cộng\t公園\tこうえん\tcông viên
園\tviên\tvườn\t公園\tこうえん\tcông viên
夫\tphu\tchồng\t夫\tおっと\tchồng tôi
妻\tthê\tvợ\t妻\tつま\tvợ tôi
特\tđặc\tđặc biệt\t特別\tとくべつ\tđặc biệt
思\ttư\tnghĩ\t思う\tおもう\tnghĩ
料\tliệu\tphí, nguyên liệu\t料理\tりょうり\tmón ăn, nấu ăn
理\tlí\tlý lẽ, xử lý\t料理\tりょうり\tmón ăn, nấu ăn
有\thữu\tcó\t有名\tゆうめい\tnổi tiếng
洋\tdương\tphương Tây, đại dương\t洋服\tようふく\tquần áo kiểu Tây
服\tphục\tquần áo\t服\tふく\tquần áo
衣\ty\táo, quần áo\t衣服\tいふく\tquần áo
短\tđoản\tngắn\t短い\tみじかい\tngắn
毛\tmao\tlông, len\t毛\tけ\tlông
糸\tti\tchỉ, sợi\t糸\tいと\tsợi chỉ
玉\tngọc\tviên ngọc, bóng\t玉\tたま\tviên, bóng
光\tquang\tánh sáng\t光\tひかり\tánh sáng
駅\tdịch\tnhà ga\t駅\tえき\tnhà ga
鉄\tsắt\tsắt\t鉄道\tてつどう\tđường sắt
乗\tthừa\tlên xe\t乗る\tのる\tlên xe
降\tgiáng\txuống xe, rơi\t降りる\tおりる\txuống xe
開\tkhai\tmở\t開く\tあく\tmở
閉\tbế\tđóng\t閉まる\tしまる\tđóng
発\tphát\txuất phát\t出発\tしゅっぱつ\txuất phát
着\ttrứ\tđến, mặc\t着く\tつく\tđến nơi
交\tgiao\tgiao nhau\t交通\tこうつう\tgiao thông
通\tthông\tđi qua, thông\t通る\tとおる\tđi qua
台\tđài\tbệ, máy\t台\tだい\tcái, chiếc
止\tchỉ\tdừng\t止まる\tとまる\tdừng lại
色\tsắc\tmàu sắc\t色\tいろ\tmàu sắc
赤\txích\tmàu đỏ\t赤い\tあかい\tđỏ
黄\thoàng\tmàu vàng\t黄色\tきいろ\tmàu vàng
青\tthanh\tmàu xanh\t青い\tあおい\txanh
病\tbệnh\tbệnh\t病気\tびょうき\tbệnh
院\tviện\tviện\t病院\tびょういん\tbệnh viện
医\ty\ty học, bác sĩ\t医者\tいしゃ\tbác sĩ
科\tkhoa\tkhoa, ngành\t内科\tないか\tkhoa nội
薬\tdược\tthuốc\t薬\tくすり\tthuốc
待\tđãi\tchờ\t待つ\tまつ\tchờ
合\thợp\thợp lại\t合う\tあう\thợp, gặp
計\tkế\ttính toán\t合計\tごうけい\ttổng cộng
研\tnghiên\tmài, nghiên cứu\t研究\tけんきゅう\tnghiên cứu
究\tcứu\tnghiên cứu\t研究\tけんきゅう\tnghiên cứu
語\tngữ\tngôn ngữ\t日本語\tにほんご\ttiếng Nhật
文\tvăn\tvăn, câu\t作文\tさくぶん\tbài văn
英\tanh\tAnh, ưu tú\t英語\tえいご\ttiếng Anh
化\thoá\tbiến đổi\t文化\tぶんか\tvăn hóa
数\tsố\tsố lượng\t数学\tすうがく\ttoán học
心\ttâm\ttrái tim, tâm trí\t心\tこころ\ttrái tim, tâm trí
若\tnhược\ttrẻ\t若い\tわかい\ttrẻ
集\ttập\ttập hợp\t集まる\tあつまる\ttụ tập
知\ttri\tbiết\t知る\tしる\tbiết
酒\ttửu\trượu\tお酒\tおさけ\trượu
歌\tca\tbài hát\t歌\tうた\tbài hát
声\tthanh\tgiọng nói\t声\tこえ\tgiọng nói
楽\tlạc\tdễ chịu, vui\t楽しい\tたのしい\tvui
味\tvị\tvị, hương vị\t味\tあじ\tvị
油\tdầu\tdầu ăn, dầu\t油\tあぶら\tdầu
太\tthái\tto, béo\t太い\tふとい\tto, dày
細\ttế\tmảnh, nhỏ\t細い\tほそい\tmảnh
皿\tmãnh\tđĩa\t皿\tさら\tđĩa
飯\tphạn\tcơm\tご飯\tごはん\tcơm
麦\tmạch\tlúa mì\t麦\tむぎ\tlúa mì
春\txuân\tmùa xuân\t春\tはる\tmùa xuân
夏\thạ\tmùa hè\t夏\tなつ\tmùa hè
秋\tthu\tmùa thu\t秋\tあき\tmùa thu
冬\tđông\tmùa đông\t冬\tふゆ\tmùa đông
空\tkhông\tbầu trời, rỗng\t空\tそら\tbầu trời
星\ttinh\tngôi sao\t星\tほし\tngôi sao
雲\tvân\tmây\t雲\tくも\tmây
去\tkhứ\trời đi, quá khứ\t去年\tきょねん\tnăm ngoái
天\tthiên\ttrời\t天気\tてんき\tthời tiết
晴\ttình\ttrời nắng\t晴れる\tはれる\ttrời nắng
雪\ttuyết\ttuyết\t雪\tゆき\ttuyết
風\tphong\tgió\t風\tかぜ\tgió
強\tcường\tmạnh\t強い\tつよい\tmạnh
弱\tnhược\tyếu\t弱い\tよわい\tyếu
暑\tthử\tnóng bức\t暑い\tあつい\tnóng
寒\thàn\tlạnh\t寒い\tさむい\tlạnh
旅\tlữ\tdu lịch\t旅行\tりょこう\tdu lịch
持\ttrì\tcầm, mang\t持つ\tもつ\tcầm, mang
世\tthế\tthế giới, đời\t世界\tせかい\tthế giới
界\tgiới\tranh giới, thế giới\t世界\tせかい\tthế giới
写\ttả\tchụp, sao chép\t写真\tしゃしん\tảnh
真\tchân\tthật\t写真\tしゃしん\tảnh
船\tthuyền\tthuyền\t船\tふね\tthuyền
勉\tmiễn\tcố gắng học\t勉強\tべんきょう\thọc tập
漢\thán\tHán\t漢字\tかんじ\tchữ Hán
宿\ttúc\tnhà trọ, bài tập\t宿題\tしゅくだい\tbài tập về nhà
題\tđề\tđề bài, chủ đề\t宿題\tしゅくだい\tbài tập về nhà
質\tchất\tchất lượng, câu hỏi\t質問\tしつもん\tcâu hỏi
問\tvấn\thỏi\t質問\tしつもん\tcâu hỏi
教\tgiáo\tdạy\t教える\tおしえる\tdạy
室\tthất\tphòng\t教室\tきょうしつ\tphòng học
試\tthí\tthử, thi\t試験\tしけん\tkỳ thi
験\tnghiệm\tkiểm nghiệm\t試験\tしけん\tkỳ thi
答\tđáp\ttrả lời\t答える\tこたえる\ttrả lời
考\tkhảo\tsuy nghĩ\t考える\tかんがえる\tsuy nghĩ
正\tchính\tđúng\t正しい\tただしい\tđúng
丸\thoàn\ttròn\t丸い\tまるい\ttròn
不\tbất\tkhông\t不便\tふべん\tbất tiện
同\tđồng\tgiống nhau\t同じ\tおなじ\tgiống nhau
政\tchính\tchính trị\t政治\tせいじ\tchính trị
治\ttrị\tcai trị, chữa trị\t政治\tせいじ\tchính trị
経\tkinh\ttrải qua, kinh tế\t経済\tけいざい\tkinh tế
済\ttế\tcứu giúp, hoàn tất\t経済\tけいざい\tkinh tế
歴\tlịch\tlịch sử\t歴史\tれきし\tlịch sử
史\tsử\tlịch sử\t歴史\tれきし\tlịch sử
国\tquốc\tđất nước\t国\tくに\tđất nước
王\tvương\tvua\t王\tおう\tvua
運\tvận\tvận chuyển, vận động\t運動\tうんどう\tvận động
動\tđộng\tchuyển động\t運動\tうんどう\tvận động
練\tluyện\tluyện tập\t練習\tれんしゅう\tluyện tập
習\ttập\thọc, luyện\t練習\tれんしゅう\tluyện tập
走\ttẩu\tchạy\t走る\tはしる\tchạy
歩\tbộ\tđi bộ\t歩く\tあるく\tđi bộ
泳\tvịnh\tbơi\t泳ぐ\tおよぐ\tbơi
才\ttài\ttài năng, tuổi\t天才\tてんさい\tthiên tài
自\ttự\ttự mình\t自分\tじぶん\tbản thân
然\tnhiên\ttự nhiên\t自然\tしぜん\ttự nhiên
草\tthảo\tcỏ\t草\tくさ\tcỏ
原\tnguyên\tđồng bằng, gốc\t草原\tそうげん\tthảo nguyên
湖\thồ\thồ nước\t湖\tみずうみ\thồ nước
谷\tcốc\tthung lũng\t谷\tたに\tthung lũng
海\thải\tbiển\t海\tうみ\tbiển
辺\tbiên\tvùng, bên cạnh\t海辺\tうみべ\tbờ biển
里\tlí\tlàng quê\t里\tさと\tlàng quê
野\tdã\tđồng ruộng, hoang dã\t野原\tのはら\tđồng cỏ
奥\táo\tphía sâu\t奥\tおく\tphía sâu
池\ttrì\tao, hồ nhỏ\t池\tいけ\tao, hồ
虫\ttrùng\tcôn trùng\t虫\tむし\tcôn trùng
羽\tvũ\tlông, cánh\t羽\tはね\tcánh, lông
鳴\tminh\tkêu, hót\t鳴く\tなく\tkêu, hót
馬\tmã\tngựa\t馬\tうま\tngựa
""".strip()


def load_kanji_api_cache() -> dict:
    if KANJI_API_CACHE.exists():
        return json.loads(KANJI_API_CACHE.read_text(encoding="utf-8"))
    return {}


def save_kanji_api_cache(cache: dict) -> None:
    KANJI_API_CACHE.parent.mkdir(parents=True, exist_ok=True)
    KANJI_API_CACHE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def fetch_kanji_api(character: str, cache: dict) -> dict:
    if not ENRICH_KANJI_API:
        return {}
    if character in cache:
        return cache[character]

    response = requests.get(
        f"https://kanjiapi.dev/v1/kanji/{character}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()
    cache[character] = response.json()
    save_kanji_api_cache(cache)
    return cache[character]


def join_readings(values: list[str] | None) -> str | None:
    if not values:
        return None
    return "・".join(values)


def parse_kanji_rows() -> dict:
    rows = {}
    for line in KANJI_ROWS.splitlines():
        character, han_viet, meaning_vi, word, reading, word_meaning_vi = line.split("\t")
        rows[character] = {
            "han_viet": han_viet,
            "meaning_vi": meaning_vi,
            "word": word,
            "reading": reading,
            "word_meaning_vi": word_meaning_vi,
        }
    return rows


def build_word_example(word: str, reading: str, meaning_vi: str) -> tuple[str, str, str]:
    return (
        f"この文で「{word}」を使います。",
        f"このぶんで「{reading}」をつかいます。",
        f"Câu này dùng từ '{word}' ({meaning_vi}).",
    )


def build_data() -> dict:
    kanji_cache = load_kanji_api_cache()
    kanji_rows = parse_kanji_rows()
    topics = []
    characters = []
    words = []
    character_id = 1
    word_id = 1

    for topic_id, chapter, lesson, name, name_reading, name_vi, page_start, character_values in TOPICS:
        topics.append(
            {
                "id": topic_id,
                "jlpt_level_id": 2,
                "name": name,
                "name_reading": name_reading,
                "name_vi": name_vi,
                "description": (
                    f"Kanji Master N4 - Chương {chapter}, bài {lesson}: "
                    f"{name} ({name_vi})."
                ),
                "source_book": "Kanji Master N4",
                "source_week": chapter,
                "source_week_title": f"第{chapter}章",
                "source_week_title_vi": f"Chương {chapter}",
                "source_day": lesson,
                "source_page_start": page_start,
                "source_url": "plan/kanji/kanji-master-n4-アークアカデミー-study-guide.pdf",
                "display_order": topic_id,
                "is_published": True,
                "version": 1,
            }
        )

        for display_order, character_value in enumerate(character_values, start=1):
            row = kanji_rows[character_value]
            api_data = fetch_kanji_api(character_value, kanji_cache)
            onyomi = join_readings(api_data.get("on_readings")) or "なし"
            kunyomi = join_readings(api_data.get("kun_readings")) or "なし"
            characters.append(
                {
                    "id": character_id,
                    "kanji_topic_id": topic_id,
                    "character_value": character_value,
                    "han_viet": row["han_viet"],
                    "onyomi": onyomi,
                    "kunyomi": kunyomi,
                    "meaning_vi": row["meaning_vi"],
                    "stroke_count": api_data.get("stroke_count"),
                    "mnemonic_vi": (
                        f"Ghi nhớ chữ {character_value} theo nghĩa '{row['meaning_vi']}' "
                        f"qua từ {row['word']}."
                    ),
                    "display_order": display_order,
                    "is_published": True,
                    "version": 1,
                }
            )

            example_sentence, example_reading, example_meaning_vi = build_word_example(
                row["word"],
                row["reading"],
                row["word_meaning_vi"],
            )
            words.append(
                {
                    "id": word_id,
                    "kanji_character_id": character_id,
                    "word": row["word"],
                    "reading": row["reading"],
                    "meaning_vi": row["word_meaning_vi"],
                    "example_sentence": example_sentence,
                    "example_reading": example_reading,
                    "example_meaning_vi": example_meaning_vi,
                    "display_order": 1,
                    "is_published": True,
                    "version": 1,
                }
            )
            word_id += 1
            character_id += 1

    return {
        "metadata": {
            "name": "JLPT N4 kanji import data by Kanji Master N4",
            "status": "ready_for_review_database_import",
            "jlpt_level_code": "N4",
            "jlpt_level_id_assumption": 2,
            "source_file": "plan/kanji/kanji-master-n4-アークアカデミー-study-guide.pdf",
            "source_note": (
                "Topic/chapter structure and the 209 index kanji follow the scanned "
                "Kanji Master N4 table of contents. Vietnamese meanings and example "
                "sentences were prepared as import-ready learning data."
            ),
            "enrichment_source": (
                "https://kanjiapi.dev/ for stroke counts and on/kun readings"
                if ENRICH_KANJI_API
                else None
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "import_order_when_completed": [
                "kanji_topics",
                "kanji_characters",
                "kanji_words",
            ],
            "notes": [
                "kanji_topics.name is Japanese-first; kanji_topics.name_vi is the Vietnamese subtitle.",
                "No note field is generated.",
                "Each kanji has one representative learning word and generated example_* fields.",
            ],
        },
        "kanji_topics": topics,
        "kanji_characters": characters,
        "kanji_words": words,
    }


def validate(data: dict) -> None:
    if len(data["kanji_topics"]) != 27:
        raise ValueError(f"Expected 27 topics, got {len(data['kanji_topics'])}")
    if len(data["kanji_characters"]) != 209:
        raise ValueError(
            f"Expected 209 kanji characters, got {len(data['kanji_characters'])}"
        )

    topic_ids = {topic["id"] for topic in data["kanji_topics"]}
    character_ids = {char["id"] for char in data["kanji_characters"]}
    character_values = [char["character_value"] for char in data["kanji_characters"]]
    if len(character_values) != len(set(character_values)):
        raise ValueError("Duplicate kanji character detected")

    for group in ("kanji_topics", "kanji_characters", "kanji_words"):
        for item in data[group]:
            if "note" in item:
                raise ValueError(f"Unexpected note field in {group}: {item}")

    for topic in data["kanji_topics"]:
        for key in ("id", "jlpt_level_id", "name", "name_vi", "display_order"):
            if topic.get(key) in (None, ""):
                raise ValueError(f"Missing {key}: {topic}")

    for char in data["kanji_characters"]:
        if char["kanji_topic_id"] not in topic_ids:
            raise ValueError(f"Invalid kanji_topic_id: {char}")
        for key in (
            "character_value",
            "han_viet",
            "onyomi",
            "kunyomi",
            "meaning_vi",
            "stroke_count",
            "mnemonic_vi",
        ):
            if char.get(key) in (None, ""):
                raise ValueError(f"Missing {key}: {char}")

    for word in data["kanji_words"]:
        if word["kanji_character_id"] not in character_ids:
            raise ValueError(f"Invalid kanji_character_id: {word}")
        for key in (
            "word",
            "reading",
            "meaning_vi",
            "example_sentence",
            "example_reading",
            "example_meaning_vi",
        ):
            if word.get(key) in (None, ""):
                raise ValueError(f"Missing {key}: {word}")


def main() -> None:
    data = build_data()
    validate(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")
    print(f"topics={len(data['kanji_topics'])}")
    print(f"kanji_characters={len(data['kanji_characters'])}")
    print(f"kanji_words={len(data['kanji_words'])}")


if __name__ == "__main__":
    main()
