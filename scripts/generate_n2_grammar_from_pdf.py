import json
from pathlib import Path


JLPT_LEVEL_ID = 4
GRAMMAR_CHAPTER_START_ID = 64
GRAMMAR_LESSON_START_ID = 295
GRAMMAR_EXAMPLE_START_ID = 418

SOURCE_PDF = Path("plan/TỔNG HỢP NGỮ PHÁP N2.pdf")
OUTPUT_JSON_PATH = Path("database/import/jlpt_n2_grammar_by_chapter_db_import.json")
OUTPUT_SQL_PATH = Path("database/seed/010_jlpt_n2_grammar.sql")


RAW_DATA = """
1	～際(に)	Khi, nhân lúc, nhân dịp	お申し込みの際に、身分証明書をお持ちください。	おもうしこみのさいに、みぶんしょうめいしょをおもちください。	Khi đăng ký, vui lòng mang theo giấy tờ tùy thân.
1	～に際して／～にあたって	Tại thời điểm, nhân dịp	入学に際して、必要な書類を提出してください。	にゅうがくにさいして、ひつようなしょるいをていしゅつしてください。	Khi nhập học, hãy nộp các giấy tờ cần thiết.
1	～たとたん(に)	Ngay khi vừa mới thì	ドアを開けたとたん、電話が鳴った。	ドアをあけたとたん、でんわがなった。	Ngay khi tôi vừa mở cửa thì điện thoại reo.
1	～(か)と思うと／～(か)と思ったら	Vừa mới thì lập tức	赤ちゃんは泣いたかと思うと、すぐ笑い出した。	あかちゃんはないたかとおもうと、すぐわらいだした。	Em bé vừa khóc xong đã bật cười ngay.
1	～(か)～ないかのうちに	Ngay sau khi vừa	布団に入るか入らないかのうちに、眠ってしまった。	ふとんにはいるかはいらないかのうちに、ねむってしまった。	Tôi vừa chui vào chăn là ngủ mất ngay.
2	～最中だ	Đúng lúc, ngay trong lúc	会議の最中に、急な電話が入った。	かいぎのさいちゅうに、きゅうなでんわがはいった。	Đúng lúc đang họp thì có cuộc gọi gấp.
2	～うちに(P1)	Nhân lúc, khi còn	若いうちに、いろいろな経験をしておきたい。	わかいうちに、いろいろなけいけんをしておきたい。	Tôi muốn trải nghiệm nhiều thứ khi còn trẻ.
2	～うちに(P2)	Trong khi đang thì dần	本を読んでいるうちに、外が暗くなった。	ほんをよんでいるうちに、そとがくらくなった。	Trong lúc đọc sách thì trời bên ngoài tối dần.
2	～ばかりだ	Ngày càng, cứ mãi	物価は上がるばかりで、生活が大変だ。	ぶっかはあがるばかりで、せいかつがたいへんだ。	Giá cả cứ tăng mãi nên cuộc sống thật vất vả.
2	～一方だ	Ngày càng theo một chiều hướng	仕事は増える一方で、休む時間がない。	しごとはふえるいっぽうで、やすむじかんがない。	Công việc ngày càng tăng nên không có thời gian nghỉ.
2	～ようとしている	Sắp sửa, đang định	空が暗くなり、雨が降ろうとしている。	そらがくらくなり、あめがふろうとしている。	Trời tối lại và mưa sắp rơi.
2	～つつある	Đang dần	この町は少しずつ変わりつつある。	このまちはすこしずつかわりつつある。	Thị trấn này đang dần thay đổi.
2	～つつ	Vừa vừa, trong lúc	悪いと思いつつ、彼に本当のことを言えなかった。	わるいとおもいつつ、かれにほんとうのことをいえなかった。	Dù biết là không tốt, tôi vẫn không thể nói thật với anh ấy.
3	～てはじめて	Chỉ sau khi mới nhận ra	一人で暮らしてはじめて、親のありがたさが分かった。	ひとりでくらしてはじめて、おやのありがたさがわかった。	Chỉ sau khi sống một mình tôi mới hiểu sự đáng quý của cha mẹ.
3	～上で	Sau khi, trên cơ sở	内容を確認した上で、契約書にサインしてください。	ないようをかくにんしたうえで、けいやくしょにサインしてください。	Sau khi kiểm tra nội dung, hãy ký hợp đồng.
3	～次第	Sau khi xong thì sẽ ngay	準備ができ次第、すぐに出発します。	じゅんびができしだい、すぐにしゅっぱつします。	Ngay khi chuẩn bị xong, chúng tôi sẽ xuất phát.
3	～以来	Suốt từ sau khi	日本に来て以来、毎日日本語を使っています。	にほんにきていらい、まいにちにほんごをつかっています。	Từ khi đến Nhật, ngày nào tôi cũng dùng tiếng Nhật.
3	～このかた	Suốt từ sau khi	卒業してこのかた、彼とは一度も会っていません。	そつぎょうしてこのかた、かれとはいちどもあっていません。	Từ sau khi tốt nghiệp đến nay tôi chưa gặp anh ấy lần nào.
3	～からでないと／～からでなければ	Nếu không sau khi thì không thể	予約してからでないと、この部屋は使えません。	よやくしてからでないと、このへやはつかえません。	Nếu chưa đặt trước thì không thể sử dụng phòng này.
4	～をはじめ(として)	Trước hết phải kể tới	京都には清水寺をはじめ、多くの名所がある。	きょうとにはきよみずでらをはじめ、おおくのめいしょがある。	Ở Kyoto có nhiều danh thắng, trước hết phải kể đến chùa Kiyomizu.
4	～をはじめとする	Bao gồm tiêu biểu là	社長をはじめとする社員全員が会議に参加した。	しゃちょうをはじめとするしゃいんぜんいんがかいぎにさんかした。	Toàn bộ nhân viên gồm cả giám đốc đã tham gia cuộc họp.
4	～からして	Ngay từ, xét ngay từ	彼の態度からして、反省していないようだ。	かれのたいどからして、はんせいしていないようだ。	Xét ngay từ thái độ của anh ấy, có vẻ anh ấy không hối lỗi.
4	～にわたって／～にわたる	Trải suốt, trải khắp	台風の影響は広い地域にわたって続いた。	たいふうのえいきょうはひろいちいきにわたってつづいた。	Ảnh hưởng của bão kéo dài trên một khu vực rộng.
4	～を通じて／～を通して	Suốt, thông qua	一年を通じて、この図書館は多くの学生に利用されている。	いちねんをつうじて、このとしょかんはおおくのがくせいにりようされている。	Thư viện này được nhiều sinh viên sử dụng suốt cả năm.
4	～限り	Bằng tất cả, chừng nào còn	私の知る限り、彼は約束を破ったことがない。	わたしのしるかぎり、かれはやくそくをやぶったことがない。	Theo những gì tôi biết, anh ấy chưa từng thất hứa.
4	～だけ	Đến mức, chỉ tới mức	できるだけ早く返事をください。	できるだけはやくへんじをください。	Hãy trả lời sớm hết mức có thể.
5	～に限り	Chỉ đối với, chỉ riêng	本日に限り、入場料が半額になります。	ほんじつにかぎり、にゅうじょうりょうがはんがくになります。	Chỉ hôm nay, phí vào cửa giảm một nửa.
5	～に限り(は)	Đến chừng nào thì còn	雨が降らない限り、試合は予定通り行われます。	あめがふらないかぎり、しあいはよていどおりおこなわれます。	Chừng nào trời không mưa, trận đấu sẽ diễn ra theo lịch.
5	～に限っては	Theo như tôi biết về riêng	今回の件に限っては、彼に責任はないと思う。	こんかいのけんにかぎっては、かれにせきにんはないとおもう。	Riêng vụ lần này, tôi nghĩ anh ấy không có trách nhiệm.
5	～に限って(P1)	Khác với mọi khi	忙しい日に限って、急な客が来る。	いそがしいひにかぎって、きゅうなきゃくがくる。	Đúng những ngày bận thì khách đột xuất lại đến.
5	～に限って(P2)	Đúng lúc, đúng vào	彼に限って、そんな失礼なことはしないはずだ。	かれにかぎって、そんなしつれいなことはしないはずだ。	Riêng anh ấy thì chắc chắn không làm chuyện thất lễ như vậy.
5	～に限って(P3)	Riêng, chỉ riêng	子どもに限って、この薬は使わないでください。	こどもにかぎって、このくすりはつかわないでください。	Riêng trẻ em thì xin đừng dùng thuốc này.
6	～限らず	Không chỉ, không giới hạn ở	休日に限らず、平日もこの店は混んでいる。	きゅうじつにかぎらず、へいじつもこのみせはこんでいる。	Không chỉ cuối tuần mà ngày thường cửa hàng này cũng đông.
6	～のみならず	Không chỉ, mà còn	彼は英語のみならず、中国語も話せる。	かれはえいごのみならず、ちゅうごくごもはなせる。	Anh ấy không chỉ nói được tiếng Anh mà còn nói được tiếng Trung.
6	～ばかりか	Không chỉ mà còn	彼は遅刻したばかりか、宿題も忘れた。	かれはちこくしたばかりか、しゅくだいもわすれた。	Anh ấy không chỉ đi muộn mà còn quên bài tập.
6	～はもとより	Dĩ nhiên, không nói cũng biết	この商品は若者はもとより、高齢者にも人気がある。	このしょうひんはわかものはもとより、こうれいしゃにもにんきがある。	Sản phẩm này được yêu thích không chỉ bởi giới trẻ mà cả người cao tuổi.
6	～上(に)	Hơn nữa, thêm vào đó	この部屋は広い上に、駅からも近い。	このへやはひろいうえに、えきからもちかい。	Căn phòng này rộng, hơn nữa còn gần ga.
7	～に関して／～に関する	Liên quan tới	この問題に関して、詳しい説明をお願いします。	このもんだいにかんして、くわしいせつめいをおねがいします。	Về vấn đề này, xin hãy giải thích chi tiết.
7	～をめぐって／～をめぐる	Xung quanh vấn đề	新しい計画をめぐって、意見が分かれている。	あたらしいけいかくをめぐって、いけんがわかれている。	Các ý kiến đang chia rẽ xoay quanh kế hoạch mới.
7	～にかけては	Riêng về mặt	料理にかけては、母にかなう人はいない。	りょうりにかけては、ははにかなうひとはいない。	Riêng về nấu ăn thì không ai bằng mẹ tôi.
7	～に対して／～に対する	Đối với	お客様に対して、失礼な言い方をしてはいけません。	おきゃくさまにたいして、しつれいないいかたをしてはいけません。	Không được nói năng thất lễ với khách hàng.
7	～にこたえて／～にこたえる	Đáp ứng	皆の期待にこたえて、彼は優勝した。	みんなのきたいにこたえて、かれはゆうしょうした。	Đáp lại kỳ vọng của mọi người, anh ấy đã vô địch.
8	～をもとに(して)	Dựa trên, căn cứ trên	実話をもとにして、この映画は作られた。	じつわをもとにして、このえいがはつくられた。	Bộ phim này được làm dựa trên câu chuyện có thật.
8	～に基づいて／～に基づく	Dựa vào, theo cơ sở	データに基づいて、計画を立て直した。	データにもとづいて、けいかくをたてなおした。	Chúng tôi lập lại kế hoạch dựa trên dữ liệu.
8	～に沿って／～に沿う	Theo, phù hợp với	会社の方針に沿って、予算を決めます。	かいしゃのほうしんにそって、よさんをきめます。	Chúng tôi quyết định ngân sách theo phương châm của công ty.
8	～のもとで／～のもとに	Dưới sự, trong điều kiện	先生の指導のもとで、研究を進めた。	せんせいのしどうのもとで、けんきゅうをすすめた。	Tôi tiến hành nghiên cứu dưới sự hướng dẫn của thầy.
8	～向けだ／～向けの	Dành cho	この雑誌は日本語を学ぶ外国人向けだ。	このざっしはにほんごをまなぶがいこくじんむけだ。	Tạp chí này dành cho người nước ngoài học tiếng Nhật.
9	～につれて／～にしたがって	Theo, càng thì càng	年を取るにつれて、健康の大切さが分かる。	としをとるにつれて、けんこうのたいせつさがわかる。	Càng lớn tuổi, tôi càng hiểu tầm quan trọng của sức khỏe.
9	～に伴って／～とともに	Kéo theo, cùng với	人口の増加に伴って、住宅も必要になった。	じんこうのぞうかにともなって、じゅうたくもひつようになった。	Dân số tăng kéo theo nhu cầu nhà ở.
9	～次第だ	Tùy thuộc vào	結果は君の努力次第だ。	けっかはきみのどりょくしだいだ。	Kết quả tùy thuộc vào nỗ lực của bạn.
9	～に応じて／～に応じた	Ứng với, tùy theo	経験に応じて、給料が決まります。	けいけんにおうじて、きゅうりょうがきまります。	Lương được quyết định tùy theo kinh nghiệm.
9	～につけて	Hễ mỗi lần là	この歌を聞くにつけて、故郷を思い出す。	このうたをきくにつけて、ふるさとをおもいだす。	Mỗi lần nghe bài hát này, tôi lại nhớ quê.
10	～やら…やら	Nào là, nào là	引っ越しの準備やら手続きやらで忙しい。	ひっこしのじゅんびやらてつづきやらでいそがしい。	Tôi bận nào là chuẩn bị chuyển nhà, nào là làm thủ tục.
10	～というか…というか	Có thể nói là, vừa như vừa như	彼の態度は親切というか、おせっかいというか、少し複雑だ。	かれのたいどはしんせつというか、おせっかいというか、すこしふくざつだ。	Thái độ của anh ấy có thể nói là tử tế, cũng có thể nói là hơi can thiệp.
10	～にしても…にしても	Cho dù là cái này hay cái kia	行くにしても行かないにしても、早く返事をください。	いくにしてもいかないにしても、はやくへんじをください。	Dù đi hay không đi, hãy trả lời sớm.
10	～といった	Như là, kiểu như	この店では、寿司や天ぷらといった日本料理が食べられる。	このみせでは、すしやてんぷらといったにほんりょうりがたべられる。	Ở cửa hàng này có thể ăn các món Nhật như sushi hay tempura.
11	～を問わず	Không kể, bất kể	このカードは年齢を問わず、誰でも使える。	このカードはねんれいをとわず、だれでもつかえる。	Thẻ này ai cũng dùng được, không kể tuổi tác.
11	～にかかわりなく／～にかかわらず	Bất chấp, bất kể	天気にかかわらず、試合は行われます。	てんきにかかわらず、しあいはおこなわれます。	Trận đấu sẽ diễn ra bất kể thời tiết.
11	～(の)もかまわず	Chẳng quan tâm đến	人目もかまわず、彼女は大声で泣いた。	ひとめもかまわず、かのじょはおおごえでないた。	Cô ấy khóc lớn mà chẳng để ý ánh mắt người khác.
11	～はともかく(として)	Khoan bàn đến, trước hết	値段はともかく、品質はとても良い。	ねだんはともかく、ひんしつはとてもよい。	Khoan nói đến giá, chất lượng thì rất tốt.
11	～はさておき	Gác sang một bên	冗談はさておき、本題に入りましょう。	じょうだんはさておき、ほんだいにはいりましょう。	Gác chuyện đùa sang một bên, chúng ta vào chủ đề chính.
12	～わけがない	Tuyệt đối không, nhất định không	こんな難しい問題が簡単に解けるわけがない。	こんなむずかしいもんだいがかんたんにとけるわけがない。	Một bài khó thế này không thể giải dễ dàng được.
12	～どころではない	Không chỉ mà còn hơn thế, không còn tâm trí	仕事が忙しくて、旅行どころではない。	しごとがいそがしくて、りょこうどころではない。	Công việc bận đến mức không còn tâm trí đi du lịch.
12	～どころか	Không những không mà còn	彼は謝るどころか、怒り出した。	かれはあやまるどころか、おこりだした。	Anh ấy không những không xin lỗi mà còn nổi giận.
12	～ものか	Làm gì có chuyện	二度と彼に頼むものか。	にどとかれにたのむものか。	Tôi sẽ không bao giờ nhờ anh ấy nữa.
12	～わけではない	Không hẳn là, không phải là	日本語が嫌いなわけではないが、漢字は苦手だ。	にほんごがきらいなわけではないが、かんじはにがてだ。	Không phải tôi ghét tiếng Nhật, nhưng tôi kém kanji.
12	～というものではない／～というものでもない	Không phải cứ là được	高ければよいというものではない。	たかければよいというものではない。	Không phải cứ đắt là tốt.
13	～とは	Định nghĩa là, nghĩa là	友情とは、困った時に助け合うことだ。	ゆうじょうとは、こまったときにたすけあうことだ。	Tình bạn là giúp đỡ nhau lúc khó khăn.
13	～といえば(1)	Nói đến thì	日本の食べ物といえば、寿司を思い出す。	にほんのたべものといえば、すしをおもいだす。	Nói đến đồ ăn Nhật thì tôi nhớ đến sushi.
13	～といえば(2)	Nếu nói thì	彼は優しいといえば優しいが、少し頼りない。	かれはやさしいといえばやさしいが、すこしたよりない。	Nói là anh ấy hiền thì đúng là hiền, nhưng hơi thiếu tin cậy.
13	～というと	Nhắc đến, nghĩ ngay tới	夏というと、海を思い出します。	なつというと、うみをおもいだします。	Nhắc đến mùa hè là tôi nhớ đến biển.
13	～(のこと)となると	Cứ nghĩ đến là, hễ nói về	仕事のこととなると、彼はとても真剣になる。	しごとのこととなると、かれはとてもしんけんになる。	Hễ nói đến công việc là anh ấy rất nghiêm túc.
13	～といったら	Nhắc đến thì, hơn mức thường	試験前の忙しさといったら、寝る時間もないほどだ。	しけんまえのいそがしさといったら、ねるじかんもないほどだ。	Nói đến sự bận rộn trước kỳ thi thì đến mức không có thời gian ngủ.
14	～にもかかわらず	Bất chấp, mặc dù	雨にもかかわらず、大勢の人が集まった。	あめにもかかわらず、おおぜいのひとがあつまった。	Mặc dù trời mưa, rất nhiều người đã tụ tập.
14	～ものの	Tuy nhưng	新しいパソコンを買ったものの、まだ使い方が分からない。	あたらしいパソコンをかったものの、まだつかいかたがわからない。	Tôi đã mua máy tính mới nhưng vẫn chưa biết cách dùng.
14	～とはいうものの	Tuy nói là nhưng	春とはいうものの、まだ寒い日が続いている。	はるとはいうものの、まださむいひがつづいている。	Tuy nói là mùa xuân nhưng những ngày lạnh vẫn tiếp tục.
14	～ながら(も)	Dù nhưng	彼は子どもながら、しっかりしている。	かれはこどもながら、しっかりしている。	Dù là trẻ con nhưng cậu ấy rất chững chạc.
14	～つつ(も)	Mặc dù nhưng	悪いと知りつつも、同じ失敗を繰り返した。	わるいとしりつつも、おなじしっぱいをくりかえした。	Dù biết là không tốt, tôi vẫn lặp lại lỗi cũ.
14	～といっても	Dù nói là thế chứ	料理ができるといっても、簡単なものだけです。	りょうりができるといっても、かんたんなものだけです。	Nói là biết nấu ăn chứ tôi chỉ làm được món đơn giản.
14	～からといって	Cho dù cũng không	日本に住んでいるからといって、日本語が完璧なわけではない。	にほんにすんでいるからといって、にほんごがかんぺきなわけではない。	Không phải cứ sống ở Nhật là tiếng Nhật hoàn hảo.
15	～としたら／～とすれば／～とすると	Giả định là, nếu vậy thì	もし明日雨だとしたら、試合は中止になる。	もしあしたあめだとしたら、しあいはちゅうしになる。	Nếu ngày mai mưa thì trận đấu sẽ bị hủy.
15	～となったら／～となれば／～となると	Nếu tình huống trở thành	海外で働くとなると、家族とも相談が必要だ。	かいがいではたらくとなると、かぞくともそうだんがひつようだ。	Nếu chuyện trở thành đi làm ở nước ngoài thì cần bàn với gia đình.
15	～ものなら	Nếu có thể thì	できるものなら、もう一度あの日に戻りたい。	できるものなら、もういちどあのひにもどりたい。	Nếu có thể, tôi muốn quay lại ngày hôm đó một lần nữa.
15	～(よ)うものなら	Nếu lỡ thì hậu quả	そんなことを言おうものなら、みんなに反対される。	そんなことをいおうものなら、みんなにはんたいされる。	Nếu lỡ nói chuyện đó thì sẽ bị mọi người phản đối.
15	～ないことには	Nếu chưa thì không	実際に会ってみないことには、彼の気持ちは分からない。	じっさいにあってみないことには、かれのきもちはわからない。	Nếu chưa gặp trực tiếp thì không thể hiểu cảm xúc của anh ấy.
15	～を抜きにしては	Nếu không có thì	先生の助けを抜きにしては、この研究は完成しなかった。	せんせいのたすけをぬきにしては、このけんきゅうはかんせいしなかった。	Nếu không có sự giúp đỡ của thầy, nghiên cứu này đã không hoàn thành.
16	～によって／～によっては	Vì, bằng, tùy theo	国によって、習慣が違います。	くにによって、しゅうかんがちがいます。	Tập quán khác nhau tùy từng nước.
16	～ものだから／～もので	Vì nên	昨日は熱があったものだから、会社を休みました。	きのうはねつがあったものだから、かいしゃをやすみました。	Vì hôm qua tôi bị sốt nên đã nghỉ làm.
16	～もの	Vì mà, dùng giải thích thân mật	だって忙しかったんだもの、連絡できなかったよ。	だっていそがしかったんだもの、れんらくできなかったよ。	Vì tôi bận quá nên đã không thể liên lạc.
16	～おかげだ／～おかげで	Nhờ có	先生のおかげで、試験に合格できました。	せんせいのおかげで、しけんにごうかくできました。	Nhờ thầy, tôi đã đỗ kỳ thi.
16	～せいだ／～せいで	Chỉ vì, do lỗi	寝不足のせいで、今日は集中できない。	ねぶそくのせいで、きょうはしゅうちゅうできない。	Do thiếu ngủ nên hôm nay tôi không thể tập trung.
16	～あまり	Vì quá mà	心配のあまり、眠れなかった。	しんぱいのあまり、ねむれなかった。	Vì quá lo lắng nên tôi không ngủ được.
16	～につき	Vì lý do, thông báo	工事中につき、この道は通れません。	こうじちゅうにつき、このみちはとおれません。	Do đang thi công nên không thể đi qua đường này.
17	～ことだし	Vả lại, cũng vì	雨もやんだことだし、そろそろ帰りましょう。	あめもやんだことだし、そろそろかえりましょう。	Mưa cũng tạnh rồi, chúng ta về thôi.
17	～のことだから	Vì là người đó nên chắc	真面目な彼のことだから、約束は守るだろう。	まじめなかれのことだから、やくそくはまもるだろう。	Vì là người nghiêm túc như anh ấy nên chắc sẽ giữ lời hứa.
17	～だけに	Chính vì	期待していただけに、失敗した時はとても残念だった。	きたいしていただけに、しっぱいしたときはとてもざんねんだった。	Chính vì đã kỳ vọng nên khi thất bại tôi rất tiếc.
17	～ばかりに	Chỉ vì mà	一言余計なことを言ったばかりに、友人を怒らせてしまった。	ひとことよけいなことをいったばかりに、ゆうじんをおこらせてしまった。	Chỉ vì nói thừa một câu mà tôi làm bạn nổi giận.
17	～からには／～以上(は)	Một khi đã thì	約束したからには、最後までやります。	やくそくしたからには、さいごまでやります。	Một khi đã hứa thì tôi sẽ làm đến cùng.
18	～がたい	Khó mà, không thể	彼の行動は理解しがたい。	かれのこうどうはりかいしがたい。	Hành động của anh ấy thật khó hiểu.
18	～わけにはいかない	Không thể làm vì lý do xã hội	大事な会議なので、休むわけにはいかない。	だいじなかいぎなので、やすむわけにはいかない。	Vì là cuộc họp quan trọng nên tôi không thể nghỉ.
18	～わけにもいかない	Không thể nào cứ	親に心配をかけるわけにもいかない。	おやにしんぱいをかけるわけにもいかない。	Tôi cũng không thể để cha mẹ lo lắng.
18	～かねる	Khó mà, không thể	そのご依頼にはお答えしかねます。	そのごいらいにはおこたえしかねます。	Chúng tôi khó có thể đáp ứng yêu cầu đó.
18	～ようがない	Không có cách nào	住所が分からないので、連絡しようがない。	じゅうしょがわからないので、れんらくしようがない。	Vì không biết địa chỉ nên không có cách nào liên lạc.
18	～得る／～得ない	Có thể, không thể có khả năng	誰にでも起こり得る問題です。	だれにでもおこりうるもんだいです。	Đây là vấn đề có thể xảy ra với bất kỳ ai.
19	～わりには	So với thì tương đối	彼は若いわりには、考え方がしっかりしている。	かれはわかいわりには、かんがえかたがしっかりしている。	So với tuổi còn trẻ, cách nghĩ của anh ấy rất chín chắn.
19	～にしては	Tuy là vậy mà	初めてにしては、上手にできました。	はじめてにしては、じょうずにできました。	Tuy là lần đầu nhưng bạn làm rất tốt.
19	～だけ(のことは)ある	Quả đúng là, đáng công	高いだけのことはあって、このカメラは性能がいい。	たかいだけのことはあって、このカメラはせいのうがいい。	Quả đúng là đắt, chiếc máy ảnh này có hiệu năng tốt.
19	～として	Với tư cách là	教師として、学生の成長を支えたい。	きょうしとして、がくせいのせいちょうをささえたい。	Với tư cách giáo viên, tôi muốn hỗ trợ sự trưởng thành của học sinh.
19	～にとって	Đối với	私にとって、家族は一番大切です。	わたしにとって、かぞくはいちばんたいせつです。	Đối với tôi, gia đình là quan trọng nhất.
19	～にしたら／～にすれば／～にしても	Đối với lập trường của	親にしたら、子どもの安全が一番心配だ。	おやにしたら、こどものあんぜんがいちばんしんぱいだ。	Đối với cha mẹ, an toàn của con là điều lo nhất.
20	～ところ	Khi thì kết quả	先生に相談したところ、すぐ返事をくれた。	せんせいにそうだんしたところ、すぐへんじをくれた。	Khi tôi hỏi thầy thì thầy trả lời ngay.
20	～きり	Cứ mãi không, sau khi rồi	彼は出て行ったきり、帰ってこない。	かれはでていったきり、かえってこない。	Anh ấy ra đi rồi không quay lại nữa.
20	～あげく	Sau cùng sau nhiều việc	長く迷ったあげく、留学することにした。	ながくまよったあげく、りゅうがくすることにした。	Sau khi phân vân lâu, tôi quyết định đi du học.
20	～末に	Sau cùng, sau quá trình	何度も話し合った末に、計画を変更した。	なんどもはなしあったすえに、けいかくをへんこうした。	Sau nhiều lần bàn bạc, chúng tôi đã đổi kế hoạch.
20	～ところだった	Suýt nữa, sắp đúng lúc	もう少しで電車に乗り遅れるところだった。	もうすこしででんしゃにのりおくれるところだった。	Chút nữa là tôi lỡ tàu.
20	～ずじまいだ	Cuối cùng vẫn không	忙しくて、友達に会えずじまいだった。	いそがしくて、ともだちにあえずじまいだった。	Vì bận nên cuối cùng tôi vẫn không gặp được bạn.
21	～くらい／～ぐらい	Cỡ như, chỉ mới	このくらいの荷物なら、一人で運べます。	このくらいのにもつなら、ひとりではこべます。	Hành lý cỡ này thì một mình tôi mang được.
21	～など	Chẳng hạn như, coi nhẹ	忙しくて、昼ご飯など食べる時間がなかった。	いそがしくて、ひるごはんなどたべるじかんがなかった。	Bận đến mức không có thời gian ăn trưa gì cả.
21	～なんか	Chẳng hạn như, coi nhẹ	失敗なんか気にしないで、もう一度やってみよう。	しっぱいなんかきにしないで、もういちどやってみよう。	Đừng bận tâm thất bại gì cả, hãy thử lại lần nữa.
21	～なんて	Chẳng hạn như, cảm thán	一人で全部やるなんて、無理です。	ひとりでぜんぶやるなんて、むりです。	Tự làm hết một mình thì không thể được.
21	～まで／～までして	Thậm chí đến mức	借金までして、そんな高い物を買う必要はない。	しゃっきんまでして、そんなたかいものをかうひつようはない。	Không cần đến mức vay nợ để mua thứ đắt như vậy.
21	～として～ない	Không một, dù chỉ	彼は一度として約束を破ったことがない。	かれはいちどとしてやくそくをやぶったことがない。	Anh ấy chưa từng thất hứa dù chỉ một lần.
21	～さえ(1)	Ngay cả, đến cả	忙しくて、食事をする時間さえなかった。	いそがしくて、しょくじをするじかんさえなかった。	Tôi bận đến mức không có cả thời gian ăn.
21	～さえ(2)	Chỉ cần là	名前さえ分かれば、すぐに調べられます。	なまえさえわかれば、すぐにしらべられます。	Chỉ cần biết tên là có thể tra ngay.
21	～でも	Cho dù, ngay cả	子どもでも分かる説明にしてください。	こどもでもわかるせつめいにしてください。	Hãy giải thích sao cho ngay cả trẻ con cũng hiểu.
22	～とみえる	Dường như	窓がぬれている。夜中に雨が降ったとみえる。	まどがぬれている。よなかにあめがふったとみえる。	Cửa sổ ướt. Có vẻ đêm qua trời đã mưa.
22	～かねない	Có thể sẽ xảy ra điều xấu	このままでは、大きな事故が起こりかねない。	このままでは、おおきなじこがおこりかねない。	Cứ thế này có thể xảy ra tai nạn lớn.
22	～おそれがある	Có nguy cơ, e rằng	明日は大雨になるおそれがある。	あしたはおおあめになるおそれがある。	Ngày mai có nguy cơ mưa lớn.
22	～まい	Chắc là không, sẽ không	彼はもう二度と来るまい。	かれはもうにどとくるまい。	Chắc anh ấy sẽ không đến lần nào nữa.
22	～ではあるまいか	Chẳng phải là sao	これは重要な問題ではあるまいか。	これはじゅうようなもんだいではあるまいか。	Chẳng phải đây là vấn đề quan trọng hay sao.
22	～に違いない／～に相違ない	Chắc chắn là	あの人は犯人に違いない。	あのひとははんにんにちがいない。	Người đó chắc chắn là thủ phạm.
22	～にきまっている	Nhất định là	彼なら試験に合格するにきまっている。	かれならしけんにごうかくするにきまっている。	Nếu là anh ấy thì nhất định sẽ đỗ kỳ thi.
23	～ものだ	Vốn là, bản chất là	人は誰でも失敗するものだ。	ひとはだれでもしっぱいするものだ。	Con người ai cũng có lúc thất bại.
23	～というものだ	Chính là, đúng là	努力せずに成功したいなんて、わがままというものだ。	どりょくせずにせいこうしたいなんて、わがままというものだ。	Muốn thành công mà không nỗ lực thì đúng là ích kỷ.
23	～にすぎない	Chẳng qua chỉ là	これは個人的な意見にすぎません。	これはこじんてきないけんにすぎません。	Đây chẳng qua chỉ là ý kiến cá nhân.
23	～にほかならない	Chính là, không gì khác hơn	成功の理由は努力にほかならない。	せいこうのりゆうはどりょくにほかならない。	Lý do thành công không gì khác ngoài nỗ lực.
23	～に越したことはない	Tốt nhất là	準備は早いに越したことはない。	じゅんびははやいにこしたことはない。	Chuẩn bị càng sớm càng tốt.
23	～しかない／～よりほかない	Chỉ còn cách là	電車が止まったので、歩くしかない。	でんしゃがとまったので、あるくしかない。	Vì tàu dừng nên chỉ còn cách đi bộ.
23	～べきだ／～べきではない	Nên, không nên	約束は守るべきだ。	やくそくはまもるべきだ。	Nên giữ lời hứa.
24	～ではないか	Hãy cùng, đề nghị mạnh	環境を守るために、今できることを考えようではないか。	かんきょうをまもるために、いまできることをかんがえようではないか。	Chúng ta hãy cùng nghĩ xem bây giờ có thể làm gì để bảo vệ môi trường.
24	～ことだ	Phải, nên, đừng	健康になりたいなら、毎日運動することだ。	けんこうになりたいなら、まいにちうんどうすることだ。	Nếu muốn khỏe mạnh thì nên vận động mỗi ngày.
24	～ものだ	Nên, không nên, lẽ thường	年上の人には丁寧に話すものだ。	としうえのひとにはていねいにはなすものだ。	Với người lớn tuổi thì nên nói chuyện lịch sự.
24	～ものではない	Không nên, không được làm	人の悪口を言うものではない。	ひとのわるぐちをいうものではない。	Không nên nói xấu người khác.
24	～ことはない	Không cần phải	そんなに心配することはない。	そんなにしんぱいすることはない。	Không cần lo lắng đến thế.
24	～ものか	Nhất định không	あんな店には二度と行くものか。	あんなみせにはにどといくものか。	Tôi nhất định không đến cửa hàng như thế lần nữa.
25	～しかたがない／～しょうがない	Không chịu nổi, vô cùng	この映画は面白くてしかたがない。	このえいがはおもしろくてしかたがない。	Bộ phim này thú vị không chịu nổi.
25	～たまらない	Không chịu nổi	試験の結果が心配でたまらない。	しけんのけっかがしんぱいでたまらない。	Tôi lo kết quả kỳ thi không chịu nổi.
25	～ならない	Vô cùng, không thể kìm	国の家族が思い出されてならない。	くにのかぞくがおもいだされてならない。	Tôi không thể ngừng nhớ gia đình ở quê.
25	～てはいられない／～ずにはいられない	Không thể cứ, không thể không	明日試験だから、遊んではいられない。	あしたしけんだから、あそんではいられない。	Vì mai thi nên không thể cứ chơi được.
25	～ざるを得ない	Đành phải, buộc phải	雨が強くなったので、予定を変更せざるを得ない。	あめがつよくなったので、よていをへんこうせざるをえない。	Vì mưa to hơn nên chúng tôi buộc phải đổi kế hoạch.
26	～たいものだ／～ほしいものだ	Thật rất muốn, ước gì	いつか富士山に登りたいものだ。	いつかふじさんにのぼりたいものだ。	Tôi thật sự muốn một ngày nào đó leo núi Phú Sĩ.
26	～ものだ(1)	Thường hay, hồi tưởng	子どもの頃、よくこの川で泳いだものだ。	こどものころ、よくこのかわでおよいだものだ。	Hồi nhỏ tôi thường bơi ở con sông này.
26	～ものだ(2)	Làm sao mà, biết bao	時間が過ぎるのは早いものだ。	じかんがすぎるのははやいものだ。	Thời gian trôi qua thật nhanh biết bao.
26	～もの(だろう)か	Phải chi, có thể nào	どうしたら彼に気持ちを伝えられるものだろうか。	どうしたらかれにきもちをつたえられるものだろうか。	Không biết làm sao để truyền đạt cảm xúc với anh ấy.
26	～ものがある	Cảm thấy, có điều gì đó	彼の話には人を引きつけるものがある。	かれのはなしにはひとをひきつけるものがある。	Câu chuyện của anh ấy có sức hút người nghe.
26	～ことだ	Thật là, làm sao mà	一人でここまで来たとは、立派なことだ。	ひとりでここまできたとは、りっぱなことだ。	Một mình đi được đến đây thật là đáng nể.
26	～ことか／～ことだろう	Tới cỡ nào, biết bao	合格の知らせを聞いて、どんなにうれしかったことか。	ごうかくのしらせをきいて、どんなにうれしかったことか。	Khi nghe tin đỗ, tôi đã vui biết bao.
"""


