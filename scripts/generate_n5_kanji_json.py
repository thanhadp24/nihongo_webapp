import json
from datetime import datetime, timezone
from pathlib import Path


OUTPUT = Path("database/import/jlpt_n5_kanji_by_topic_db_import.json")

TOPICS = [
    {
        "id": 1,
        "jlpt_level_id": 1,
        "name": "お名前は?",
        "name_vi": "Tên và giới thiệu bản thân",
        "description": "Bài kanji/vocabulary về tên, người, quốc tịch, trường học và giới thiệu cơ bản.",
        "source_week": 1,
        "source_day": 1,
        "source_page_start": 16,
    },
    {
        "id": 2,
        "jlpt_level_id": 1,
        "name": "それは何ですか。",
        "name_vi": "Đây là gì?",
        "description": "Bài kanji/vocabulary về thời gian, ngày tháng, tuần và câu hỏi với 何.",
        "source_week": 1,
        "source_day": 2,
        "source_page_start": 18,
    },
    {
        "id": 3,
        "jlpt_level_id": 1,
        "name": "大きい ↔ 小さい",
        "name_vi": "Lớn và nhỏ",
        "description": "Bài kanji/vocabulary về tính chất, kích thước, mức độ và màu sắc cơ bản.",
        "source_week": 1,
        "source_day": 3,
        "source_page_start": 20,
    },
    {
        "id": 4,
        "jlpt_level_id": 1,
        "name": "どこですか。",
        "name_vi": "Ở đâu?",
        "description": "Bài kanji/vocabulary về địa điểm, lối ra vào, vị trí và phương hướng.",
        "source_week": 1,
        "source_day": 4,
        "source_page_start": 22,
    },
    {
        "id": 5,
        "jlpt_level_id": 1,
        "name": "何をしていますか。",
        "name_vi": "Đang làm gì?",
        "description": "Bài kanji/vocabulary về các hoạt động sinh hoạt thường gặp.",
        "source_week": 1,
        "source_day": 5,
        "source_page_start": 24,
    },
    {
        "id": 6,
        "jlpt_level_id": 1,
        "name": "手と足",
        "name_vi": "Tay và chân",
        "description": "Bài kanji/vocabulary về cơ thể, tay chân, sức lực và nghỉ ngơi.",
        "source_week": 1,
        "source_day": 6,
        "source_page_start": 26,
    },
    {
        "id": 7,
        "jlpt_level_id": 1,
        "name": "つめたい飲みもの",
        "name_vi": "Đồ uống lạnh",
        "description": "Bài kanji/vocabulary về tự nhiên, thời tiết, cảm giác và các sự vật quen thuộc.",
        "source_week": 2,
        "source_day": 1,
        "source_page_start": 32,
    },
    {
        "id": 8,
        "jlpt_level_id": 1,
        "name": "はたらいています",
        "name_vi": "Đang làm việc",
        "description": "Bài kanji/vocabulary về trường học, công ty, nhân viên và việc dạy học.",
        "source_week": 2,
        "source_day": 2,
        "source_page_start": 34,
    },
    {
        "id": 9,
        "jlpt_level_id": 1,
        "name": "どのぐらい?",
        "name_vi": "Bao nhiêu, bao lâu?",
        "description": "Bài kanji/vocabulary về số đếm, lượng, tiền và khoảng thời gian.",
        "source_week": 2,
        "source_day": 3,
        "source_page_start": 36,
    },
    {
        "id": 10,
        "jlpt_level_id": 1,
        "name": "ちょっと...",
        "name_vi": "Một chút...",
        "description": "Bài kanji/vocabulary về đi lại, mua sắm, cửa hàng, phương tiện và đồ vật.",
        "source_week": 2,
        "source_day": 4,
        "source_page_start": 38,
    },
    {
        "id": 11,
        "jlpt_level_id": 1,
        "name": "かぞく",
        "name_vi": "Gia đình",
        "description": "Bài kanji/vocabulary về cha mẹ và các cách gọi người thân ở trình độ N5.",
        "source_week": 2,
        "source_day": 5,
        "source_page_start": 40,
    },
    {
        "id": 12,
        "jlpt_level_id": 1,
        "name": "すきなもの・ほしいもの",
        "name_vi": "Điều thích và điều muốn có",
        "description": "Bài kanji/vocabulary về sở thích, đồ vật, đồ ăn uống và những thứ muốn mua.",
        "source_week": 2,
        "source_day": 6,
        "source_page_start": 42,
    },
]

