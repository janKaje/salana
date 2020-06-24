import discord
from discord.ext import commands
import re
import emoji
import string
import time
import math
    
def setup(client):
    client.add_cog(language(client))

tp_words = {
    '',
    'a', 'あ',
    'kin', 'きん',
    'akesi', 'あけし',
    'ala', 'あら',
    'alasa', 'あらさ',
    'ale', 'あれ',
    'ali', 'あり',
    'anpa', 'あんぱ',
    'ante', 'あんて',
    'anu', 'あぬ',
    'awen', 'あうぇん',
    'e', 'え',
    'en', 'えん',
    'esun', 'えすん',
    'ijo', 'いよ',
    'ike', 'いけ',
    'ilo', 'いろ',
    'insa', 'いんさ',
    'jaki', 'やき',
    'jan', 'やん',
    'jelo', 'いぇろ',
    'jo', 'よ',
    'kala', 'から',
    'kalama', 'からま',
    'kama', 'かま',
    'kasi', 'かし',
    'ken', 'けん',
    'kepeken', 'けぺけん',
    'kili', 'きり',
    'kiwen', 'きうぇん',
    'ko', 'こ',
    'kon', 'こん',
    'kule', 'くれ',
    'kulupu', 'くるぷ',
    'kute', 'くて',
    'la', 'ら',
    'lape', 'らぺ',
    'laso', 'らそ',
    'lawa', 'らわ',
    'len', 'れん',
    'lete', 'れて',
    'li', 'り',
    'lili', 'りり',
    'linja', 'りんや',
    'lipu', 'りぷ',
    'loje', 'ろいえ',
    'lon', 'ろん',
    'luka', 'るか',
    'lukin', 'るきん',
    'oko', 'おこ',
    'lupa', 'るぱ',
    'ma', 'ま',
    'mama', 'まま',
    'mani', 'まに',
    'meli', 'めり',
    'mi', 'み',
    'mije', 'みいぇ',
    'moku', 'もく',
    'moli', 'もり',
    'monsi', 'もんし',
    'mu', 'む',
    'mun', 'むん',
    'musi', 'むし',
    'mute', 'むて',
    'nanpa', 'なんぱ',
    'nasa', 'なさ',
    'nasin', 'なしん',
    'nena', 'ねな',
    'ni', 'に',
    'nimi', 'にみ',
    'noka', 'のか',
    'o', 'お',
    'olin', 'おりん',
    'ona', 'おな',
    'open', 'おぺん',
    'pakala', 'ぱから',
    'pali', 'ぱり',
    'palisa', 'ぱりさ',
    'pan', 'ぱん',
    'pana', 'ぱな',
    'pi', 'ぴ',
    'pilin', 'ぴりん',
    'pimeja', 'ぴめや',
    'pini', 'ぴに',
    'pipi', 'ぴぴ',
    'poka', 'ぽか',
    'poki', 'ぽき',
    'pona', 'ぽな',
    'pu', 'ぷ',
    'sama', 'さま',
    'seli', 'せり',
    'selo', 'せろ',
    'seme', 'せめ',
    'sewi', 'せうぃ',
    'sijelo', 'しいぇろ',
    'sike', 'しけ',
    'sin', 'しん',
    'namako', 'なまこ',
    'sina', 'しな',
    'sinpin', 'しんぴん',
    'sitelen', 'してれん',
    'sona', 'そな',
    'soweli', 'そうぇり',
    'suli', 'すり',
    'suno', 'すの',
    'supa', 'すぱ',
    'suwi', 'すうぃ',
    'tan', 'たん',
    'taso', 'たそ',
    'tawa', 'たわ',
    'telo', 'てろ',
    'tenpo', 'てんぽ',
    'toki', 'とき',
    'tomo', 'とも',
    'tu', 'つ',
    'unpa', 'うんぱ',
    'uta', 'うた',
    'utala', 'うたら',
    'walo', 'わろ',
    'wan', 'わん',
    'waso', 'わそ',
    'wawa', 'わわ',
    'weka', 'うぇか',
    'wile', 'うぃれ',
    'monsuta', 'もんすた',
    'kipisi', 'きぴし',
    'kijetesantakalu', 'きいぇてさんたかる',
    'tonsi', 'とんし',
    'leko', 'れこ',
    'apeja', 'あぺや',
    'majuna', 'まゆな',
    'pake', 'ぱけ',
    'mulapisu', 'むらぴす',
    'powe', 'ぽうぇ',
    'linluwi', 'りんるうぃ',
    'epiku', 'えぴく',
    'yupekosi', 'ゆぺこし',
    'lanpan', 'らんぱん',
    'pata', 'ぱた',
    'wuwojiti', 'うをいち',
    'tuli', 'つり',
    'po', 'ぽ',
    'kan', 'かん',
    'iki', 'いき',
    'kapa', 'かぱ',
    'kapesi', 'かぺし',
    'misikeke', 'みしけけ',
    'pasila', 'ぱしら',
    'alu', 'ある',
    'ete', 'えて',
    'ewe', 'えうぇ',
    'ini', 'いに',
    'jaku', 'やく',
    'jami', 'やみ',
    'jasima', 'やしま',
    'jatu', 'やつ',
    'kajo', 'かよ',
    'kamalawala', 'かまらわら',
    'ke', 'け',
    'kulu', 'くる',
    'kuntu', 'くんつ',
    'lenke', 'れんけ',
    'likujo', 'りくよ',
    'loku', 'ろく',
    'melome', 'めろめ',
    'mijomi', 'みよみ',
    'neja', 'ねや',
    'nun', 'ぬん',
    'oke', 'おけ',
    'patu', 'ぱつ',
    'peto', 'ぺと',
    'peta', 'ぺた',
    'san', 'さん',
    'se', 'せ',
    'soko', 'そこ',
    'soto', 'そと',
    'take', 'たけ',
    'te', 'て',
    'ten', 'てん',
    'we', 'うぇ',
    'ipi', 'いぴ',
    'jalan', 'やらん',
    'epiku', 'えぴく',
    'itomi', 'いとみ',
    'jans', 'やんす',
    'lokon', 'ろこん',
    'nu', 'ぬ',
    'nuwa', 'ぬわ',
    'okepuma', 'おけぷま',
    'omen', 'おめん',
    'pa', 'ぱ',
    'pipo', 'ぴぽ',
    'polinpin', 'ぽりんぴん',
    'pomotolo', 'ぽもとろ',
    'samu', 'さむ',
    'sikomo', 'しこも',
    'slape', 'すらぺ',
    'su', 'す',
    'wawajete', 'わわいぇて',
    'wi', 'うぃ',
    'waleja', 'われや'
}