def sql_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "''") + "'"


def insert_rows(table: str, columns: list[str], rows: list[dict], update_columns: list[str]) -> str:
    values = ",\n".join(
        "(" + ", ".join(sql_value(row.get(column)) for column in columns) + ")" for row in rows
    )
    updates = ",\n    ".join(f"{column} = VALUES({column})" for column in update_columns)
    return (
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES\n"
        f"{values}\n"
        f"ON DUPLICATE KEY UPDATE\n    {updates};"
    )


def parse_rows() -> list[dict]:
    rows = []
    for line_number, line in enumerate(RAW_DATA.strip().splitlines(), start=1):
        parts = line.split("\t")
        if len(parts) != 6:
            raise ValueError(f"Invalid N2 row {line_number}: expected 6 columns, got {len(parts)}")
        chapter, pattern, meaning_vi, japanese_text, reading, example_meaning_vi = parts
        rows.append(
            {
                "chapter_number": int(chapter),
                "pattern": pattern.strip(),
                "meaning_vi": meaning_vi.strip(),
                "japanese_text": japanese_text.strip(),
                "reading": reading.strip(),
                "example_meaning_vi": example_meaning_vi.strip(),
            }
        )
    return rows


def build_data() -> dict:
    source_exists = SOURCE_PDF.exists()
    rows = parse_rows()
    chapter_numbers = sorted({row["chapter_number"] for row in rows})

    grammar_chapters = []
    grammar_lessons = []
    grammar_examples = []

    lesson_id = GRAMMAR_LESSON_START_ID
    example_id = GRAMMAR_EXAMPLE_START_ID

    for display_order, chapter_number in enumerate(chapter_numbers, start=1):
        chapter_rows = [row for row in rows if row["chapter_number"] == chapter_number]
        chapter_id = GRAMMAR_CHAPTER_START_ID + chapter_number - 1
        first = lesson_id
        last = lesson_id + len(chapter_rows) - 1
        grammar_chapters.append(
            {
                "id": chapter_id,
                "jlpt_level_id": JLPT_LEVEL_ID,
                "chapter_number": chapter_number,
                "name": f"Bài {chapter_number}",
                "description": f"Ngữ pháp N2 - Bài {chapter_number} ({len(chapter_rows)} mẫu, lesson {first}-{last})",
                "display_order": display_order,
                "is_published": True,
                "version": 1,
            }
        )

        for order_in_chapter, row in enumerate(chapter_rows, start=1):
            title = f"Bài {chapter_number}.{order_in_chapter} - {row['pattern']}"
            grammar_lessons.append(
                {
                    "id": lesson_id,
                    "grammar_chapter_id": chapter_id,
                    "title": title[:255],
                    "pattern": row["pattern"],
                    "meaning_vi": row["meaning_vi"],
                    "explanation": (
                        f"Dùng để diễn đạt ý '{row['meaning_vi']}'. "
                        "Khi dùng trong câu, hãy chú ý thể đứng trước mẫu và sắc thái trang trọng/thân mật theo ngữ cảnh."
                    ),
                    "formation": row["pattern"],
                    "jlpt_level_id": JLPT_LEVEL_ID,
                    "display_order": order_in_chapter,
                    "is_published": True,
                    "version": 1,
                }
            )
            grammar_examples.append(
                {
                    "id": example_id,
                    "grammar_lesson_id": lesson_id,
                    "japanese_text": row["japanese_text"],
                    "reading": row["reading"],
                    "meaning_vi": row["example_meaning_vi"],
                    "display_order": 1,
                }
            )
            lesson_id += 1
            example_id += 1

    return {
        "metadata": {
            "name": "JLPT N2 grammar import data by chapters",
            "source_file": str(SOURCE_PDF),
            "source_file_exists": source_exists,
            "jlpt_level_id_assumption": JLPT_LEVEL_ID,
            "generated_from": "image-only PDF rendered to contact sheets and normalized manually",
            "import_order": ["grammar_chapters", "grammar_lessons", "grammar_examples"],
            "notes": [
                "The source PDF has no selectable text layer, so lessons were transcribed from rendered page images.",
                "The PDF is organized as Bài số 1-26; these are mapped directly to grammar_chapters.",
                "Each lesson includes one complete Japanese example, kana reading, and Vietnamese meaning for import.",
            ],
        },
        "grammar_chapters": grammar_chapters,
        "grammar_lessons": grammar_lessons,
        "grammar_examples": grammar_examples,
    }


