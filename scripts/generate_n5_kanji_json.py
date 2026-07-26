import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests


OUTPUT = Path("database/import/jlpt_n5_kanji_by_topic_db_import.json")
KANJI_API_CACHE = Path("tmp/cache/kanjiapi_n5.json")
ENRICH_KANJI_API = os.environ.get("ENRICH_KANJI_API", "1") != "0"


TOPICS = [
    (1, "すうじ", "すうじ", "Số đếm", 11, "一二三四五六七八九十百千万円"),
    (2, "カレンダー", "カレンダー", "Lịch và ngày tháng", 23, "月火水木金土日年"),
    (3, "人", "ひと", "Con người và cơ thể", 31, "人口目耳手足力"),
    (4, "しぜん - 1", "しぜん いち", "Tự nhiên 1", 39, "山川田石花竹雨"),
    (5, "ばしょ", "ばしょ", "Vị trí và nơi chốn", 47, "上下左右外内中"),
    (6, "学校 - 1", "がっこう いち", "Trường học 1", 57, "学校先生名字本体"),
    (7, "学校 - 2", "がっこう に", "Trường học 2", 65, "大小高友入出門"),
    (8, "かぞく", "かぞく", "Gia đình", 73, "父母子男女犬鳥"),
    (9, "どうし - 1", "どうし いち", "Động từ 1", 81, "立休見聞行来帰"),
    (10, "たべもの", "たべもの", "Đồ ăn", 89, "米茶牛肉魚貝好物"),
    (11, "しぜん - 2", "しぜん に", "Tự nhiên 2", 99, "林森畑岩音明暗"),
    (12, "どうし - 2", "どうし に", "Động từ 2", 107, "言書読話食飲買"),
    (13, "町", "まち", "Thị trấn và phương hướng", 115, "町寺電車東西南北"),
    (14, "時間", "じかん", "Thời gian", 123, "時間半分今何夕方"),
    (15, "けいようし", "けいようし", "Tính từ và trạng thái", 131, "新古長安多少元気"),
]