tp_dict = {
    'a': '***a*** – *~pu~* (emphasis, emotion or confirmation) {see ***kin***}\n\t←? onomatopoeia',
    'akesi': '***akesi*** – *~pu~* non-cute animal; reptile, amphibian\n\t← Dutch *hagedis* ‘lizard’',
    'ala': '***ala*** – *~pu~* no, not, zero; [~ *ala* ~] (used to form a yes-no question)\n\t← Georgian არა *ara* ‘no’',
    'alasa': '***alasa*** – *~pu~* to hunt, forage | *~alt. usage~* (pv.) try to {see ***lukin***}\n\t← Acadian French *à la chasse* ‘hunting’ ← French *chasser* ‘to hunt’',
    'ale': '***ale*** – *~pu~* all; abundant, countless, bountiful, every, plentiful; abundance, everything, life, universe; one hundred | *~alt. usage~* twenty; 100; 120\n\t← Dutch *alle* ‘all’',
    'ali': '***ali*** – *~pu~* all; abundant, countless, bountiful, every, plentiful; abundance, everything, life, universe; one hundred | *~alt. usage~* twenty; 100; 120\n\t← Dutch *alle* ‘all’',
    'alu': r'***alu*** – *~post-pu~* (between the main sentence and the context phrase) {see ***la***}\n\t← toki pona \**al* (*la* reversed)',
    'anpa': '***anpa*** – *~pu~* bowing down, downward, humble, lowly, dependent\n\t← Acadian French *en bas* ‘below’',
    'ante': '***ante*** – *~pu~* different, altered changed, other\n\t← Dutch *ander* ‘other, different’',
    'anu': '***anu*** – *~pu~* or | *~alt. usage~* choose, decide\n\t← Georgian ან *an* ‘or’',
    'apeja': '***apeja*** – *~pre-pu~* shame, guilt\n\t←? Finnish *häpeä* ‘shame, disgrace, dishonor’',
    'awen': '***awen*** – *~pu~* enduring, kept, protected, safe, waiting, staying; (pv.) to continue to\n\t← Dutch *houden* ‘keep, care for, hold (in a particular state)’',
    'e': '***e*** – *~pu~* (before the direct object)\n\t←?',
    'en': '***en*** – *~pu~* (between multiple subjects) | *~alt. usage~* (coordinates modifiers in a *pi*-phrase)\n\t← Dutch *en* ‘and’',
    'epiku': '***epiku*** – *~post-pu, humorous~* {see ***sikomo***}\n\t← English *epic*',
    'esun': '***esun*** – *~pu~* market, shop, fair, bazaar, business transaction\n\t←? of Akan origin',
    'ete': '***ete*** – *~post-pu~* beyond, exceeding, outside of, more than {see ***selo***, ***weka***}\n\t← Turkish *öte* ‘beyond, further, over’',
    'ewe': '***ewe*** – *~post-pu~* stone, gravel, rock, pebble, lava, magma (when used, *kiwen* is limited to ‘metal, hardness’ {see ***kiwen***}\n\t← ?',
    'ijo': '***ijo*** – *~pu~* thing, phenomenon, object, matter\n\t← Esperanto io ‘something’ ← Romance i- ‘(relative pronoun root)’',
    'ike': '***ike*** – *~pu~* bad, negative; non-essential, irrelevant | *~alt. usage~* complicated, complex\n\t← Finnish *ilkeä* ‘bad, mean, wicked’',
    'iki': '***iki*** – *~pre-pu~* {see ***ona***}\n\t←?',
    'ilo': '***ilo*** – *~pu~* tool, implement, machine, device\n\t← Esperanto *ilo* ‘tool’ ← German -*el* ‘(agent suffix)’ {cf. *Schlüssel* ‘key’ ~*schließen* ‘lock, shut’)',
    'ini': '***ini*** – *~post-pu~* the digit ‘2’\n\t← Cantonese 二/貳 *yih* ‘two’',
    'insa': '***insa*** – *~pu~* centre, content, inside, between; internal organ, stomach\n\t← Tok Pisin *insait* ‘inside, center, stomach’ ← English *inside*',
    'ipi': '***ipi*** – *~pre-pu, prop.~* (presented as an early alternative to ***iki***) {see ***ona***}\n\t←?',
    'itomi': '***itomi*** – *~post-pu, humorous~* Schadenfreude, indirect insult or disrespect, shade\n\t← English *hit or miss* (from the song ‘Mia Khalifa’ by iLOVEFRiDay)',
    'jaki': '***jaki*** – *~pu~* disgusting, obscene, sickly, toxic, unclean, unsanitary\n\t← English *yucky*',
    'jaku': '***jaku*** – *~post-pu~* 100 {see ***ale*** and ***ali***}\n\t← Japanese 百 *hyaku* \'100\'',
    'jalan': '***jalan*** – *~pre-pu, prop.~* foot {see ***noka***}\n\t←Finnish *jalan* ‘afoot’ (← *jalka* ‘foot’)',
    'jami': '***jami*** – *~post-pu~* eliciting a positive sensory or stimulating experience {see ***suwi***}\n\t← English *yummy*',
    'jan': '***jan*** – *~pu~* human being, person, somebody\n\t← Cantonese 人 *jan* ‘person’',
    'jans': '***jans*** – *~post-pu, humorous~* a particular group of early members of the ma pona Discord\n\t← toki pona *jan* and English -*/z/* ‘[plural]’',
    'jasima': '***jasima*** – *~post-pu~* reflect, resound, mirror, be on the opposite/polar end of\n\t← Turkish *yansıtmak* ‘to reflect, reverberate’',
    'jatu': '***jatu*** – *~post-pu~* the digit ‘1’\n\t← Cantonese 一/壹 *yāt* ‘one’',
    'jelo': '***jelo*** – *~pu~* yellow, yellowish\n\t← English *yellow*',
    'jo': '***jo*** – *~pu~* to have, carry, contain, hold {see ***lon***, ***poki***, ***lanpan***}\n\t← Mandarin 有 *yǒu* ‘have’',
    'kajo': '***kajo*** – *~post-pu~* the digit ‘9’\n\t← Cantonese 九 / 玖 *gáu* ‘nine’',
    'kala': '***kala*** – *~pu~* fish, marine animal, sea creature\n\t← Finnish *kala* ‘fish’',
    'kalama': '***kalama*** – *~pu~* to produce a sound; recite, utter aloud\n\t← Serbo-Croatian *галама galama* ‘fuss, noise’',
    'kama': '***kama*** – *~pu~* arriving, coming, future, summoned; (pv.) to become, manage to, succeed in\n\t← Tok Pisin *kamap* ‘event, arrive, happen, become, bring about, summon’ ← English *come up*',
    'kamalawala': '***kamalawala*** – *~post-pu~* anarchy, uprising, revolt, rebellion\n\t← toki pona *‘kama pi lawa ala’*',
    'kan': '***kan*** – *~pre-pu~* with, among {see ***poka***}\n\t← ?Finnish *kanssa* ‘with’ or Esperanto *kun* ‘with’ (← Latin *cum*)',
    'kapa': '***kapa*** – *~pre-pu~* extrusion, protrusion, hill, mountain, button {see ***nena***}\n\t← ?Dutch *kop* ‘head, cup’ or Esperanto *kapo* ‘head’ (← Latin *caput*)',
    'kapesi': '***kapesi*** – *~pre-pu~* brown, gray\n\t← Greek *καφές kafés* ‘coffee’ or ?French *café* ‘light brown’',
    'kasi': '***kasi*** – *~pu~* plant, vegetation; herb, leaf\n\t← Finnish *kasvi* ‘plant’',
    'ke': '***ke*** – *~post-pu~* (acknowledgment or acceptance) {see ***oke***}\n\t← English *’kay* ← *okay*',
    'ken': '***ken*** – *~pu~* (pv.) to be able to, be allowed to, can, may; possible\n\t← Tok Pisin *ken* ← English *can*',
    'kepeken': '***kepeken*** – *~pu~* to use, with, by means of\n\t← Dutch *gebruiken* ‘to use’',
    'kijetesantakalu': '***kijetesantakalu*** – *~pre-pu, humorous, w.o.g. Sonja~* any animal from the Procyonidae family, such as raccoons, coatis, kinkajous, olingos, ringtails and cacomistles\n\t← Finnish *kierteishäntäkarhu* ‘kinkajou’ ← *kierteis* ‘spiral’ + *häntä* ‘tail’ + *karhu* ‘bear’',
    'kili': '***kili*** – *~pu~* fruit, vegetable, mushroom\n\t← Georgian ხილი *xili* ‘fruit’',
    'kin': '***kin*** – *~pu~* {see ***a***} | *~pre-pu, alt. usage~* too, also, as well\n\t← Finnish -*kin* ‘too, also, still’',
    'kipisi': '***kipisi*** – *~pre-pu~* split, cut, slice {see ***tu***}\n\t← Iñupiat *kipriruk* ‘cut’ or Swahili *kipisi* ‘sliver, small piece of wood’',
    'kiwen': '***kiwen*** – *~pu~* hard object, metal, rock, stone\n\t← Finnish *kiven*, genitive of *kivi* ‘stone’',
    'ko': '***ko*** – *~pu~* clay, clinging form, dough, semi-solid, paste, powder\n\t← Cantonese 膏 *gou* ‘cream, paste’',
    'kon': '***kon*** – *~pu~* air, breath; essence, spirit; hidden reality, unseen agent\n\t← Mandarin 空氣 *kōngqì* ‘air, atmosphere, ambience, opinion’',
    'kule': '***kule*** – *~pu~* colourful, pigmented, painted | *~alt. usage~* of or relating to the LGBT+ community\n\t← Acadian French *couleur* ‘color’',
    'kulu': '***kulu*** – *~post-pu~* {shortened variant of ***kulupu***}; six {particularly in senary base}\n\t← toki pona *kulupu*',
    'kulupu': '***kulupu*** – *~pu~* community, company, group, nation, society, tribe\n\t← Tongan *kulupu* ← English *group*',
    'kuntu': '***kuntu*** – *~post-pu~* laughter, humor {see ***musi***}\n\t← toki pona *k.m.t.u.* ← *‘kalama musi tan uta’*',
    'kute': '***kute*** – *~pu~* ear; to hear, listen; pay attention to, obey\n\t← Acadian French *écouter* ‘listen’',
    'la': '***la*** – *~pu~* (between the context phrase and the main sentence)\n\t← Esperanto *la* ‘(definite article)’ ← Romance *la* ‘(feminine singular definite article)’\n\t← Acadian French -*la`*’(proximal & topical suffix)’',
    'lanpan': '***lanpan*** – *~post-pu~* take, seize, catch, receive, get {see ***jo***, ***alasa***}\n\t← Greek *λαμβάνω lamváno* ‘take, seize, grasp, receive’',
    'lape': '***lape*** – *~pu~* sleeping, resting\n\t← Dutch *slapen* ‘sleep’',
    'laso': '***laso*** – *~pu~* blue, green\n\t← Welsh *glas* ‘blue, inexperienced’ ← Proto-Brythonic *glas* ‘green, blue’',
    'lawa': '***lawa*** – *~pu~* head, mind; to control, direct, guide, lead, own, plan, regulate, rule\n\t← Serbo-Croatian *глава glava* ‘head’',
    'leko': '***leko*** – *~pre-pu~* stairs, square, block\n\t← ?English *Lego* (← Danish *Lego* ← *‘leg godt’* ‘play well’) or Finnish *lohko* ‘block, section’',
    'len': '***len*** – *~pu~* cloth, clothing, fabric, textile; cover, layer of privacy\n\t← Acadian French *linge* ‘clothing’',
    'lenke': '***lenke*** – *~post-pu~* the digit ‘0’\n\t← Cantonese 〇/零 *lìhng* ‘zero’',
    'lete': '***lete*** – *~pu~* cold, cool; uncooked, raw\n\t← Acadian French *frette* ‘cold’ ← Old French *freit* ‘cold’',
    'li': '***li*** – *~pu~* (between any subject except *mi* alone or *sina* alone and its verb; also to introduce a new verb for the same subject)\n\t← Esperanto *li* ‘he’ {cf. Tok Pisin transitive suffix -*im*} ← Latin *ille*',
    'likujo': '***likujo*** – *~post-pu~* collection, assortment, menagerie, arrangement, handful, harvest {see ***kulupu***, ***alasa***}; seven\n\t← Acadian French *recueil* ‘collection, ensemble, anthology’',
    'lili': '***lili*** – *~pu~* little, small, short; few; a bit; young\n\t← Tok Pisin *liklik* ‘small, little’ ← Ramoaaina *liklik*',
    'linja': '***linja*** – *~pu~* long and flexible thing; cord, hair, rope, thread, yarn | *~alt. usage~* line, connection\n\t← Finnish *linja* ‘line’ ← Old Swedish *linia*',
    'linluwi': '***linluwi*** – *~post-pu~* network(s), internet(s) {see ***len***}\n\t← Welsh *rhyngrwyd* ‘internet’ (← *rhwng* ‘between’ + *rhwyd* ‘net’)',
    'lipu': '***lipu*** – *~pu~* flat object; book, document, card, paper, record, website\n\t← Finnish *lippu* ‘flag, banner, ticket’',
    'loje': '***loje*** – *~pu~* red, reddish\n\t← Dutch *rooie* ‘red (inflected)’ ← *rood* ‘red’',
    'lokon': '***lokon*** – *~post-pu, humorous~* {a compromise between ***lukin*** & ***oko***}\n\t← toki pona *lukin* & *oko*',
    'loku': '***loku*** – *~post-pu~* the digit ‘6’\n\t← Cantonese 六 / 陸 *luhk* ‘six’',
    'lon': '***lon*** – *~pu~* located at, present at, real, true, existing | *~alt. usage~* (affirmative response)\n\t← Tok Pisin *long* ‘at, in, on, (spacial particle)’ ← English *along*',
    'luka': '***luka*** – *~pu~* arm, hand, tactile organ; five | *~alt. usage~* touch (physically), interact, press\n\t← Serbo-Croatian *рука ruka* ‘hand, arm’',
    'lukin': '***lukin*** – *~pu~* eye {see ***oko***}; look at, see, examine, observe, read, watch; (pv.) to seek, look for, try to {see ***alasa***}\n\t← Tok Pisin *lukim* ‘see, look at’ ← *luk* ‘look’ (← English *look*) + -*im* ‘(transitive suffix)’ (← English *him*, *’em*)',
    'lupa': '***lupa*** – *~pu~* door, hole, orifice, window\n\t← Lojban *clupa* ‘loop’ (← Mandarin 圈 *quān*, English *loop*, Hindi पाश *pāś*, Arabic أنشوطة‏ *ʾanšūṭa*)',
    'ma': '***ma*** – *~pu~* earth, land; outdoors, world; country, territory; soil\n\t← Finnish *maa* ‘earth, land’',
    'majuna': '***majuna*** – *~pre-pu~* old, aged\n\t← Esperanto *maljuna* ‘old’ ← *mal*- ‘(opposite of)’ (← Latin *malus*) + *juna* ‘young’ (← German *jung* & French *jeune*)',
    'mama': '***mama*** – *~pu~* parent, ancestor; creator, originator; caretaker, sustainer\n\t← Georgian მამა *mama* ‘father’',
    'mani': '***mani*** – *~pu~* money, cash, savings, wealth; large domesticated animal\n\t← English *money* {cf. *fee* and *pecuniary* etymologies}',
    'meli': '***meli*** – *~pu~* woman, female, feminine person; wife {see ***mije***, ***tonsi***}\n\t← Tok Pisin *meri* ‘woman, wife, feminine’ ← Tolai *mari* ‘pretty’ & English *Mary*',
    'melome': '***melome*** – *~post-pu~* sapphic, lesbian, wlw {see ***kule***}\n\t← toki pona *‘meli pi olin meli’*',
    'mi': '***mi*** – *~pu~* I, me, we, us\n\t← Esperanto *mi* ‘I, me’ ← Romance *m*- ‘(1st person singular oblique)’',
    'mije': '***mije*** – *~pu~* man, male, masculine person; husband {see ***meli***, ***tonsi***}\n\t← Finnish *mies* ‘man, husband’',
    'mijomi': '***mijomi*** – *~post-pu~* gay, mlm {see ***kule***}\n\t← toki pona *‘mije pi olin mije’*',
    'misikeke': '***misikeke*** – *~pre-pu~* medicine\n\t← ? Ojibwe',
    'moku': '***moku*** – *~pu~* to eat, drink, consume, swallow, ingest\n\t← Japanese モグモグ *mogumogu* ‘munching’',
    'moli': '***moli*** – *~pu~* dead, dying\n\t← Acadian French *mourir* ‘die’',
    'monsi': '***monsi*** – *~pu~* back, behind, rear\n\t← Acadian French *mon tchu* ‘(vulgar) my ass’',
    'monsuta': '***monsuta*** – *~pre-pu~* fear, monster\n\t← Japanese モンスター *monsutā* ‘monster’ ← English *monster*',
    'mu': '***mu*** – *~pu~* (animal noise or communication) | *~alt. usage~* (non-speech vocalization)\n\t←? onomatopoeia',
    'mulapisu': '***mulapisu*** – *~post-pu, humorous, w.o.g. Sonja~* pizza\n\t←?',
    'mun': '***mun*** – *~pu~* moon, night sky object, star\n\t← English *moon*',
    'musi': '***musi*** – *~pu~* artistic, entertaining, frivolous, playful, recreation\n\t← Esperanto *amuzi* ‘have fun’ ← French *amuser*',
    'mute': '***mute*** – *~pu~* many, a lot, more, much, several, very; quantity | *~alt. usage~* three (or more)\n\t← Esperanto *multe* ‘a lot’ ← Latin *multus*',
    'namako': '***namako*** – *~pu~* {see ***sin***} | *~alt. usage~* embellishment, spice; extra additional\n\t← Persian نمک *namak* ‘salt’',
    'nanpa': '***nanpa*** – *~pu~* -th (ordinal number); numbers\n\t← Tok Pisin *namba* ‘number, (ordinal marker)’ ← English *number*',
    'nasa': '***nasa*** – *~pu~* unusual, strange; foolish, crazy; drunk, intoxicated\n\t← Tok Pisin *nasau* ‘stupid’',
    'nasin': '***nasin*** – *~pu~* way, custom, doctrine, method, path, road\n\t← Serbo-Croatian *начин način* ‘way, method’',
    'neja': '***neja*** – *~post-pu~* four\n\t← Finnish *neljä* ‘four’',
    'nena': '***nena*** – *~pu~* bump, button, hill, mountain, nose, protuberance\n\t← Finnish *nenä* ‘nose’',
    'ni': '***ni*** – *~pu~* that, this {see ***ona***}\n\t← Cantonese 呢 *ni* ‘this’',
    'nimi': '***nimi*** – *~pu~* name, word\n\t← Finnish *nimi* ‘name’',
    'noka': '***noka*** – *~pu~* foot, leg, organ of locomotion; bottom, lower part\n\t← Serbo-Croatian *нога noga* ‘foot, leg’',
    'nu': '***nu*** – *~post-pu, humorous~* {see ***nuwa***, ***sin***}\n\t← English *new*',
    'nun': '***nun*** – *~post-pu~* the digit ‘5’\n\t← Cantonese 五 / 伍 *ńgh* ‘five’',
    'nuwa': '***nuwa*** – *~post-pu, humorous~* {see ***nu***, ***sin***}\n\t← English *newer*',
    'o': '***o*** – *~pu~* hey! O! (vocative, imperative, or optative) {see ***li***}\n\t← Georgian -ო -*o* ‘(vocative suffix)’ & English *oh*',
    'oke': '***oke*** – *~post-pu~* (acknowledgement or acceptance) {see ***ke***}\n\t← English *okay*',
    'okepuma': '***okepuma*** – *~post-pu, humorous~* boomer, Baby Boomer, inconsiderate elder\n\t← English *okay boomer*',
    'oko': '***oko*** – *~pu~* {see ***lukin***} | *~alt. usage~* eye, ocular, visual {cf. ***lukin***}\n\t← Serbo-Croatian *око oko* ‘eye’',
    'olin': '***olin*** – *~pu~* love, have compassion for, respect, show affection to\n\t← Serbo-Croatian *волим volim* ‘I love’',
    'omen': '***omen*** – *~post-pu, humorous~* sarcasm, ironic\n\t← toki pona *o.m.e.m.* ← *‘o moli e mi’*',
    'ona': '***ona*** – *~pu~* he, she, it, they\n\t← Serbo-Croatian *она ona* ‘she’',
    'open': '***open*** – *~pu~* begin, start; open; turn on\n\t← English *open*',
    'pa': '***pa*** – *~post-pu, humorous~* bruh\n\t← English *bruh*',
    'pakala': '***pakala*** – *~pu~* botched, broken, damaged, harmed, messed up | *~alt. usage~* (curse expletive, e.g. fuck!)\n\t← Tok Pisin *bagarap* ‘accident’ ← English *bugger up*',
    'pake': '***pake*** – *~pre-pu~* stop, cease {see ***pini***}\n\t←? English *block*',
    'pali': '***pali*** – *~pu~* do, take action on, work on; build, make, prepare\n\t← Esperanto *fari* ‘do, make’ ← Italian *fare* & French *faire*',
    'palisa': '***palisa*** – *~pu~* long hard thing; branch, rod, stick\n\t← Serbo-Croatian *палица palica* ‘bat, rod, cane’',
    'pan': '***pan*** – *~pu~* cereal, grain; barley, corn, oat, rice, wheat; bread, pasta\n\t← Romance *pan* ‘bread’ & Japanese パン *pan* (← Portuguese *pão*)',
    'pana': '***pana*** – *~pu~* give, send, emit, provide, put, release\n\t←? Finnish *panna* ‘put, set, place’ or Swahili *pana* ‘give to each other’',
    'pasila': '***pasila*** – *~pre-pu~* good, easy {see ***pona***}\n\t← French *facile* ‘easy’',
    'pata': '***pata*** – *~pre-pu~* sibling\n\t←? Serbo-Croatian *брат brat* ‘brother’ or Tok Pisin *brata* ‘sibling or cousin of the same gender’ (← English *brother*)',
    'patu': '***patu*** – *~post-pu~* the digit ‘8’\n\t← Cantonese 八 / 捌 *baat* ‘eight’',
    'peto': '***peto*** – *~post-pu~* cry, tears\n\t← toki pona *p.e.t.o.* ← *‘pana e telo oko’*',
    'peta': '***peta*** – *~post-pu~* green, greenish; verdant, alive; ecofriendly\n\t← Esperanto *verda* ‘green’',
    'pi': '***pi*** – *~pu~* of [used to divide a second noun group that describes a first noun group] | \n\t← Tok Pisin *bilong* ‘of’ ← English *belong*',
    'pilin': '***pilin*** – *~pu~* heart (physical or emotional); feeling (an emotion, a direct experience)\n\t← Tok Pisin *pilim* ‘feel’ ← *pil* (← English *feel*) + -*im* ‘(transitive suffix)’ ← (English *him*, *’em*)',
    'pimeja': '***pimeja*** – *~pu~* black, dark, unlit\n\t← Finnish *pimeä* ‘dark’',
    'pini': '***pini*** – *~pu~* ago, completed, ended, finished, past {see ***pake***}\n\t← French *fini* ‘finished, completed’ & Tok Pisin *pinis* ‘(perfective aspect)’ ← English *finish*',
    'pipi': '***pipi*** – *~pu~* bug, insect, ant, spider\n\t← Acadian French *bibitte* ‘bug’',
    'pipo': '***pipo*** – *~post-pu, humorous~* annoy, annoyance, bothersome, boring\n\t← toki pona *pipi*',
    'po': '***po*** – *~pre-pu~* four\n\t←? English *four*',
    'poka': '***poka*** – *~pu~* hip, side; next to, nearby, vicinity | *~alt. usage~* along with (comitative), beside {see ***kan***}\n\t← Serbo-Croatian *бока boka*, genitive of *бок bok* ‘side, flank’',
    'poki': '***poki*** – *~pu~* container, bag, bowl, box, cup, cupboard, drawer, vessel\n\t← Tok Pisin *bokis* ‘box, (vulgar) female genitalia’ ← English *box*',
    'polinpin': '***polinpin*** – *~post-pu, humorous~* bowling pin\n\t← English *bowling pin*',
    'pomotolo': '***pomotolo*** – *~post-pu, humorous~* effective, useful, give good results\n\t← Italian *pomodoro* ‘tomato,’ from the time management method developed by Francesco Cirillo in Berlin in the 1980s',
    'pona': '***pona*** – *~pu~* good, positive, useful; friendly, peaceful; simple\n\t← Esperanto *bona* ‘good’',
    'powe': '***powe*** – *~pre-pu~* unreal, false, untrue, pretend, deceive, trickster\n\t←? French *faux* ‘false’',
    'pu': '***pu*** – *~pu~* interacting with the official Toki Pona book\n\t←? Mandarin 樸 *pǔ* ‘unworked wood; inherent quality; simple’ & English *book*',
    'sama': r'***sama*** – *~pu~* same, similar; each other; sibling, peer, fellow; as, like\n\t← Finnish *sama* ‘same’ (← PG \**samaz* ‘same, alike’) & Esperanto *sama* ‘same’ (← English *same*)',
    'samu': '***samu*** – *~post-pu, humorous, w.o.g. Sonja~* wanting to create new words\n\t← jan Samu, a user who attempted to propose a new word',
    'san': '***san*** – *~post-pu~* three {particularly in senary base; see ***tuli***} | *~post-pu~* the digit ‘3’\n\t← Japanese 三 *san* ‘three’ | Cantonese 三/叁 *sāam* ‘three’',
    'se': '***se*** – *~post-pu~* the digit ‘4’\n\t← Cantonese 四/肆 *sei* ‘four’',
    'seli': '***seli*** – *~pu~* fire; cooking element, chemical reaction, heat source\n\t← Georgian ცხელი *cxeli* ‘hot’',
    'selo': '***selo*** – *~pu~* outer form, outer layer; bark, peel, shell, skin; boundary\n\t← Esperanto *ŝel*o ‘skin, peel’ ← German *Schale* ‘peel, husk, shell’',
    'seme': '***seme*** – *~pu~* what? which?\n\t← Mandarin 什麼 *shénme* ‘what, something’',
    'sewi': '***sewi*** – *~pu~* area above, highest part, something elevated; awe-inspiring, divine, sacred, supernatural\n\t← Georgian ზევით *zevit* ‘upwards’',
    'sijelo': '***sijelo*** – *~pu~* body (of person or animal), physical state, torso\n\t← Serbo-Croatian *тијело tijelo* ‘body’',
    'sike': '***sike*** – *~pu~* round or circular thing; ball, circle, cycle; of one year\n\t← English *circle*',
    'sikomo': '***sikomo*** – *~post-pu, humorous~* on a higher tier/plane, enlighten(ed), epic; to an exceedingly great extent\n\t← English *sicko mode* (← Travis Scott song *Sicko Mode*)',
    'sin': '***sin*** – *~pu~* new, fresh; additional, another, extra {see ***namako***}\n\t← Mandarin 新 *xīn* ‘new, fresh’',
    'sina': '***sina*** – *~pu~* you, your\n\t← Finnish *sinä* ‘you’',
    'sinpin': '***sinpin*** – *~pu~* face, foremost, front, wall\n\t← Cantonese 前邊 *tsin bin* ‘in front’',
    'sitelen': '***sitelen*** – *~pu~* image, picture, representation, symbol, mark, writing\n\t← Dutch *schilderen* ‘paint’',
    'slape': '***slape*** – *~post-pu, humorous~* {see ***lape***}\n\t← toki pona *lape* and English *sleep*',
    'soko': '***soko*** – *~post-pu~* fungus, fungi\n\t← Georgian სოკო *sok’o* ‘mushroom’',
    'sona': '***sona*** – *~pu~* know, be skilled in, be wise about, have information on; (pv.) know how to\n\t← Georgian ცოდნა *codna* ‘knowledge’',
    'soto': '***soto*** – *~post-pu~* left, left side\n\t← Swahili *shoto* ‘left side’',
    'soweli': '***soweli*** – *~pu~* animal, beast, land mammal\n\t← Georgian ცხოველი *cxoveli* ‘beastly animal, lively, passionate’',
    'su': '***su*** – *~post-pu, humorous~* [yes/no question marker, taking the place of *li* & *o*] {see ***ala***}\n\t← Esperanto *ĉu* ‘[yes/no question marker]; whether’',
    'suli': '***suli*** – *~pu~* big, heavy, large, long, tall; important; adult\n\t← Finnish *suuri* ‘big, large, great’',
    'suno': '***suno*** – *~pu~* sun; light, brightness, glow, radiance, shine; light source\n\t← Esperanto *suno* ‘sun’',
    'supa': '***supa*** – *~pu~* horizontal surface, thing to put or rest something on\n\t← Esperanto *surfaco* ‘surface’ ← French & English *surface*',
    'suwi': '***suwi*** – *~pu~* sweet, fragrant; cute, innocent, adorable\n\t← Tok Pisin *suwi* ← English *sweet*',
    'take': '***take*** – *~post-pu~* the digit ‘7’\n\t← Cantonese 七 / 柒 *chāt* ‘seven’',
    'tan': '***tan*** – *~pu~* by, from, because of; origin, cause\n\t← Cantonese 從 *tsung* ‘from’',
    'taso': '***taso*** – *~pu~* but, however; only\n\t← Tok Pisin *tasol* ‘just, only, but, however’ ← English *that’s all*',
    'tawa': '***tawa*** – *~pu~* going to, toward; for; from the perspective of; moving\n\t← English *towards*',
    'te': '***te*** – *~post-pu~* right, the right side\n\t← Welsh *de* ‘right’',
    'telo': '***telo*** – *~pu~* water, liquid, fluid, wet substance; beverages\n\t← Acadian French *de l’eau* ‘(some) water’',
    'ten': '***ten*** – *~post-pu~* {shortened variant of ***tenpo***}\n\t← toki pona *tenpo*',
    'tenpo': '***tenpo*** – *~pu~* time, duration, moment, occasion, period, situation\n\t← Esperanto *tempo* ‘time’ ← Latin *tempus*',
    'toki': '***toki*** – *~pu~* communicate, say, speak, talk, use language, think\n\t← Tok Pisin *tok* ← English *talk*',
    'tomo': '***tomo*** – *~pu~* indoor space; building, home, house, room\n\t← Esperanto *domo* ‘house’ ← Polish *dom*, Latin *domus*, Ancient Greek *δόμος*',
    'tonsi': '***tonsi*** – *~post pu~* trans, gender-non-conforming, non-binary {see ***meli***, ***mije***, ***kule***}\n\t← Mandarin 同志 *tóngzhì* ‘comrade (same will/purpose); LGBT+’',
    'tu': '***tu*** – *~pu~* two | *~alt. usage~* separate, cut {see ***kipisi***}\n\t← English *two* & Esperanto *du*',
    'tuli': '***tuli*** – *~pre-pu~* three {see ***san***}\n\t← English *three*',
    'unpa': '***unpa*** – *~pu~* have sexual or marital relations with\n\t←? onomatopoeia',
    'uta': '***uta*** – *~pu~* mouth, lips, oral cavity, jaw\n\t← Serbo-Croatian *уста usta* ‘mouth’',
    'utala': '***utala*** – *~pu~* battle, challenge, compete against, struggle against\n\t← Serbo-Croatian *ударати udarati* ‘strike, hit, hurt’',
    'waleja': '***waleja*** – *~post-pu~* context, topic, salience, pertinent, topical, pertain to, be relevant\n\t← Quenya *valdea* ‘of moment, important’',
    'walo': '***walo*** – *~pu~* white, whitish; light-coloured, pale\n\t← Finnish *valko*- ‘white’',
    'wan': '***wan*** – *~pu~* unique, united; one\n\t← English *one*',
    'waso': '***waso*** – *~pu~* bird, flying creature, winged animal\n\t← French *oiseau* ‘bird’',
    'wawa': '***wawa*** – *~pu~* strong, powerful; confident, sure; energetic, intense\n\t← Finnish *vahva* ‘strong, powerful, thick’',
    'wawajete': '***wawajete*** – *~post-pu, humorous~* something that appears to break the rules but doesn\'t; faux edginess, provocation\n\t← toki pona *wuwojiti* (all phonotactically unviable CV syllables in toki pona)',
    'we': '***we*** – *~post-pu~* (acts as a transition from one complete sentence to another)\n\t←Spanish *güey* ‘man’ ← English *man* (sentence tag)',
    'weka': '***weka*** – *~pu~* absent, away, ignored\n\t← Dutch *weg* ‘away, gone’',
    'wi': '***wi*** – *~post-pu, humorous~* we (excluding you, i.e. 1st person exclusive) {see ***mi***}\n\t← English *we*',
    'wile': '***wile*** – *~pu~* must, need, require, should, want, wish\n\t← Dutch *willen* ‘want, desire’',
    'yupekosi': '***yupekosi*** – *~post-pu, humorous, w.o.g. Sonja~* to behave like George Lucas and revise your old creative works and actually make them worse; “nobody knows how to pronounce the *y*”\n\t← ?'
}