TOPIC_BY_KANJI = {
    "先": 1,
    "生": 1,
    "学": 1,
    "人": 1,
    "国": 1,
    "男": 1,
    "女": 1,
    "子": 1,
    "友": 1,
    "名": 1,
    "語": 1,
    "何": 2,
    "時": 2,
    "分": 2,
    "間": 2,
    "半": 2,
    "午": 2,
    "前": 2,
    "後": 2,
    "今": 2,
    "週": 2,
    "毎": 2,
    "日": 2,
    "月": 2,
    "年": 2,
    "曜": 2,
    "少": 3,
    "多": 3,
    "小": 3,
    "大": 3,
    "安": 3,
    "高": 3,
    "新": 3,
    "古": 3,
    "早": 3,
    "長": 3,
    "白": 3,
    "黒": 3,
    "赤": 3,
    "青": 3,
    "駅": 4,
    "口": 4,
    "出": 4,
    "入": 4,
    "東": 4,
    "西": 4,
    "南": 4,
    "北": 4,
    "上": 4,
    "下": 4,
    "左": 4,
    "右": 4,
    "中": 4,
    "外": 4,
    "食": 5,
    "飲": 5,
    "見": 5,
    "書": 5,
    "読": 5,
    "聞": 5,
    "話": 5,
    "立": 5,
    "体": 6,
    "目": 6,
    "耳": 6,
    "手": 6,
    "足": 6,
    "力": 6,
    "休": 6,
    "火": 7,
    "水": 7,
    "木": 7,
    "金": 7,
    "土": 7,
    "雨": 7,
    "天": 7,
    "空": 7,
    "山": 7,
    "川": 7,
    "田": 7,
    "花": 7,
    "校": 8,
    "会": 8,
    "社": 8,
    "員": 8,
    "教": 8,
    "一": 9,
    "二": 9,
    "三": 9,
    "四": 9,
    "五": 9,
    "六": 9,
    "七": 9,
    "八": 9,
    "九": 9,
    "十": 9,
    "百": 9,
    "千": 9,
    "万": 9,
    "円": 9,
    "行": 10,
    "来": 10,
    "帰": 10,
    "車": 10,
    "電": 10,
    "店": 10,
    "買": 10,
    "気": 10,
    "本": 10,
    "父": 11,
    "母": 11,
    "好": 12,
    "物": 12,
    "私": 12,
    "家": 12,
}