KANJI_DATA = {
    "一": ("nhất", "một", [("一つ", "ひとつ", "một cái"), ("一人", "ひとり", "một người")]),
    "二": ("nhị", "hai", [("二つ", "ふたつ", "hai cái"), ("二人", "ふたり", "hai người")]),
    "三": ("tam", "ba", [("三つ", "みっつ", "ba cái"), ("三日", "みっか", "ngày mùng ba, ba ngày")]),
    "四": ("tứ", "bốn", [("四つ", "よっつ", "bốn cái"), ("四日", "よっか", "ngày mùng bốn, bốn ngày")]),
    "五": ("ngũ", "năm", [("五つ", "いつつ", "năm cái"), ("五日", "いつか", "ngày mùng năm, năm ngày")]),
    "六": ("lục", "sáu", [("六つ", "むっつ", "sáu cái"), ("六日", "むいか", "ngày mùng sáu, sáu ngày")]),
    "七": ("thất", "bảy", [("七つ", "ななつ", "bảy cái"), ("七日", "なのか", "ngày mùng bảy, bảy ngày")]),
    "八": ("bát", "tám", [("八つ", "やっつ", "tám cái"), ("八日", "ようか", "ngày mùng tám, tám ngày")]),
    "九": ("cửu", "chín", [("九つ", "ここのつ", "chín cái"), ("九日", "ここのか", "ngày mùng chín, chín ngày")]),
    "十": ("thập", "mười", [("十", "とお", "mười"), ("十日", "とおか", "ngày mùng mười, mười ngày")]),
    "百": ("bách", "trăm", [("百", "ひゃく", "một trăm"), ("三百", "さんびゃく", "ba trăm")]),
    "千": ("thiên", "nghìn", [("千", "せん", "một nghìn"), ("千円", "せんえん", "một nghìn yên")]),
    "万": ("vạn", "mười nghìn", [("一万", "いちまん", "mười nghìn"), ("万年筆", "まんねんひつ", "bút máy")]),
    "円": ("viên", "yên, hình tròn", [("円", "えん", "yên"), ("百円", "ひゃくえん", "một trăm yên")]),
    "月": ("nguyệt", "mặt trăng, tháng", [("月", "つき", "mặt trăng"), ("月曜日", "げつようび", "thứ Hai")]),
    "火": ("hỏa", "lửa", [("火", "ひ", "lửa"), ("火曜日", "かようび", "thứ Ba")]),
    "水": ("thủy", "nước", [("水", "みず", "nước"), ("水曜日", "すいようび", "thứ Tư")]),
    "木": ("mộc", "cây, gỗ", [("木", "き", "cây"), ("木曜日", "もくようび", "thứ Năm")]),
    "金": ("kim", "vàng, tiền", [("お金", "おかね", "tiền"), ("金曜日", "きんようび", "thứ Sáu")]),
    "土": ("thổ", "đất", [("土", "つち", "đất"), ("土曜日", "どようび", "thứ Bảy")]),
    "日": ("nhật", "mặt trời, ngày", [("日", "ひ", "ngày, mặt trời"), ("日曜日", "にちようび", "Chủ nhật")]),
    "年": ("niên", "năm", [("年", "とし", "năm, tuổi"), ("今年", "ことし", "năm nay")]),
    "人": ("nhân", "người", [("人", "ひと", "người"), ("日本人", "にほんじん", "người Nhật")]),
    "口": ("khẩu", "miệng, cửa", [("口", "くち", "miệng"), ("入口", "いりぐち", "lối vào")]),
    "目": ("mục", "mắt", [("目", "め", "mắt"), ("一目", "ひとめ", "một cái nhìn")]),
    "耳": ("nhĩ", "tai", [("耳", "みみ", "tai"), ("耳元", "みみもと", "bên tai")]),
    "手": ("thủ", "tay", [("手", "て", "tay"), ("上手", "じょうず", "giỏi, khéo")]),
    "足": ("túc", "chân, đủ", [("足", "あし", "chân"), ("足りる", "たりる", "đủ")]),
    "力": ("lực", "sức mạnh", [("力", "ちから", "sức mạnh"), ("力持ち", "ちからもち", "người khỏe")]),
    "山": ("sơn", "núi", [("山", "やま", "núi"), ("富士山", "ふじさん", "núi Phú Sĩ")]),
    "川": ("xuyên", "sông", [("川", "かわ", "sông"), ("小川", "おがわ", "suối nhỏ")]),
    "田": ("điền", "ruộng", [("田んぼ", "たんぼ", "ruộng lúa"), ("山田", "やまだ", "Yamada")]),
    "石": ("thạch", "đá", [("石", "いし", "đá"), ("宝石", "ほうせき", "đá quý")]),
    "花": ("hoa", "hoa", [("花", "はな", "hoa"), ("花見", "はなみ", "ngắm hoa")]),
    "竹": ("trúc", "tre", [("竹", "たけ", "tre"), ("竹林", "ちくりん", "rừng tre")]),
    "雨": ("vũ", "mưa", [("雨", "あめ", "mưa"), ("大雨", "おおあめ", "mưa lớn")]),
    "上": ("thượng", "trên", [("上", "うえ", "trên"), ("上手", "じょうず", "giỏi, khéo")]),
    "下": ("hạ", "dưới", [("下", "した", "dưới"), ("下手", "へた", "kém, vụng")]),
    "左": ("tả", "trái", [("左", "ひだり", "bên trái"), ("左手", "ひだりて", "tay trái")]),
    "右": ("hữu", "phải", [("右", "みぎ", "bên phải"), ("右手", "みぎて", "tay phải")]),
    "外": ("ngoại", "ngoài", [("外", "そと", "bên ngoài"), ("外国", "がいこく", "nước ngoài")]),
    "内": ("nội", "trong", [("内", "うち", "bên trong, nhà mình"), ("案内", "あんない", "hướng dẫn")]),
    "中": ("trung", "giữa, trong", [("中", "なか", "bên trong"), ("一日中", "いちにちじゅう", "suốt cả ngày")]),
    "学": ("học", "học", [("学生", "がくせい", "học sinh, sinh viên"), ("学校", "がっこう", "trường học")]),
    "校": ("hiệu", "trường học", [("学校", "がっこう", "trường học"), ("校長", "こうちょう", "hiệu trưởng")]),
    "先": ("tiên", "trước", [("先生", "せんせい", "giáo viên"), ("先月", "せんげつ", "tháng trước")]),
    "生": ("sinh", "sinh, sống", [("学生", "がくせい", "học sinh, sinh viên"), ("生まれる", "うまれる", "được sinh ra")]),
    "名": ("danh", "tên", [("名前", "なまえ", "tên"), ("有名", "ゆうめい", "nổi tiếng")]),
    "字": ("tự", "chữ", [("漢字", "かんじ", "chữ Hán"), ("文字", "もじ", "chữ, ký tự")]),
    "本": ("bản", "sách, gốc", [("本", "ほん", "sách"), ("日本", "にほん", "Nhật Bản")]),
    "体": ("thể", "cơ thể", [("体", "からだ", "cơ thể"), ("体育", "たいいく", "thể dục")]),
    "大": ("đại", "to, lớn", [("大きい", "おおきい", "to, lớn"), ("大学", "だいがく", "đại học")]),
    "小": ("tiểu", "nhỏ", [("小さい", "ちいさい", "nhỏ"), ("小学校", "しょうがっこう", "trường tiểu học")]),
    "高": ("cao", "cao, đắt", [("高い", "たかい", "cao, đắt"), ("高校", "こうこう", "trường cấp ba")]),
    "友": ("hữu", "bạn", [("友だち", "ともだち", "bạn bè"), ("友人", "ゆうじん", "bạn bè")]),
    "入": ("nhập", "vào", [("入る", "はいる", "đi vào"), ("入口", "いりぐち", "lối vào")]),
    "出": ("xuất", "ra", [("出る", "でる", "đi ra"), ("出口", "でぐち", "lối ra")]),
    "門": ("môn", "cổng", [("門", "もん", "cổng"), ("専門", "せんもん", "chuyên môn")]),
    "父": ("phụ", "cha", [("父", "ちち", "cha tôi"), ("お父さん", "おとうさん", "bố")]),
    "母": ("mẫu", "mẹ", [("母", "はは", "mẹ tôi"), ("お母さん", "おかあさん", "mẹ")]),
    "子": ("tử", "con", [("子ども", "こども", "trẻ em"), ("女の子", "おんなのこ", "bé gái")]),
    "男": ("nam", "nam giới", [("男", "おとこ", "nam, đàn ông"), ("男の子", "おとこのこ", "bé trai")]),
    "女": ("nữ", "nữ giới", [("女", "おんな", "nữ, phụ nữ"), ("女の人", "おんなのひと", "người phụ nữ")]),
    "犬": ("khuyển", "chó", [("犬", "いぬ", "chó"), ("子犬", "こいぬ", "chó con")]),
    "鳥": ("điểu", "chim", [("鳥", "とり", "chim"), ("小鳥", "ことり", "chim nhỏ")]),
    "立": ("lập", "đứng", [("立つ", "たつ", "đứng"), ("立てる", "たてる", "dựng lên")]),
    "休": ("hưu", "nghỉ", [("休む", "やすむ", "nghỉ"), ("休日", "きゅうじつ", "ngày nghỉ")]),
    "見": ("kiến", "nhìn", [("見る", "みる", "nhìn, xem"), ("見せる", "みせる", "cho xem")]),
    "聞": ("văn", "nghe, hỏi", [("聞く", "きく", "nghe, hỏi"), ("新聞", "しんぶん", "báo")]),
    "行": ("hành", "đi", [("行く", "いく", "đi"), ("銀行", "ぎんこう", "ngân hàng")]),
    "来": ("lai", "đến", [("来る", "くる", "đến"), ("来年", "らいねん", "năm sau")]),
    "帰": ("quy", "trở về", [("帰る", "かえる", "trở về"), ("帰国", "きこく", "về nước")]),
    "米": ("mễ", "gạo", [("米", "こめ", "gạo"), ("米国", "べいこく", "Hoa Kỳ")]),
    "茶": ("trà", "trà", [("お茶", "おちゃ", "trà"), ("茶色", "ちゃいろ", "màu nâu")]),
    "牛": ("ngưu", "bò", [("牛", "うし", "bò"), ("牛肉", "ぎゅうにく", "thịt bò")]),
    "肉": ("nhục", "thịt", [("肉", "にく", "thịt"), ("牛肉", "ぎゅうにく", "thịt bò")]),
    "魚": ("ngư", "cá", [("魚", "さかな", "cá"), ("金魚", "きんぎょ", "cá vàng")]),
    "貝": ("bối", "sò, vỏ sò", [("貝", "かい", "sò, vỏ sò"), ("貝殻", "かいがら", "vỏ sò")]),
    "好": ("hảo", "thích, tốt", [("好き", "すき", "thích"), ("大好き", "だいすき", "rất thích")]),
    "物": ("vật", "đồ vật", [("物", "もの", "đồ vật"), ("食べ物", "たべもの", "đồ ăn")]),
    "林": ("lâm", "rừng thưa", [("林", "はやし", "rừng thưa"), ("山林", "さんりん", "rừng núi")]),
    "森": ("sâm", "rừng rậm", [("森", "もり", "rừng"), ("森林", "しんりん", "rừng rậm")]),
    "畑": ("điền Nhật", "ruộng, vườn", [("畑", "はたけ", "ruộng, vườn"), ("花畑", "はなばたけ", "vườn hoa")]),
    "岩": ("nham", "đá lớn", [("岩", "いわ", "đá lớn"), ("岩山", "いわやま", "núi đá")]),
    "音": ("âm", "âm thanh", [("音", "おと", "âm thanh"), ("音楽", "おんがく", "âm nhạc")]),
    "明": ("minh", "sáng", [("明るい", "あかるい", "sáng sủa"), ("明日", "あした", "ngày mai")]),
    "暗": ("ám", "tối", [("暗い", "くらい", "tối"), ("暗記", "あんき", "học thuộc lòng")]),
    "言": ("ngôn", "nói", [("言う", "いう", "nói"), ("言葉", "ことば", "từ ngữ")]),
    "書": ("thư", "viết, sách", [("書く", "かく", "viết"), ("図書館", "としょかん", "thư viện")]),
    "読": ("độc", "đọc", [("読む", "よむ", "đọc"), ("読書", "どくしょ", "việc đọc sách")]),
    "話": ("thoại", "nói chuyện", [("話す", "はなす", "nói chuyện"), ("電話", "でんわ", "điện thoại")]),
    "食": ("thực", "ăn", [("食べる", "たべる", "ăn"), ("食べ物", "たべもの", "đồ ăn")]),
    "飲": ("ẩm", "uống", [("飲む", "のむ", "uống"), ("飲み物", "のみもの", "đồ uống")]),
    "買": ("mãi", "mua", [("買う", "かう", "mua"), ("買い物", "かいもの", "mua sắm")]),
    "町": ("đinh", "thị trấn", [("町", "まち", "thị trấn"), ("町内", "ちょうない", "trong khu phố")]),
    "寺": ("tự", "chùa", [("寺", "てら", "chùa"), ("お寺", "おてら", "ngôi chùa")]),
    "電": ("điện", "điện", [("電気", "でんき", "điện"), ("電話", "でんわ", "điện thoại")]),
    "車": ("xa", "xe", [("車", "くるま", "xe ô tô"), ("電車", "でんしゃ", "tàu điện")]),
    "東": ("đông", "phía đông", [("東", "ひがし", "phía đông"), ("東京", "とうきょう", "Tokyo")]),
    "西": ("tây", "phía tây", [("西", "にし", "phía tây"), ("関西", "かんさい", "vùng Kansai")]),
    "南": ("nam", "phía nam", [("南", "みなみ", "phía nam"), ("南口", "みなみぐち", "cửa nam")]),
    "北": ("bắc", "phía bắc", [("北", "きた", "phía bắc"), ("北口", "きたぐち", "cửa bắc")]),
    "時": ("thời", "thời gian, giờ", [("時", "とき", "thời điểm"), ("時間", "じかん", "thời gian")]),
    "間": ("gian", "khoảng, giữa", [("間", "あいだ", "khoảng giữa"), ("時間", "じかん", "thời gian")]),
    "半": ("bán", "nửa", [("半分", "はんぶん", "một nửa"), ("半年", "はんとし", "nửa năm")]),
    "分": ("phân", "phút, phần", [("分かる", "わかる", "hiểu"), ("自分", "じぶん", "bản thân")]),
    "今": ("kim", "bây giờ", [("今", "いま", "bây giờ"), ("今日", "きょう", "hôm nay")]),
    "何": ("hà", "cái gì", [("何", "なに", "cái gì"), ("何人", "なんにん", "mấy người")]),
    "夕": ("tịch", "chiều tối", [("夕方", "ゆうがた", "chiều tối"), ("夕日", "ゆうひ", "nắng chiều")]),
    "方": ("phương", "phương hướng, cách", [("方", "かた", "người, cách"), ("夕方", "ゆうがた", "chiều tối")]),
    "新": ("tân", "mới", [("新しい", "あたらしい", "mới"), ("新聞", "しんぶん", "báo")]),
    "古": ("cổ", "cũ", [("古い", "ふるい", "cũ"), ("中古", "ちゅうこ", "đồ cũ")]),
    "長": ("trường", "dài, trưởng", [("長い", "ながい", "dài"), ("校長", "こうちょう", "hiệu trưởng")]),
    "安": ("an", "rẻ, yên ổn", [("安い", "やすい", "rẻ"), ("安心", "あんしん", "yên tâm")]),
    "多": ("đa", "nhiều", [("多い", "おおい", "nhiều"), ("多分", "たぶん", "có lẽ")]),
    "少": ("thiếu", "ít", [("少ない", "すくない", "ít"), ("少し", "すこし", "một chút")]),
    "元": ("nguyên", "gốc, khỏe khoắn", [("元気", "げんき", "khỏe mạnh"), ("元日", "がんじつ", "ngày đầu năm")]),
    "気": ("khí", "khí, tinh thần", [("元気", "げんき", "khỏe mạnh"), ("天気", "てんき", "thời tiết")]),
}