def main() -> None:
    data = build_data()
    OUTPUT_JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    chapter_columns = [
        "id",
        "jlpt_level_id",
        "chapter_number",
        "name",
        "description",
        "display_order",
        "is_published",
        "version",
    ]
    lesson_columns = [
        "id",
        "grammar_chapter_id",
        "title",
        "pattern",
        "meaning_vi",
        "explanation",
        "formation",
        "jlpt_level_id",
        "display_order",
        "is_published",
        "version",
    ]
    example_columns = [
        "id",
        "grammar_lesson_id",
        "japanese_text",
        "reading",
        "meaning_vi",
        "display_order",
    ]

    sql_parts = [
        "SET NAMES utf8mb4;",
        (
            "DELETE ge FROM grammar_examples ge "
            "JOIN grammar_lessons gl ON gl.id = ge.grammar_lesson_id "
            f"WHERE gl.jlpt_level_id = {JLPT_LEVEL_ID};"
        ),
        f"DELETE FROM grammar_lessons WHERE jlpt_level_id = {JLPT_LEVEL_ID};",
        f"DELETE FROM grammar_chapters WHERE jlpt_level_id = {JLPT_LEVEL_ID};",
        insert_rows(
            "grammar_chapters",
            chapter_columns,
            data["grammar_chapters"],
            ["jlpt_level_id", "chapter_number", "name", "description", "display_order", "is_published", "version"],
        ),
        insert_rows(
            "grammar_lessons",
            lesson_columns,
            data["grammar_lessons"],
            [
                "grammar_chapter_id",
                "title",
                "pattern",
                "meaning_vi",
                "explanation",
                "formation",
                "jlpt_level_id",
                "display_order",
                "is_published",
                "version",
            ],
        ),
        insert_rows(
            "grammar_examples",
            example_columns,
            data["grammar_examples"],
            ["grammar_lesson_id", "japanese_text", "reading", "meaning_vi", "display_order"],
        ),
    ]
    OUTPUT_SQL_PATH.write_text("\n\n".join(sql_parts) + "\n", encoding="utf-8")

    print(f"created {OUTPUT_JSON_PATH}")
    print(f"created {OUTPUT_SQL_PATH}")
    print(
        f"{len(data['grammar_chapters'])} grammar chapters, "
        f"{len(data['grammar_lessons'])} grammar lessons, "
        f"{len(data['grammar_examples'])} grammar examples"
    )
    for chapter in data["grammar_chapters"]:
        count = sum(
            1 for lesson in data["grammar_lessons"] if lesson["grammar_chapter_id"] == chapter["id"]
        )
        print(f"{chapter['name']}: {count} lessons")


if __name__ == "__main__":
    main()