# topic_id|kanji|han_viet|onyomi|kunyomi|meaning_vi|stroke_count|word:reading:meaning_vi;...
RAW_DATA = """
1|先|tiên|セン|さき|trước, trước tiên|6|先生:せんせい:giáo viên, thầy cô;先月:せんげつ:tháng trước;お先に:おさきに:trước
1|生|sinh|セイ,ショウ|い(きる),う(まれる)|sinh, sống|5|学生:がくせい:học sinh, sinh viên;生活:せいかつ:cuộc sống, sinh hoạt;誕生日:たんじょうび:sinh nhật
1|学|học|ガク|まな(ぶ)|học|8|学生:がくせい:học sinh, sinh viên;学校:がっこう:trường học;大学:だいがく:đại học
1|人|nhân|ジン,ニン|ひと|người|2|日本人:にほんじん:người Nhật;外国人:がいこくじん:người nước ngoài;一人:ひとり:một người
1|国|quốc|コク|くに|nước, quốc gia|8|外国:がいこく:nước ngoài;中国:ちゅうごく:Trung Quốc;国:くに:đất nước
1|男|nam|ダン,ナン|おとこ|nam, đàn ông|7|男の人:おとこのひと:người đàn ông;男の子:おとこのこ:bé trai;男性:だんせい:nam giới
1|女|nữ|ジョ,ニョ|おんな|nữ, phụ nữ|3|女の人:おんなのひと:người phụ nữ;女の子:おんなのこ:bé gái;彼女:かのじょ:cô ấy, bạn gái
1|子|tử|シ,ス|こ|con, trẻ em|3|子ども:こども:trẻ em;男の子:おとこのこ:bé trai;女の子:おんなのこ:bé gái
1|友|hữu|ユウ|とも|bạn|4|友だち:ともだち:bạn bè;友人:ゆうじん:bạn hữu;親友:しんゆう:bạn thân
1|父|phụ|フ|ちち|cha, bố|4|父:ちち:cha tôi;お父さん:おとうさん:bố, cha;父母:ふぼ:cha mẹ
1|母|mẫu|ボ|はは|mẹ|5|母:はは:mẹ tôi;お母さん:おかあさん:mẹ;父母:ふぼ:cha mẹ
1|名|danh|メイ,ミョウ|な|tên, danh tiếng|6|名前:なまえ:tên;有名な:ゆうめいな:nổi tiếng;名刺:めいし:danh thiếp
1|語|ngữ|ゴ|かた(る)|ngôn ngữ, lời nói|14|日本語:にほんご:tiếng Nhật;英語:えいご:tiếng Anh;何語:なんご:tiếng gì
2|日|nhật|ニチ,ジツ|ひ,か|ngày, mặt trời|4|日本:にほん:Nhật Bản;日曜日:にちようび:Chủ nhật;今日:きょう:hôm nay
2|月|nguyệt|ゲツ,ガツ|つき|tháng, mặt trăng|4|月曜日:げつようび:thứ Hai;今月:こんげつ:tháng này;一月:いちがつ:tháng Một
2|火|hỏa|カ|ひ|lửa|4|火曜日:かようび:thứ Ba;火:ひ:lửa;花火:はなび:pháo hoa
2|水|thủy|スイ|みず|nước|4|水曜日:すいようび:thứ Tư;水:みず:nước;水道:すいどう:nước máy
2|木|mộc|モク,ボク|き|cây, gỗ|4|木曜日:もくようび:thứ Năm;木:き:cây;木村:きむら:tên họ Kimura
2|金|kim|キン,コン|かね|vàng, tiền, kim loại|8|金曜日:きんようび:thứ Sáu;お金:おかね:tiền;料金:りょうきん:phí
2|土|thổ|ド,ト|つち|đất|3|土曜日:どようび:thứ Bảy;土:つち:đất;土地:とち:đất đai
2|曜|diệu|ヨウ||ngày trong tuần|18|曜日:ようび:thứ trong tuần;日曜日:にちようび:Chủ nhật;何曜日:なんようび:thứ mấy
2|年|niên|ネン|とし|năm, tuổi|6|今年:ことし:năm nay;来年:らいねん:năm sau;一年:いちねん:một năm
2|時|thời|ジ|とき|giờ, thời gian|10|時間:じかん:thời gian;時計:とけい:đồng hồ;一時:いちじ:một giờ
2|分|phân|フン,ブン,ブ|わ(かる)|phút, phần, hiểu|4|五分:ごふん:năm phút;半分:はんぶん:một nửa;分かる:わかる:hiểu
2|間|gian|カン,ケン|あいだ,ま|khoảng, giữa|12|時間:じかん:thời gian;一週間:いっしゅうかん:một tuần;間に合う:まにあう:kịp giờ
2|半|bán|ハン|なか(ば)|một nửa|5|半分:はんぶん:một nửa;七時半:しちじはん:bảy giờ rưỡi;一年半:いちねんはん:một năm rưỡi
2|午|ngọ|ゴ||buổi trưa|4|午前:ごぜん:buổi sáng;午後:ごご:buổi chiều;正午:しょうご:chính ngọ
2|前|tiền|ゼン|まえ|trước|9|午前:ごぜん:buổi sáng;名前:なまえ:tên;前:まえ:phía trước
2|後|hậu|ゴ,コウ|あと,うし(ろ),のち|sau|9|午後:ごご:buổi chiều;後で:あとで:lát nữa;後ろ:うしろ:phía sau
2|今|kim|コン,キン|いま|bây giờ, hiện tại|4|今:いま:bây giờ;今日:きょう:hôm nay;今週:こんしゅう:tuần này
2|週|chu|シュウ||tuần|11|今週:こんしゅう:tuần này;先週:せんしゅう:tuần trước;来週:らいしゅう:tuần sau
2|毎|mỗi|マイ|ごと|mỗi, hằng|6|毎日:まいにち:hằng ngày;毎週:まいしゅう:hằng tuần;毎朝:まいあさ:mỗi sáng
2|何|hà|カ|なに,なん|cái gì, bao nhiêu|7|何:なに:cái gì;何時:なんじ:mấy giờ;何人:なんにん:mấy người
3|一|nhất|イチ,イツ|ひと(つ)|một|1|一つ:ひとつ:một cái;一日:いちにち:một ngày;一人:ひとり:một người
3|二|nhị|ニ|ふた(つ)|hai|2|二つ:ふたつ:hai cái;二日:ふつか:ngày mùng hai, hai ngày;二人:ふたり:hai người
3|三|tam|サン|み(つ)|ba|3|三つ:みっつ:ba cái;三日:みっか:ngày mùng ba, ba ngày;三月:さんがつ:tháng Ba
3|四|tứ|シ|よん,よ,よっ(つ)|bốn|5|四つ:よっつ:bốn cái;四月:しがつ:tháng Tư;四人:よにん:bốn người
3|五|ngũ|ゴ|いつ(つ)|năm|4|五つ:いつつ:năm cái;五月:ごがつ:tháng Năm;五分:ごふん:năm phút
3|六|lục|ロク|むっ(つ)|sáu|4|六つ:むっつ:sáu cái;六月:ろくがつ:tháng Sáu;六日:むいか:ngày mùng sáu, sáu ngày
3|七|thất|シチ|なな(つ),なの|bảy|2|七つ:ななつ:bảy cái;七月:しちがつ:tháng Bảy;七日:なのか:ngày mùng bảy, bảy ngày
3|八|bát|ハチ|やっ(つ)|tám|2|八つ:やっつ:tám cái;八月:はちがつ:tháng Tám;八日:ようか:ngày mùng tám, tám ngày
3|九|cửu|キュウ,ク|ここの(つ)|chín|2|九つ:ここのつ:chín cái;九月:くがつ:tháng Chín;九日:ここのか:ngày mùng chín, chín ngày
3|十|thập|ジュウ,ジッ|とお|mười|2|十:じゅう:mười;十日:とおか:ngày mùng mười, mười ngày;十分:じゅっぷん:mười phút
3|百|bách|ヒャク||trăm|6|百:ひゃく:một trăm;三百:さんびゃく:ba trăm;百円:ひゃくえん:một trăm yên
3|千|thiên|セン|ち|nghìn|3|千:せん:một nghìn;三千:さんぜん:ba nghìn;千円:せんえん:một nghìn yên
3|万|vạn|マン,バン||mười nghìn|3|一万:いちまん:mười nghìn;万円:まんえん:mười nghìn yên;万年筆:まんねんひつ:bút máy
3|円|viên|エン|まる(い)|yên, hình tròn|4|円:えん:yên;百円:ひゃくえん:một trăm yên;円い:まるい:tròn
4|少|thiểu|ショウ|すく(ない),すこ(し)|ít, một chút|4|少し:すこし:một chút;少ない:すくない:ít;少年:しょうねん:thiếu niên
4|多|đa|タ|おお(い)|nhiều|6|多い:おおい:nhiều;多少:たしょう:ít nhiều;多分:たぶん:có lẽ
4|小|tiểu|ショウ|ちい(さい),こ,お|nhỏ|3|小さい:ちいさい:nhỏ;小学校:しょうがっこう:trường tiểu học;小さな:ちいさな:nhỏ
4|大|đại|ダイ,タイ|おお(きい)|to, lớn|3|大きい:おおきい:to, lớn;大学:だいがく:đại học;大切な:たいせつな:quan trọng
4|安|an|アン|やす(い)|rẻ, yên ổn|6|安い:やすい:rẻ;安全な:あんぜんな:an toàn;安心する:あんしんする:yên tâm
4|高|cao|コウ|たか(い)|cao, đắt|10|高い:たかい:cao, đắt;高校:こうこう:trường cấp ba;高山:こうざん:núi cao
4|新|tân|シン|あたら(しい),あら(た)|mới|13|新しい:あたらしい:mới;新聞:しんぶん:báo;新年:しんねん:năm mới
4|古|cổ|コ|ふる(い)|cũ, cổ|5|古い:ふるい:cũ;中古:ちゅうこ:đồ cũ;古本:ふるほん:sách cũ
4|早|tảo|ソウ|はや(い)|sớm, nhanh|6|早い:はやい:sớm, nhanh;早く:はやく:sớm lên;早朝:そうちょう:sáng sớm
4|長|trường|チョウ|なが(い)|dài, trưởng|8|長い:ながい:dài;社長:しゃちょう:giám đốc công ty;校長:こうちょう:hiệu trưởng
4|白|bạch|ハク,ビャク|しろ,しろ(い)|trắng|5|白い:しろい:trắng;白:しろ:màu trắng;白紙:はくし:giấy trắng
4|黒|hắc|コク|くろ,くろ(い)|đen|11|黒い:くろい:đen;黒:くろ:màu đen;黒板:こくばん:bảng đen
4|赤|xích|セキ|あか,あか(い)|đỏ|7|赤い:あかい:đỏ;赤:あか:màu đỏ;赤ちゃん:あかちゃん:em bé
4|青|thanh|セイ,ショウ|あお,あお(い)|xanh lam, xanh|8|青い:あおい:xanh;青:あお:màu xanh;青年:せいねん:thanh niên
5|駅|dịch|エキ||nhà ga|14|駅:えき:nhà ga;駅前:えきまえ:trước ga;東京駅:とうきょうえき:ga Tokyo
5|口|khẩu|コウ,ク|くち|miệng, cửa|3|口:くち:miệng;入口:いりぐち:lối vào;出口:でぐち:lối ra
5|出|xuất|シュツ,スイ|で(る),だ(す)|ra, đưa ra|5|出る:でる:ra, xuất hiện;出す:だす:đưa ra, nộp;出口:でぐち:lối ra
5|入|nhập|ニュウ|はい(る),い(る),い(れる)|vào, cho vào|2|入る:はいる:vào;入れる:いれる:cho vào;入口:いりぐち:lối vào
5|東|đông|トウ|ひがし|phía đông|8|東:ひがし:phía đông;東京:とうきょう:Tokyo;東口:ひがしぐち:cửa đông
5|西|tây|セイ,サイ|にし|phía tây|6|西:にし:phía tây;西口:にしぐち:cửa tây;関西:かんさい:vùng Kansai
5|南|nam|ナン|みなみ|phía nam|9|南:みなみ:phía nam;南口:みなみぐち:cửa nam;東南:とうなん:đông nam
5|北|bắc|ホク|きた|phía bắc|5|北:きた:phía bắc;北口:きたぐち:cửa bắc;北海道:ほっかいどう:Hokkaido
5|上|thượng|ジョウ,ショウ|うえ,うわ,あ(げる),のぼ(る)|trên, lên|3|上:うえ:phía trên;上手な:じょうずな:giỏi;上着:うわぎ:áo khoác
5|下|hạ|カ,ゲ|した,しも,さ(げる),くだ(る)|dưới, xuống|3|下:した:phía dưới;地下鉄:ちかてつ:tàu điện ngầm;下手な:へたな:kém
5|左|tả|サ|ひだり|bên trái|5|左:ひだり:bên trái;左手:ひだりて:tay trái;左側:ひだりがわ:phía bên trái
5|右|hữu|ウ,ユウ|みぎ|bên phải|5|右:みぎ:bên phải;右手:みぎて:tay phải;右側:みぎがわ:phía bên phải
5|中|trung|チュウ|なか|trong, giữa|4|中:なか:bên trong;中国:ちゅうごく:Trung Quốc;一日中:いちにちじゅう:cả ngày
5|外|ngoại|ガイ,ゲ|そと,ほか,はず(す)|ngoài|5|外:そと:bên ngoài;外国:がいこく:nước ngoài;外す:はずす:tháo ra
6|山|sơn|サン|やま|núi|3|山:やま:núi;火山:かざん:núi lửa;富士山:ふじさん:núi Phú Sĩ
6|川|xuyên|セン|かわ|sông|3|川:かわ:sông;小川:おがわ:suối nhỏ;川口:かわぐち:cửa sông, họ Kawaguchi
6|田|điền|デン|た|ruộng|5|田:た:ruộng;田中:たなか:họ Tanaka;水田:すいでん:ruộng nước
6|雨|vũ|ウ|あめ,あま|mưa|8|雨:あめ:mưa;大雨:おおあめ:mưa to;雨天:うてん:trời mưa
6|天|thiên|テン|あま,あめ|trời|4|天気:てんき:thời tiết;天:てん:trời;雨天:うてん:trời mưa
6|空|không|クウ|そら,あ(く),から|bầu trời, trống|8|空:そら:bầu trời;空気:くうき:không khí;空港:くうこう:sân bay
6|花|hoa|カ|はな|hoa|7|花:はな:hoa;花見:はなみ:ngắm hoa;花火:はなび:pháo hoa
6|本|bản|ホン|もと|sách, gốc, cái dài|5|本:ほん:sách;日本:にほん:Nhật Bản;一本:いっぽん:một cây, một chiếc dài
6|休|hưu|キュウ|やす(む)|nghỉ|6|休む:やすむ:nghỉ;休み:やすみ:ngày nghỉ;休日:きゅうじつ:ngày nghỉ
6|体|thể|タイ,テイ|からだ|cơ thể|7|体:からだ:cơ thể;体育:たいいく:thể dục;体力:たいりょく:thể lực
6|目|mục|モク,ボク|め|mắt, mục|5|目:め:mắt;一日目:いちにちめ:ngày thứ nhất;目的:もくてき:mục đích
6|耳|nhĩ|ジ|みみ|tai|6|耳:みみ:tai;耳鼻科:じびか:khoa tai mũi;耳元:みみもと:gần tai
6|手|thủ|シュ|て|tay|4|手:て:tay;上手な:じょうずな:giỏi;手紙:てがみ:thư
6|足|túc|ソク|あし,た(りる)|chân, đủ|7|足:あし:chân;足りる:たりる:đủ;一足:いっそく:một đôi giày
6|力|lực|リョク,リキ|ちから|sức mạnh|2|力:ちから:sức mạnh;体力:たいりょく:thể lực;力学:りきがく:cơ học
7|校|hiệu|コウ||trường học|10|学校:がっこう:trường học;小学校:しょうがっこう:trường tiểu học;校長:こうちょう:hiệu trưởng
7|会|hội|カイ,エ|あ(う)|gặp, hội|6|会う:あう:gặp;会社:かいしゃ:công ty;会話:かいわ:hội thoại
7|社|xã|シャ|やしろ|công ty, đền|7|会社:かいしゃ:công ty;社長:しゃちょう:giám đốc;神社:じんじゃ:đền Thần đạo
7|員|viên|イン||nhân viên, thành viên|10|会社員:かいしゃいん:nhân viên công ty;店員:てんいん:nhân viên cửa hàng;銀行員:ぎんこういん:nhân viên ngân hàng
7|店|điếm|テン|みせ|cửa hàng|8|店:みせ:cửa hàng;店員:てんいん:nhân viên cửa hàng;本店:ほんてん:cửa hàng chính
7|車|xa|シャ|くるま|xe|7|車:くるま:xe hơi;電車:でんしゃ:tàu điện;自転車:じてんしゃ:xe đạp
7|電|điện|デン||điện|13|電車:でんしゃ:tàu điện;電話:でんわ:điện thoại;電気:でんき:điện, đèn điện
7|気|khí|キ,ケ||khí, tinh thần|6|天気:てんき:thời tiết;元気な:げんきな:khỏe mạnh;電気:でんき:điện
8|食|thực|ショク,ジキ|た(べる),く(う)|ăn, thức ăn|9|食べる:たべる:ăn;食べ物:たべもの:đồ ăn;食堂:しょくどう:nhà ăn
8|飲|ẩm|イン|の(む)|uống|12|飲む:のむ:uống;飲み物:のみもの:đồ uống;飲食:いんしょく:ăn uống
8|見|kiến|ケン|み(る),み(える),み(せる)|nhìn, xem|7|見る:みる:xem, nhìn;見える:みえる:nhìn thấy;花見:はなみ:ngắm hoa
8|行|hành|コウ,ギョウ|い(く),おこな(う)|đi, thực hiện|6|行く:いく:đi;旅行:りょこう:du lịch;銀行:ぎんこう:ngân hàng
8|来|lai|ライ|く(る),きた(る)|đến|7|来る:くる:đến;来週:らいしゅう:tuần sau;来年:らいねん:năm sau
8|帰|quy|キ|かえ(る)|trở về|10|帰る:かえる:trở về;帰国:きこく:về nước;お帰り:おかえり:mừng về nhà
8|書|thư|ショ|か(く)|viết, sách|10|書く:かく:viết;辞書:じしょ:từ điển;図書館:としょかん:thư viện
8|読|độc|ドク,トク|よ(む)|đọc|14|読む:よむ:đọc;読書:どくしょ:đọc sách;読み方:よみかた:cách đọc
8|聞|văn|ブン,モン|き(く),き(こえる)|nghe, hỏi|14|聞く:きく:nghe, hỏi;新聞:しんぶん:báo;聞こえる:きこえる:nghe thấy
8|話|thoại|ワ|はな(す),はなし|nói, câu chuyện|13|話す:はなす:nói;電話:でんわ:điện thoại;会話:かいわ:hội thoại
8|買|mãi|バイ|か(う)|mua|12|買う:かう:mua;買い物:かいもの:mua sắm;売買:ばいばい:mua bán
8|教|giáo|キョウ|おし(える),おそ(わる)|dạy, học từ ai|11|教える:おしえる:dạy, chỉ cho;教室:きょうしつ:lớp học;教師:きょうし:giáo viên
8|立|lập|リツ,リュウ|た(つ),た(てる)|đứng, dựng lên|5|立つ:たつ:đứng;立てる:たてる:dựng lên;国立:こくりつ:quốc lập
12|好|hiếu|コウ|す(き),この(む)|thích, tốt|6|好きな:すきな:yêu thích;大好きな:だいすきな:rất thích;好む:このむ:ưa thích
12|物|vật|ブツ,モツ|もの|đồ vật|8|物:もの:đồ vật;食べ物:たべもの:đồ ăn;飲み物:のみもの:đồ uống
12|私|tư|シ|わたし,わたくし|tôi, riêng tư|7|私:わたし:tôi;私たち:わたしたち:chúng tôi;私立:しりつ:tư lập
12|家|gia|カ,ケ|いえ,や|nhà, gia đình|10|家:いえ:nhà;家族:かぞく:gia đình;大家:おおや:chủ nhà
""".strip()