def check_pamu(text):
    msg_step1 = re.sub(r'\|\|[^\|]+\|\||\s', '', text)
    msg_step2 = emoji.demojize(msg_step1)
    msg_step3 = re.sub(r':\w+:', '', msg_step2)
    msg_step4 = re.sub('([mnptksljw][uia])', '', msg_step3)
    if msg_step4 == '':
        return True
    else:
        return False

def removeduplicates(s):
    n = len(s)
    if (n < 2):
        return s
    j = 0
    for i in range(n):
        if (s[j] != s[i]):
            j += 1
            s = s[:j]+s[i]+s[j+1:]
    j += 1
    s = s[:j]
    return s

def check_tp(text):
    msg_step1 = re.sub(r'\|\|[^\|]+\|\|', '', text, flags=re.S) #Removes things behind spoiler bars
    msg_step2 = emoji.demojize(msg_step1) #Turns emojis into ascii characters
    msg_step3 = re.sub(r':[\w-]+:', '', msg_step2) #Removes now textified emojis
    msg_step4 = re.sub(r'https\S+', '', msg_step3) #Removes links
    msg_step5 = re.sub('j?[A-Z][a-z]+|[゠-ヿ]+', '', msg_step4) #Removes proper names
    msg_step6 = re.sub(r'[\W_0-9]', ' ', msg_step5) #Removes non-letter characters, such as punctuation
    msg_step7 = removeduplicates(msg_step6) #Removes repeated letters
    msg_step8 = re.split(r'\s+', msg_step7) #Splits the string and prepares it for analysis
    for dj in msg_step8:
        if dj in tp_words:
            pass
        else:
            return False
    return True

