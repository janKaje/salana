import discord
from discord.ext import commands
import re
import emoji
import string
import time
import math
from PIL import Image, ImageDraw, ImageFont
import os
    
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

tpt_dict = {
    "a": "**ona li pona a!** ona li pona. ni li lon.\n**mi toki e ni: “a a a!”** mi lukin anu kute e ijo. mi toki insa e ni: “tenpo pini lili la mi sona ala e ni: ijo ni li kama. ken la ona li ike tawa jan. a! ona li ike ala tawa mi. mi pilin pona tan ona.” uta mi li kalama.",
    "akesi": "akesi li sama soweli, taso akesi li lete li jo ala e linja sama soweli.\nakesi li sama soweli, taso akesi li ken lon telo lon tenpo suli.\nakesi li sama soweli, taso akesi li ike lukin.",
    "ala": "**ijo ala li lon.** ijo ale li lon ala.\n**ona li moku ala moku?** ona li moku anu seme?",
    "alasa": "**mi alasa e ona.** mi kama sona e ni: ona li lon seme? mi tawa ona. ken la mi utala e ona.\n**mi alasa e ijo mute**. ijo mute li lon ma ante mute. mi pana e ijo ni ale tawa ma wan.\n**mi alasa moli e ona.** mi lukin moli e ona.",
    "ale": "**ijo ale li lon.** ijo ala li lon ala.\n**ale li pona.** lon li pona.\n**ale li pona.** ma ale en ijo ale li pona.\n**ona ale li pona.** wan ale ona li pona.\nale li nanpa mute mute mute mute mute.",
    "anpa": "**mi lon anpa ona.** ona li lon sewi mi.\n**mi anpa.** mi tawa anpa.\nanpa li supa suli lon tomo. ijo li lon insa tomo la ona li lon ijo ante ala la ona li lon anpa.",
    "ante": "**ona li ante.** ona li sama ala.",
    "anu": "**mi anu sina li moku.** mi moku ala la sina moku.\n**mi moku. anu la sina moli.** mi moku ala la sina moli.",
    "awen": "ijo awen li ante ala lon tenpo suli.\nijo awen li tawa ala lon tenpo suli.\n**mi awen moku.** mi pini ala moku.",
    "e": "**mi moli e ona.** mi tan pi moli ona.\n**mi pona e ona.** ona li kama pona tan mi.\n**mi moku e kili e pan.** mi moku e kili. mi moku e pan.",
    "en": "**mi en sina li moku.** mi moku. sina moku.",
    "esun": "**mi esun e ona.** mi jo e ona. taso mi wile e ijo pi jan ante. ni la mi toki tawa jan ni li toki e ni: “mi pana e ona tawa sina la o pana e ijo ni tawa mi.”\n**mi esun e ona.** jan ante li jo e ona li toki e ni: “sina pana e mani tawa mi la mi pana e ona tawa sina.” ni la mi pana e mani tawa jan ni. tan ni la jan ni li pana e ona tawa mi.\nesun li kulupu jan li pali li esun.\nesun li tomo. jan li esun lon esun.",
    "ijo": "jan en soweli en kasi en kiwen en pali li ijo.",
    "ike": "ike li pona ala.\n**pali ni li ike.** mi pali suli ala la mi ken ala pali e pali ni.\n**ona li ike.** ona li jo e wan mute mute. jan li kama sona e ona lon tenpo lili taso la jan ni li sona ala e ona.",
    "ilo": "jan li kepeken ilo.\njan li ken moku kepeken ilo moku. jan mute li wile moku kepeken ilo moku. tan ni la jan li pali e ilo moku mute.",
    "insa": "**mi lon insa pi ijo tu.** ijo ni wan li lon poka mi. ijo ni ante li lon poka ante mi.\n**mi tawa insa tomo.** tenpo pini la mi lon insa tomo ala. taso mi tawa. ni la mi lon insa tomo.\ninsa li wan insa sijelo.",
    "jaki": "ijo lili mute li lon selo pi ijo jaki. mi wile weka e ijo lili ale tan selo ona.",
    "jan": "jan li sama soweli, taso jan li ken toki pona.",
    "jelo": "insa pi sike mama li jelo.",
    "jo": "**mi jo e ona.** mi luka e ona. ni la ona li lon poka mi. ni la mi ken tawa e ona.",
    "kala": "kala li sama soweli, taso kala li lon telo li lete li jo ala e noka.",
    "kalama": "jan li ken kute e kalama. taso jan ala li ken lukin e kalama. kalama li tawa kepeken kon.\nmi weka tan kalama suli la mi ken kute e kalama suli.\n**mi kalama.** mi pali e kalama.",
    "kama": "**sina kama tawa ona.** mi en ona li lon ma ni. sina tawa ma ni.\n**ona li kama tawa mi.** jan anu ijo li pali e ona tawa mi.\n**moli mi li kama.** mi moli.\n**mi kama suli.** tenpo pini la mi suli ala. taso ijo li kama. ni la mi suli.\n**mi kama e ona.** ona li lon tan mi.\n**mi moku la tenpo kama la sina toki.** sina toki la tenpo pini la mi moku.\ntenpo kama la mi moli.\ntenpo pini la mi sona ala e ona. tenpo ni la mi kama sona e ona. tenpo kama la mi sona e ona.",
    "kasi": "kasi li jo ala e suno e telo la kasi li moli.\njan li tu e kasi li pali e tomo kepeken ona.\nkasi li wan kasi.",
    "ken": "**mi ken pali.** mi lukin pali la mi pali.\n**ken la ona li lon.** ijo sama ona li ken lon. mi sona ala e ni: ona li lon ala lon?\n**mi ken e ona.** mi kama ala e ni: ona li kama ala. ni la ona li ken kama.\nijo ken li ken kama.",
    "kepeken": "**mi utala e ona kepeken ilo.** mi lawa e ilo. tan ni la ilo li tawa li utala e ona.\n**mi kepeken ona.** mi pali kepeken ona.",
    "kili": "kili li moku kasi.",
    "kin": "**ona kin li lon.** ona li ijo sin sama ni li lon.",
    "kiwen": "kon en telo en kiwen li ante. ijo li kiwen la ona li kon ala li telo ala.\njan li pali e ilo moku e ilo pakala e ilo utala kepeken kiwen.",
    "ko": "jan li weka e ko tan ma li pali e poki kepeken ko. ko en telo li wan la ona li kiwen ala. ko li seli la ona li kama kiwen.",
    "kon": "jan ala li ken lukin e kon. taso kon li tawa la jan li ken pilin e ona.\nijo kon li sama kon.\njan li ken pilin kon kepeken nena ona.\n**mi kon.** mi pana e kon.\n**mi tawa kon.** mi tawa lon kon lon tenpo suli. mi pilin e kon, taso mi pilin ala e ma kiwen.\nkon li wan jan li pilin. jan mute li pilin e ni: sijelo jan li moli la kon ona li awen lon li awen pilin.",
    "kule": "pimeja en walo en laso en jelo en loje li kule.",
    "kulupu": "ijo mute li sama wan la ona li kulupu.",
    "kute": "mi ken kute e kalama e toki kepeken kute mi.",
    "la": "**tenpo ni la mi moku.** mi moku lon tenpo ni.\n**tan ni la mi moku.** mi moku tan ni.\n**mi moku ala la mi moli.** ken la mi moku ala. tan ni la mi moli.\n**ni la mi moku.** tan ni la mi moku.\n**mi la ona li pona.** tawa mi la ona li pona.\n**pipi ante la pipi ni li suli.** pipi ni li suli mute. pipi ante li suli lili.",
    "lape": "**mi lape.** tenpo suli la mi awen li tawa ala li lukin ala li pilin ala li toki ala. tenpo mute la jan ale li lape. tenpo pimeja la jan mute li lape.",
    "laso": "tenpo suno la sewi li laso.\nkasi mute li laso.",
    "lawa": '**mi lawa e ona.** mi kama e ni: ona li pali.\nuta mi en lukin mi li lon lawa mi.\nlawa jan li wan sijelo li pilin li toki insa.\njan lawa li toki e ijo sama ni: “jan ale li ken pali e ijo ni li ken ala pali e ijo ante. mi pali e ike tawa jan ike. mi pana e pona tawa jan pona.”\nijo lawa li suli mute li ken pali e ijo mute.',
    "len": "**mi len e ona kepeken ijo.** mi pana e ijo ni lon poka ale ona.\njan li pali e len kepeken linja mute. jan li ken len e sijelo kepeken len. sijelo li lon insa len la ona li seli.",
    "lete": "lete li lon la telo li kama kiwen.\nijo lete li seli ala.",
    "li": "**sina moku li moli.** sina moku. sina moli.",
    "lili": "ijo lili li suli ala.\nijo lili li ijo pi mute ala.\ntenpo pini suli la jan lili li lon ala. taso tenpo pini lili la mama ona li lon e ona.",
    "linja": "linja mute li lon selo soweli li lon lawa jan mute.\njan li pali e linja kepeken nasin ni: ona li kama jo e linja mute li tawa e kulupu linja sama ni: pini wan taso pi kulupu linja li sike.\nmi jo e pini linja wan la sina jo e pini linja ante la mi tawa weka tan sina la mi ken ala tawa weka e pini linja mi la linja ni li lukin sama ijo linja.",
    "lipu": "wan ale pi selo sinpin lipu li lon poka pi selo monsi lipu. jan li pali e lipu kepeken nasin ni: ona li wan e wan kasi lili mute e telo seli.\nlipu li jo e lipu mute e nimi mute.",
    "loje": "jan li tu e sijelo la telo sijelo loje li tawa weka tan sijelo.",
    "lon": "**mi lon ma ni.** mi pilin e ma ni.\n**mi lon ni.** mi lon ma ni.\n**jan li toki e ni: “soweli li lon ni.”** jan li lon ma li toki. toki ona la soweli li lon ma sama.\n**ona li lon.** ona li lon ma.\n**mi lon e ona.** mi tan pi lon ona.",
    "luka": "luka jan li wan sijelo. jan li ken jo kepeken luka ona.\nluka li nanpa tu tu wan.\npalisa luka li lon luka.\n**mi luka e ona.** mi pilin e ona kepeken luka mi.",
    "lukin": "jan li ken lukin e kule. taso jan ala li ken kute e kule.\nlukin jan li wan sijelo. jan li ken lukin tan lukin ona.\n*mi lukin moli e ona.* mi wile e ni: ona li moli. mi toki insa e ni: “ken la mi pali e ijo la ona li moli.” tan ni la mi pali e ijo ni.",
    "lupa": "lupa ona li lon insa ona. taso wan ona ala li lon insa lupa. ijo ante li ken tawa insa lupa.\nlupa li lupa lon sinpin tomo.",
    "ma": "jan ale li lon ma. kasi mute li kama suli lon insa ma.\ntomo li lon ma, taso ma li lon insa tomo ala.\njan lawa li lawa e ma.",
    "mama": "jan tu li lon e jan lili la ona li mama pi jan lili ni.\nmama pi mama mi li mama mi.\nmama mi en jan sama mi li kulupu mama mi.\nsike mama li kama suli lon insa pi sijelo waso li tawa weka tan waso mama li kama e waso lili.\njan meli mute en soweli meli mute li pali e telo mama lon insa pi sijelo ona. jan lili mute en soweli lili mute li moku e telo mama taso.",
    "mani": "tenpo mute la jan li esun kepeken mani. jan mute li wile e mani.\nmani li soweli suli. jan mute li moku e sijelo mani e telo mama mani. jan li awen e mani mute tan ni.",
    "meli": "meli li sama ni: tenpo mute la meli li lon e jan lili la jan lili li lon insa pi sijelo ona.",
    "mi": "**jan li toki e ni: “mi moku.”** jan li toki. toki ona la ona li moku.",
    "mije": "mije li meli ala.",
    "moku": "**mi moku e kili.** mi tawa e kili lon insa mi.\njan li moku e moku.",
    "moli": "**mi moli.** mi pini lon.",
    "monsi": "ona li jo e pini tu la pini wan li sinpin ona la pini ante li monsi ona.\nmonsi jan li wan sijelo lon sewi noka.",
    "mu": "soweli li toki e mu taso.",
    "mun": "tenpo pimeja la jan li ken lukin e mun lon sewi.",
    "musi": "**mi musi.** mi pali e pona tawa mi.\njan li pali e kalama musi tan ni: jan li wile kute e ona.\njan li pali e musi. musi li pona lukin.",
    "mute": "wan li mute ala. tu li mute ala. tu wan li mute. tu tu li mute. tu tu wan li mute…\n**sina lukin e jan pi mute seme?** sina lukin e jan wan anu jan tu anu jan tu wan…?\nmute li nanpa luka luka luka luka.",
    "namako": "jan li pana e telo tan telo suli tawa poki li seli e poki. tenpo kama la poki li jo e telo ala e namako walo.",
    "nanpa": "ala en wan en tu li nanpa. ken la luka en mute en ale li nanpa.\ntenpo pini la ijo nanpa wan li kama. tenpo ni la ijo nanpa tu li kama. tenpo kama la ijo nanpa tu wan li kama.",
    "nasa": "jan nasa li toki insa e ni: “ijo li lon.” jan mute li sona e ni: ijo ni li lon ala. tan ni la ken la jan nasa li pali e ike.\njan nasa li lukin kama e ni: jan ante li toki e ni: “a a a!”\njan nasa li ken ala kama sona e ijo mute.\njan li pakala e kili li pana e telo suwi tawa poki. tenpo kama suli la telo ni li kama telo nasa. jan li moku e telo nasa la ona li kama nasa.",
    "nasin": "**sina pali e ona kepeken nasin seme?** sina pali e ijo mute. tan ni la ona li kama. ijo mute ni li seme?\nkulupu jan li pilin e ijo sama li pali e ijo sama la ijo ni li nasin pi kulupu ni.\njan li ken tawa ma wan tan ma ante lon nasin.",
    "nena": "nena jan li lon sinpin ona lon sewi uta. jan li ken kon kepeken nena ona.\nnena li ma. ma ante li lon poka nena la selo ona li lon anpa pi selo nena.",
    "ni": "mi pilin e ijo. mi pilin ala e ijo ante. mi pilin e ijo ni.",
    "nimi": "jan li toki e nimi mute. nimi ni li kalama. nimi ni li ale toki.\njan ale li jo e nimi. jan li wile toki e jan ante wan la ona li toki e nimi ona.",
    "o": "**sina o moku!** mi wile e ni: sina moku.\n**o moku!** sina o moku!\n**sina o!** sina o kute e mi!",
    "oko": "oko mi li lukin mi.",
    "olin": "**mi olin e ona.** mi wile lon poka ona lon tenpo suli. mi lukin e ona la ni li pona tawa mi. mi wile e ni: ona li pilin pona.",
    "ona": "ona li pali. ijo ni anu jan ni li pali.",
    "open": "mi open pali e ona. tenpo pini lili la mi pali ala e ona. taso mi pali e ona lon tenpo ni lon tenpo kama.\nmi open e ona. mi tawa e wan ona. tan ni la ijo ante li ken tawa insa ona.\nmi open e ilo. mi tan e ni: ilo li open pali.\ntenpo suno open la jan li ken lukin e suno lon sewi. taso tenpo pini lili la ona li ken ala lukin e suno lon sewi.",
    "pakala": "**mi pakala e ona.** mi pali e ike tawa ona. ni la ona li kama ike. ken la ona li ken ala pali lon tenpo ni.\n**mi kama e pakala.** mi kama e ike, taso mi lukin ala kama e ona.",
    "pali": "**mi pali e ilo.** mi pali kepeken ijo mute. tan ni la ijo ni li kama wan li kama ilo.",
    "pan": "pan li kiwen lili li kama suli lon insa kili. tenpo kama la pan li lon insa ma la ona li lon e kasi kili.\njan li pali e pan kepeken nasin ni: pan en telo li kama wan li seli li kama kiwen. jan mute li moku e pan.",
    "pana": "**mi pana e ona lon ni.** tenpo pini la ona li lon ni ala. taso mi tawa e ona. ni la ona li lon ni.\n**mi pana e ona tawa jan.** mi kama e ni: jan li jo e ona.\n**mi pana e ona tawa ma ante.** mi tawa ma ante e ona, taso mi tawa ma ante ala.\n**mi pana e telo lukin.** telo li tawa weka tan lukin mi.\n**mi pana e kon.** mi tawa insa sijelo e kon. mi tawa weka e kon.",
    "pi": "mi moku kepeken uta mi. jan ante li moku kepeken uta pi jan ante.",
    "pilin": "jan li pali e ike tawa mi la mi pilin ike. jan li pana e pona tawa mi la mi pilin pona.\npilin jan li wan sijelo li tawa insa sijelo e telo sijelo loje.\n**mi pilin e ona.** mi toki insa e ona.",
    "pimeja": "tenpo pimeja la suno li lon ala.\nijo pimeja li lukin sama sewi lon tenpo pimeja.\nsuno ala li lon la mi lukin e pimeja taso.",
    "pini": "pini palisa li wan palisa. palisa li jo e pini tu taso. pini wan li weka tan pini ante.\n**mi pini moku.** tenpo pini lili la mi moku. taso tenpo ni la mi moku ala.\n**mi pini e ona.** mi tawa e wan ona. tan ni la ijo ante li ken ala tawa insa ona.\n**mi pini e ilo.** mi kama e ni: ilo li pini pali.\n**sina toki la tenpo pini la mi moku.** mi moku la tenpo kama la sina toki.\ntenpo pini la mama mi li lon e mi.",
    "pipi": "pipi li sama soweli, taso pipi li lili mute li jo e selo kiwen e noka mute.",
    "poka": "**mi lon poka ona.** mi weka ala tan ona.",
    "poki": "poki li ilo. jan li pali e poki tan ni: ijo ante li ken lon insa poki. jan li wile e ni.\njan li pana e telo lon insa poki li moku e telo ni.",
    "pona": "**ona li pona.** ona li ike ala.\nijo li pona tawa mi la mi wile e ona.",
    "pu": "**mi pu.** mi kepeken lipu pi toki pona.",
    "sama": "**ona li lukin sama pipi.** mi lukin e ni li toki insa e ni: “ona li sama pipi.”\n**mi en sina li sama.** mi sama sina. sina sama mi.\nmama mi li sama mama pi jan sama mi.",
    "seli": "seli li lon la telo li kama kon.\nijo seli li pilin sama seli.\nseli wawa li suno.",
    "selo": "selo jan li wan sijelo. ijo ante li ken pilin e selo li ken ala pilin e insa sijelo.\n**ona li lon selo mi.** ona li pilin e selo mi.",
    "seme": "mi toki e ni: “seme li lon?” sina toki e ni: “ala li lon.”\n**jan li pali e seme?** jan li pali e ijo. mi wile sona e ijo ni.\n**ona li moku anu seme?** mi wile sona e ni: ona li moku ala moku?.\n**sina moku tan seme?** tan pi moku sina li seme?\n**sina pali kepeken nasin seme?** sina pali kepeken nasin. nasin ni li seme?",
    "sewi": "**mi lon sewi ona.** ona li lon anpa mi.\nsewi li ma suli lon sewi pi ma jan.\njan mute li pilin e ni: sewi li lon li pona li sama jan li jo ala e sijelo li moli ala li lon e ale.",
    "sijelo": "wan mi li ken pilin e ijo ante. wan ante li lon insa mi. sijelo mi li wan ni ale.",
    "sike": "nena ala li lon selo sike. insa sike li weka sama tan wan ale pi selo sike.\n**mi sike e ona.** mi tawa sinpin ona. mi tawa poka ona wan. mi tawa monsi ona. mi tawa poka ona ante. mi tawa sinpin ona.",
    "sin": "**ijo sin li lon ni.** tenpo pini lili la ijo li lon ni. taso tenpo ni la ijo ni en ijo ante sin ni li lon ni.\n**ona li sin.** tenpo pini lili la ijo li lon e ona.",
    "sina": "jan li toki e ni tawa soweli: “sina moku.” jan li toki. toki ona la soweli moku.",
    "sinpin": "tenpo mute la jan li kepeken ijo la sinpin ona li lon poka pi jan ni.\ntenpo mute la ijo li tawa mi la mi ken lukin e sinpin ona taso.\nsinpin jan li sinpin pi lawa ona.\nsinpin li sama supa, taso sinpin li len e poka ale tomo.",
    "sitelen": "**mi sitelen e pipi.** mi pilin e lipu kepeken ilo. tan ni la wan pi selo lipu li kama kule ante. ni la lipu ni li lukin sama pipi li sitelen pipi.\n**mi sitelen e nimi.** mi sitelen. jan ante li lukin e sitelen ni la ona li toki insa e nimi ni.",
    "sona": "**mi sona e nimi.** jan li toki e nimi tawa mi la ona li wile e ni: mi pilin e ijo. mi sona e ijo ni.\n**mi sona pali e ona.** mi sona e ni: mi ken pali e ona kepeken nasin seme?\n**mi pana e sona tawa sina.** mi kama e ni: sina kama sona.\njan sona li sona e ijo mute.\n**mi sona e ona.** tenpo pini la mi lukin e ona li sona e ijo mute ona.",
    "soweli": "soweli li ken pilin li ken wile li ken tawa ma ante.\nlinja mute li lon selo soweli. mama meli soweli li pana e telo mama.",
    "suli": "sinpin pi ijo suli li weka tan monsi ona.\n**ona li suli.** mi pali lili taso la mi ken ala tawa e ona. taso mi pali mute la ken la mi ken tawa e ona. tawa pi ijo suli li pali ike.\n**ona li suli.** ona li ken kama e wile mi.\ntenpo pini la jan suli li jan lili. taso ona li kama suli. ni la ona li suli.",
    "suno": "suno li lon ala la jan li ken ala lukin.\nsuno li ijo suli walo lon sewi.",
    "supa": "wan pi telo suli li pilin e kon. supa li lukin sama wan ni.",
    "suwi": "moku suwi li pona tawa uta.\nkon suwi li pona tawa nena.\nsoweli suwi li pona tawa lukin.",
    "tan": "**mi moli tan ni: mi moku ala.** mi moku ala la mi moli. mi moku ala. mi moli.\n**mi tan ona."" ona li kama tan mi.\n**mi tawa ma ni tan ma ante.** tenpo pini la mi lon ma ante. taso mi tawa. ni la mi lon ma ni.",
    "taso": "**ijo nanpa wan li lon, taso ijo nanpa tu li lon ala.** mi toki e ni: “ijo nanpa wan li lon.” ken la sina kute e ni la sina pilin e ni: “ijo nanpa tu li lon.” wile mi la sina sona e ni: ijo nanpa tu li lon ala. ni la mi toki e ni: “taso ijo nanpa tu li lon ala.”\n**mi jo e ona taso.** mi jo e ona e ijo ante ala.",
    "tawa": "**mi tawa ona.** tenpo pini la mi weka tan ona. taso mi tawa. ni la mi lon poka ona.\n**mi tawa e ona.** mi kama e ni: ona li tawa.\n**ona li pona tawa mi.** mi pilin e ni: ona li pona.\n**mi tawa anpa.** tenpo pini la mi lon ma. taso mi tawa. ni la mi lon anpa pi ma ni.",
    "telo": "jan li ken lukin e telo mute lon ma. jan li lon insa telo la telo li ken pilin e selo ona ale.\ntelo li lon insa poki la lupa lili li lon anpa poki la telo li tawa anpa li tawa weka tan poki.",
    "tenpo": "jan li toki e ni: “tenpo ni la soweli li moku.” tenpo la jan li toki. toki ona la soweli li moku lon tenpo sama.\ntenpo suno la suno li lon. tenpo pimeja la suno li lon ala.",
    "toki": "jan mute li toki kepeken uta ona.\nsina lukin e nimi mi. mi sitelen e nimi ni kepeken toki pona.\n**toki!** mi lon. mi ken kute e sina. mi wile toki tawa sina.\n**mi toki insa e ona.** mi taso li kute e ni: mi toki e ona. taso mi toki uta ala.",
    "tomo": "jan li ken lon insa tomo. jan li pali e tomo tan ni.",
    "tu": "wan en wan li tu.\n**mi tu e ona.** mi kama e ni: ona li kama tu. ni la mi ken weka e wan ona tan wan ante ona.",
    "unpa": "tenpo mute la meli wan en mije wan li ken lon e jan lili kepeken unpa.",
    "uta": "uta jan li wan sijelo. jan li ken moku li ken toki kepeken uta ona.",
    "utala": "**mi utala e ona.** mi tawa wawa e kiwen tawa ona. kiwen tawa li pilin wawa e ona. ken la mi pakala e ona tan ni.\n**mi utala e ona.** ona li pali lili. mi lukin pali mute.\n**mi toki utala tawa sina.** mi lukin lawa e sina kepeken toki. ken la mi tu li pilin ike tan ni.\njan utala li moli e jan utala ante.",
    "walo": "telo mama li walo.",
    "wan": "**jan wan li lon ni.** jan ni taso li lon ni. jan li tu ala li mute ala\n**mi wan.** mi taso li lon ni.",
    "waso": "waso li sama soweli, taso waso li jo ala e linja sama soweli li jo e linja lipu e noka tu taso. waso mute li ken tawa kon lon tenpo suli kepeken tawa wawa pi linja lipu ona.",
    "wawa": "jan wawa li ken tawa e ijo suli.\njan li ken ala lukin e wawa, taso wawa li kon ala. wawa li ken tawa insa pi linja kiwen. wawa li ken lon e seli e tawa e suno. ilo mute li kepeken wawa.",
    "weka": "**mi weka tan ona.** mi lon poka ona ala.\n**mi tawa weka tan ona.** tenpo pini la mi lon poka ona. taso mi tawa. ni la mi weka tan ona.\n**mi weka e ona.** mi kama e ni: ona li tawa weka.\nijo weka li lon ni ala.",
    "wile": "**mi wile e ona.** mi jo e ona la mi pilin pona. mi jo ala e ona la mi pilin ike.\n**mi wile moku e ona.** mi wile e ni: mi moku e ona."
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
        """Displays the definition and etymology of a word or words. Entries taken from *nimi ale pona* and *lipu nimi pi toki pona taso.*\n\nEntries were edited in both cases. For *nimi ale pona*, the only revisions were formatting. For *lipu nimi pi toki pona taso*, several grammatical corrections and stylistic changes were made."""
        if ctx.channel.id in {316063418253705229, 716768435081576448, 716768463791718490, 716768500659781642, 716768537729040387, 716768591864791100, 716768624085303297}:
            if len(words) == 0:
                await ctx.send('o toki e nimi a.')
                return
            if len(words) > 10:
                await ctx.send('mute nimi pi toki sina li ike. mi wile ala toki e ona ale.')
                return
            for i in words:
                try:
                    await ctx.send(tpt_dict[i])
                except KeyError:
                    if i in tp_words:
                        await ctx.send(f'mi pakala, toki pona la mi sona taso e nimi pu. ni la mi ken ala toki e kon pi nimi "{i}".')
                    else:
                        await ctx.send(f'mi sona ala e nimi "{i}".')
        else:
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

    @commands.command(aliases=['k', 'kpnn'])
    async def kon_pi_nimi_ni(self, ctx, *words):
        "sina toki e ni la mi toki e kon pi nimi pi toki sina. jan Kaje li kama e toki ni tan *lipu nimi pi toki pona taso.* ona li ante lili e toki ona.\nni li jo ala e nimi ale pona. sina wile e kon pi nimi pi pu ala la sina o pali e ona o pana e ona tawa jan Kaje."
        if len(words) == 0:
            await ctx.send('o toki e nimi a.')
            return
        if len(words) > 10:
            await ctx.send('mute nimi pi toki sina li ike. mi wile ala toki e ona ale.')
            return
        for i in words:
            try:
                await ctx.send(tpt_dict[i])
            except KeyError:
                if i in tp_words:
                    await ctx.send(f'mi pakala, toki pona la mi sona taso e nimi pu. ni la mi ken ala toki e kon pi nimi "{i}".')
                else:
                    await ctx.send(f'mi sona ala e nimi "{i}".')
    
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

    @commands.command(aliases=['s', 'sp', 'sitelenpona', 'sitelen_pona'])
    async def sitelen(self, ctx, *, text, border=4, bg='white', fg='black'):
        """Displays the given text in sitelen pona. Currently only supports linja pona 4.2"""
        try:
            border = int(border)
            font = ImageFont.truetype(font=os.path.dirname(os.path.abspath(__file__))+'\\spfonts\\linja-pona-4.2.otf')
            size = font.getsize(text)
            for i in size:
                i = i + 2*border
            img = Image.new('RGB', size, color=bg)
            draw = ImageDraw.Draw(img)
            draw.text((border, border), text, fill=fg, font=font)
            await ctx.send(img)
        except Exception as e:
            await ctx.send(e)

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