def split_nullable(value: str) -> str | None:
    value = value.strip()
    return value or None


def build_data() -> dict:
    topics = []
    for order, topic in enumerate(TOPICS, start=1):
        row = dict(topic)
        row.setdefault("source_book", "Soumatome N5")
        row.update({"display_order": order, "is_published": True, "version": 1})
        topics.append(row)

    characters = []
    words = []
    character_id = 1
    word_id = 1
    order_by_topic: dict[int, int] = {}

    for raw_line in RAW_DATA.splitlines():
        parts = raw_line.split("|")
        if len(parts) != 8:
            raise ValueError(f"Invalid row: {raw_line}")

        topic_id = TOPIC_BY_KANJI.get(parts[1], int(parts[0]))
        order_by_topic[topic_id] = order_by_topic.get(topic_id, 0) + 1

        character = {
            "id": character_id,
            "kanji_topic_id": topic_id,
            "character_value": parts[1],
            "han_viet": split_nullable(parts[2]),
            "onyomi": split_nullable(parts[3]),
            "kunyomi": split_nullable(parts[4]),
            "meaning_vi": parts[5],
            "stroke_count": int(parts[6]),
            "mnemonic_vi": None,
            "display_order": order_by_topic[topic_id],
            "is_published": True,
            "version": 1,
        }
        characters.append(character)

        for word_order, word_raw in enumerate(parts[7].split(";"), start=1):
            word, reading, meaning = word_raw.split(":", 2)
            example_sentence, example_reading, example_meaning = build_word_example(
                word, reading, meaning
            )
            words.append(
                {
                    "id": word_id,
                    "kanji_character_id": character_id,
                    "word": word,
                    "reading": split_nullable(reading),
                    "meaning_vi": meaning,
                    "example_sentence": example_sentence,
                    "example_reading": example_reading,
                    "example_meaning_vi": example_meaning,
                    "display_order": word_order,
                    "is_published": True,
                    "version": 1,
                }
            )
            word_id += 1

        character_id += 1

    return {
        "metadata": {
            "name": "JLPT N5 kanji import data",
            "jlpt_level_code": "N5",
            "jlpt_level_id_assumption": 1,
            "source_file": "plan/kanji/[Nihongopro.net]-N5-soumatome-tieng-viet.pdf",
            "source_note": "PDF is image-based; text extraction only exposes watermark text. Data was normalized from the visible Soumatome N5 kanji structure and completed with standard N5 kanji readings, Sino-Vietnamese readings, meanings, stroke counts, and vocabulary examples.",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "import_order": [
                "kanji_topics",
                "kanji_characters",
                "kanji_words",
            ],
            "notes": [
                "The JSON follows the simple UI flow: jlpt_levels -> kanji_topics -> kanji_characters -> kanji_words.",
                "kanji_topics.name is Japanese-first. kanji_topics.name_vi is a Vietnamese subtitle for the UI.",
                "source_week, source_day, and source_page_start preserve the Soumatome-style lesson origin.",
                "han_viet stores the Sino-Vietnamese reading.",
                "word uses kanji where applicable; reading stores kana/furigana reading.",
                "example_* fields are generated learning examples for every kanji word.",
            ],
        },
        "kanji_topics": topics,
        "kanji_characters": characters,
        "kanji_words": words,
    }