READING_FALLBACKS = {
    "校": {"kunyomi": "なし"},
    "茶": {"kunyomi": "なし"},
    "畑": {"onyomi": "なし"},
    "電": {"kunyomi": "なし"},
}


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
    return cache[character]


def join_readings(values: list[str] | None) -> str | None:
    if not values:
        return None
    return "・".join(values)


def build_word_example(word: str, reading: str, meaning_vi: str) -> tuple[str, str, str]:
    return (
        f"この言葉は「{word}」です。",
        f"このことばは「{reading}」です。",
        f"Từ này là '{word}' ({meaning_vi}).",
    )


def build_data() -> dict:
    kanji_cache = load_kanji_api_cache()
    topics = []
    characters = []
    words = []
    character_id = 1
    word_id = 1

    for topic_id, name, name_reading, name_vi, page_start, character_values in TOPICS:
        topics.append(
            {
                "id": topic_id,
                "jlpt_level_id": 1,
                "name": name,
                "name_reading": name_reading,
                "name_vi": name_vi,
                "description": (
                    f"Kanji Master N5 - Chương {topic_id}: {name} ({name_vi})."
                ),
                "source_book": "Kanji Master N5",
                "source_week": topic_id,
                "source_week_title": name,
                "source_week_title_vi": name_vi,
                "source_day": None,
                "source_page_start": page_start,
                "source_url": "plan/kanji/N5 - Kanji master Bản nét.pdf",
                "display_order": topic_id,
                "is_published": True,
                "version": 1,
            }
        )

        for display_order, character_value in enumerate(character_values, start=1):
            han_viet, meaning_vi, word_rows = KANJI_DATA[character_value]
            api_data = fetch_kanji_api(character_value, kanji_cache)
            fallback = READING_FALLBACKS.get(character_value, {})
            onyomi = join_readings(api_data.get("on_readings")) or fallback.get("onyomi")
            kunyomi = join_readings(api_data.get("kun_readings")) or fallback.get("kunyomi")
            characters.append(
                {
                    "id": character_id,
                    "kanji_topic_id": topic_id,
                    "character_value": character_value,
                    "han_viet": han_viet,
                    "onyomi": onyomi,
                    "kunyomi": kunyomi,
                    "meaning_vi": meaning_vi,
                    "stroke_count": api_data.get("stroke_count"),
                    "mnemonic_vi": (
                        f"Ghi nhớ chữ {character_value} theo nghĩa '{meaning_vi}' "
                        f"qua các từ như {word_rows[0][0]}."
                    ),
                    "display_order": display_order,
                    "is_published": True,
                    "version": 1,
                }
            )

            for word_display_order, (word, reading, word_meaning_vi) in enumerate(
                word_rows,
                start=1,
            ):
                example_sentence, example_reading, example_meaning_vi = build_word_example(
                    word,
                    reading,
                    word_meaning_vi,
                )
                words.append(
                    {
                        "id": word_id,
                        "kanji_character_id": character_id,
                        "word": word,
                        "reading": reading,
                        "meaning_vi": word_meaning_vi,
                        "example_sentence": example_sentence,
                        "example_reading": example_reading,
                        "example_meaning_vi": example_meaning_vi,
                        "display_order": word_display_order,
                        "is_published": True,
                        "version": 1,
                    }
                )
                word_id += 1

            character_id += 1

    if ENRICH_KANJI_API:
        save_kanji_api_cache(kanji_cache)

    return {
        "metadata": {
            "name": "JLPT N5 kanji import data by Kanji Master N5",
            "status": "ready_for_review_database_import",
            "jlpt_level_code": "N5",
            "jlpt_level_id_assumption": 1,
            "source_file": "plan/kanji/N5 - Kanji master Bản nét.pdf",
            "source_note": (
                "Topic/chapter structure and the 118 index kanji follow the scanned "
                "Kanji Master N5 textbook. The PDF has no text layer, so vocabulary "
                "and Vietnamese examples were prepared as learning data."
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
                "Each kanji has at least two learning words and generated example_* fields.",
            ],
        },
        "kanji_topics": topics,
        "kanji_characters": characters,
        "kanji_words": words,
    }


def validate(data: dict) -> None:
    if len(data["kanji_topics"]) != 15:
        raise ValueError(f"Expected 15 topics, got {len(data['kanji_topics'])}")
    if len(data["kanji_characters"]) != 118:
        raise ValueError(
            f"Expected 118 kanji characters, got {len(data['kanji_characters'])}"
        )

    topic_ids = {topic["id"] for topic in data["kanji_topics"]}
    character_ids = {char["id"] for char in data["kanji_characters"]}
    for group in ("kanji_topics", "kanji_characters", "kanji_words"):
        for item in data[group]:
            if "note" in item:
                raise ValueError(f"Unexpected note field in {group}: {item}")

    for topic in data["kanji_topics"]:
        if not topic["name"] or not topic["name_vi"]:
            raise ValueError(f"Missing topic text: {topic}")

    for char in data["kanji_characters"]:
        if char["kanji_topic_id"] not in topic_ids:
            raise ValueError(f"Invalid kanji_topic_id: {char}")
        for key in ("character_value", "han_viet", "meaning_vi", "mnemonic_vi"):
            if not char.get(key):
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
            if not word.get(key):
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