def check_tp_soft(text):
    score = 0
    msg_step1 = re.sub(r'\|\|[^\|]+\|\|', '', text, flags=re.S) #Removes things behind spoiler bars
    msg_step2 = emoji.demojize(msg_step1) #Turns emojis into ascii characters
    msg_step3 = re.sub(r':[\w-]+:', '', msg_step2) #Removes now textified emojis
    msg_step4 = re.sub(r'https\S+', '', msg_step3) #Removes links
    msg_step5 = re.sub('j?[A-Z][a-z]+|[゠-ヿ]+', '', msg_step4) #Removes proper names
    msg_step6 = re.sub(r'[\W_0-9]', ' ', msg_step5) #Removes non-letter characters, such as punctuation
    msg_step7 = removeduplicates(msg_step6) #Removes repeated letters
    msg_step8 = re.split(r'\s+', msg_step7) #Splits the string and prepares it for analysis
    for dj in msg_step8:
        if dj in tp_words:
            score += 1
        else:
            score -= 1
    if score < 0:
        return False
    else:
        return True

class language(commands.Cog):

    """LANGUAGE"""

    def __init__(self, client):
        self.client = client

    #Commands
    @commands.command(hidden=True)
    @commands.is_owner()
    async def test(self, ctx, a, b):
        """Don't worry about this one. Bot owner only."""
        a = int(a)
        b = int(b)
        result1 = (a + ((a**2)/b) - (b**a) + (a**b))
        result2 = ((((a ** 2) + (a * b))/b) - ((b ** a) - (a ** b)))
        result3 = math.fsum([a, (a**2/b), -(b**a), (a**b)])
        await ctx.send(f'Simplified formula result: {result1}\nUnsimplified formula result: {result2}\nExtra test: {result3}')

    @commands.command(aliases=['cpm', 'cfpm', 'cfp'])
    async def check_for_pamu(self, ctx, *, text):
        """Checks if the input text is valid in pa mu or not. It does so by first removing anything behind spoiler bars and any whitespace characters, then removing emojis, and then it runs the text through all possible syllables in pa mu."""
        if check_pamu(text):
            await ctx.send("pa mu confirmed. :sleepy:")
        else:
            await ctx.send(":rotating_light: Not pa mu! :rotating_light:")

    @commands.command(aliases=['ctp', 'cftp', 'cft'])
    async def check_for_tp(self, ctx, *, text):
        """Checks if the input text is valid in toki pona or not.\n\nAnything behind spoiler bars won\'t count towards the detection process. In addition, any word that is capitalized will pass. Every other word will be examined, and if it doesn\'t match a word in a certain list (taken from nimi ale pona), it won\'t pass. Hiragana and Katakana is supported, as long as there are spaces between words.\n\nFor more information, or to request a change in the program, please contact me (jan Kaje#3293)."""
        if check_tp(text):
            await ctx.send("toki pona confirmed. :sleepy:")
        else:
            await ctx.send(":rotating_light: Not toki pona! :rotating_light:")

    @commands.command(aliases=['d', 'dict', 'define'])
    async def dictionary(self, ctx, *words):
        """Displays the definition and etymology of a word or words. Entries taken from *nimi ale pona.*"""
        if len(words) == 0:
            await ctx.send('You need to input at least one word.')
            return
        if len(words) > 10:
            await ctx.send('That\'s too many words.')
            return
        for i in words:
            try:
                await ctx.send(tp_dict[i])
            except KeyError:
                await ctx.send(f'{i} is not a word in my dictionary.')
    
    @commands.command()
    async def hc(self, ctx):
        """Gives/takes the hardcore role. See the Features section of `,help` for more info."""
        if ctx.guild.id == 654411781929959424:
            role = ctx.guild.get_role(706257334682386582)
        elif ctx.guild.id == 301377942062366741:
            role = ctx.guild.get_role(712083555131326464)
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.send("Hardcore role removed.")
        else:
            await ctx.author.add_roles(role)
            await ctx.send("Hardcore role given.")

    #On message: hardcore, tpt moderation
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild.id == 654411781929959424:
            try:
                role = msg.guild.get_role(706257334682386582)
                if role in msg.author.roles:
                    if msg.content[0] not in ',*' and msg.content[:2] != 't!':
                        if check_pamu(msg.content) == False:                            
                            try:
                                await msg.delete()
                            except discord.errors.NotFound:
                                return
                elif msg.channel.id == 654422747090518036:
                    if check_pamu(msg.content) == False:
                        try:
                            await msg.delete()
                        except discord.errors.NotFound:
                            return
            except AttributeError:
                if msg.channel.id == 654422747090518036:
                    if check_pamu(msg.content) == False:
                        try:
                            await msg.delete()
                        except discord.errors.NotFound:
                            return
        elif msg.guild.id == 301377942062366741:
            try:
                role = msg.guild.get_role(712083555131326464)
                if role in msg.author.roles:
                    if msg.channel.id in [301377942062366741, 375591429608570881, 340307145373253642, 545467374254555137]:
                        if msg.content[0] not in ',*=.!' and msg.content[:2] not in 't!x/;;' and msg.content[:3] != 'pk;':
                            if check_tp(msg.content) == False:
                                try:
                                    await msg.delete()
                                except discord.errors.NotFound:
                                    return
            except AttributeError:
                pass
            if msg.channel.id in [316063418253705229, 716768435081576448, 716768463791718490, 716768500659781642, 716768537729040387, 716768591864791100, 716768624085303297]:
                try:
                    if msg.content[0] not in ',*=.!' and msg.content[:2] not in 't!x/;;' and msg.content[:3] != 'pk;' and not msg.author.bot:
                        if not check_tp_soft(msg.content):
                            score = 0
                            async for i in msg.channel.history(limit=10):
                                if not check_tp_soft(i.content):
                                    score += 1
                                if i.content == 'https://cdn.discordapp.com/attachments/316066233755631616/672822465633976345/image-6.png':
                                    score += 1
                            if score == 10:
                                await msg.channel.send('https://cdn.discordapp.com/attachments/316066233755631616/672822465633976345/image-6.png')
                            elif score == 7:
                                await msg.channel.send('*o toki pona taso a.* Seriously, please stop. Channels that begin with tpt are for toki pona only. If you\'re going to speak in a different language, move to a different channel.', delete_after=20)
                            elif score == 3:
                                await msg.channel.send('This is your friendly, automated reminder to only speak in toki pona here. pona la o toki pona taso lon tomo ni.', delete_after=8)
                except:
                    pass
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.guild.id == 654411781929959424:
            try:
                role = after.guild.get_role(706257334682386582)
                if role in after.author.roles:
                    if after.content[0] not in ',*' and after.content[:2] != 't!':
                        if check_pamu(after.content) == False:                            
                            try:
                                await after.delete()
                            except discord.errors.NotFound:
                                return
                elif after.channel.id == 654422747090518036:
                    if check_pamu(after.content) == False:
                        try:
                            await after.delete()
                        except discord.errors.NotFound:
                            return
            except AttributeError:
                if after.channel.id == 654422747090518036:
                    if check_pamu(after.content) == False:
                        try:
                            await after.delete()
                        except discord.errors.NotFound:
                            return
        elif after.guild.id == 301377942062366741:
            try:
                role = after.guild.get_role(712083555131326464)
                if role in after.author.roles:
                    if after.channel.id in [301380012156911616, 301377942062366741, 316063418253705229, 375591429608570881, 340307145373253642, 545467374254555137]:
                        if after.content[0] not in ',*=.!' and after.content[:2] not in 't!x/;;' and after.content[:3] != 'pk;':
                            if check_tp(after.content) == False:
                                try:
                                    await after.delete()
                                except discord.errors.NotFound:
                                    return
            except AttributeError:
                return