def validate(data: dict) -> None:
    topic_ids = {topic["id"] for topic in data["kanji_topics"]}
    character_ids = {char["id"] for char in data["kanji_characters"]}
    seen_chars: set[str] = set()

    for char in data["kanji_characters"]:
        if char["kanji_topic_id"] not in topic_ids:
            raise ValueError(f"Missing topic for kanji {char['character_value']}")
        if char["character_value"] in seen_chars:
            raise ValueError(f"Duplicate kanji: {char['character_value']}")
        seen_chars.add(char["character_value"])
        for key in ("character_value", "han_viet", "meaning_vi", "display_order"):
            if char[key] in (None, ""):
                raise ValueError(f"Missing {key} for {char['character_value']}")

    for word in data["kanji_words"]:
        if word["kanji_character_id"] not in character_ids:
            raise ValueError(f"Missing kanji for word {word['word']}")
        for key in ("word", "reading", "meaning_vi", "display_order"):
            if word[key] in (None, ""):
                raise ValueError(f"Missing {key} for word id={word['id']}")
        for key in ("example_sentence", "example_reading", "example_meaning_vi"):
            if word[key] in (None, ""):
                raise ValueError(f"Missing {key} for word id={word['id']}")

    empty_topics = [
        topic["id"]
        for topic in data["kanji_topics"]
        if not any(char["kanji_topic_id"] == topic["id"] for char in data["kanji_characters"])
    ]
    if empty_topics:
        raise ValueError(f"Topics without kanji: {empty_topics}")


def build_word_example(word: str, reading: str, meaning_vi: str) -> tuple[str, str, str]:
    sentence = f"「{word}」をもう一度読みます。"
    sentence_reading = f"「{reading}」をもういちどよみます。"
    sentence_meaning = f"Tôi đọc lại từ '{word}' ({meaning_vi})."
    return sentence, sentence_reading, sentence_meaning


if __name__ == "__main__":
    data = build_data()
    validate(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"topics={len(data['kanji_topics'])}")
    print(f"kanji_characters={len(data['kanji_characters'])}")
    print(f"kanji_words={len(data['kanji_words'])}")
