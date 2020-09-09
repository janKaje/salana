import discord
from discord.ext import commands, tasks
import json
import os
import re
from emoji import demojize
from PIL import Image, ImageFont, ImageDraw, ImageColor
from random import choice
from copy import deepcopy

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(tokipona(client))

class tokipona(commands.Cog, name='TOKI PONA'):

    '''A module for toki pona servers.'''

    def __init__(self, client):
        self.client = client
        self.tpwords = {'isipin', 'je', 'ki', 'n', 'teje', 'to', 'wa', 'wekama', 'ini', 'te', 'ike', 'kalama', 'kuntu', 'ipi', 'meli', 'awen', 'anu', 'pimeja', 'loku', 'nasa', 'okepuma', 'lete', 'o', 'soweli', 'pomotolo', 'peta', 'en', 'jatu', 'pipi', 'sona', 'lape', 'mije', 'mun', 'likujo', 'kan', 'namako', 'wawajete', 'mi', 'mu', 'lupa', 'kamalawala', 'palisa', 'ale', 'monsuta', 'li', 'jans', 'ete', 'peto', 'po', 'kulupu', 'ni', 'luka', 'len', 'pata', 'pa', 'pi', 'tawa', 'musi', 'ma', 'kala', 'sama', 'moku', 'alu', 'mute', 'jalan', 'jelo', 'jami', 'misikeke', 'nun', 'soto', 'powe', 'monsi', 'linluwi', 'sinpin', 'sewi', 'patu', 'loje', 'lili', 'ante', 'ten', 'lanpan', 'ijo', 'tu', 'pasila', 'sin', 'weka', 'majuna', 'wan', 'apeja', 'nuwa', 'kama', 'alasa', 'tuli', 'mijomi', 'se', 'la', 'ewe', 'insa', 'oko', 'tan', 'utala', 'kijetesantakalu', 'toki', 'tenpo', 'lenke', 'pana', 'we', 'kule', 'waleja', 'slape', 'poki', 'pona', 'pakala', 'pipo', 'wawa', 'kepeken', 'jan', 'seme', 'walo', 'wuwojiti', 'itomi', 'anpa', 'open', 'suli', 'jo', 'wile', 'ken', 'noka', 'jaku', 'pu', 'uta', 'su', 'lokon', 'epiku', 'lon', 'suwi', 'nimi', 'omen', 'nu', 'pan', 'ilo', 'ali', 'tomo', 'akesi', 'poka', 'mani', 'olin', 'ona', 'taso', 'samu', 'nanpa', 'lukin', 'suno', 'san', 'tonsi', 'waso', 'laso', 'sitelen', 'pini', 'kasi', 'sina', 'ala', 'mama', 'pake', 'kiwen', 'esun', 'pilin', 'supa', 'yupekosi', 'oke', 'mulapisu', 'kili', 'sijelo', 'kipisi', 'jasima', 'sike', 'nena', 'selo', 'polinpin', 'unpa', 'a', 'telo', 'jaki', 'e', 'wi', 'moli', 'pali', 'kin', 'kapesi', 'leko', 'omekapo', 'kapa', 'take', 'kulu', 'lipu', 'ko', 'nasin', 'lawa', 'neja', 'ke', 'kon', 'seli', 'iki', 'soko', 'sikomo', 'linja', 'kajo', 'kute', 'melome'}
        self.tp_dict = {
            'a': '***a*** – *~pu~* (emphasis, emotion or confirmation) {see ***kin***}\n\t←? onomatopoeia',
            'akesi': '***akesi*** – *~pu~* non-cute animal; reptile, amphibian\n\t← Dutch *hagedis* ‘lizard’',
            'ala': '***ala*** – *~pu~* no, not, zero; [~ *ala* ~] (used to form a yes-no question)\n\t← Georgian არა *ara* ‘no’',
            'alasa': '***alasa*** – *~pu~* to hunt, forage | *~alt. usage~* (pv.) try to {see ***lukin***}\n\t← Acadian French *à la chasse* ‘hunting’ ← French *chasser* ‘to hunt’',
            'ale': '***ale*** – *~pu~* all; abundant, countless, bountiful, every, plentiful; abundance, everything, life, universe; one hundred | *~alt. usage~* twenty; 100; 120\n\t← Dutch *alle* ‘all’',
            'ali': '***ali*** – *~pu~* all; abundant, countless, bountiful, every, plentiful; abundance, everything, life, universe; one hundred | *~alt. usage~* twenty; 100; 120\n\t← Dutch *alle* ‘all’',
            'alu': '***alu*** – *~post-pu~* (between the main sentence and the context phrase) {see ***la***}\n\t← toki pona \\**al* (*la* reversed)',
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
            'isipin': '***isipin*** – *~post-pu~* to think, to imagine, to believe (not in religion or philosophy), skepticality\n\t← Tagalog isipin ‘to think’',
            'itomi': '***itomi*** – *~post-pu, humorous~* Schadenfreude, indirect insult or disrespect, shade\n\t← English *hit or miss* (from the song ‘Mia Khalifa’ by iLOVEFRiDay)',
            'jaki': '***jaki*** – *~pu~* disgusting, obscene, sickly, toxic, unclean, unsanitary\n\t← English *yucky*',
            'jaku': '***jaku*** – *~post-pu~* 100 {see ***ale*** and ***ali***}\n\t← Japanese 百 *hyaku* \'100\'',
            'jalan': '***jalan*** – *~pre-pu, prop.~* foot {see ***noka***}\n\t←Finnish *jalan* ‘afoot’ (← *jalka* ‘foot’)',
            'jami': '***jami*** – *~post-pu~* eliciting a positive sensory or stimulating experience {see ***suwi***}\n\t← English *yummy*',
            'jan': '***jan*** – *~pu~* human being, person, somebody\n\t← Cantonese 人 *jan* ‘person’',
            'jans': '***jans*** – *~post-pu, humorous~* a particular group of early members of the ma pona Discord\n\t← toki pona *jan* and English -*/z/* ‘[plural]’',
            'jasima': '***jasima*** – *~post-pu~* reflect, resound, mirror, be on the opposite/polar end of\n\t← Turkish *yansıtmak* ‘to reflect, reverberate’',
            'jatu': '***jatu*** – *~post-pu~* the digit ‘1’\n\t← Cantonese 一/壹 *yāt* ‘one’',
            'je': '***je*** – *~post-pu~* [interjection] indicating excitement\n\t← English yay',
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
            'ki': '***ki*** – *~post-pu~* relative clause marker\n\t← French qui ‘who’',
            'kijetesantakalu': '***kijetesantakalu*** – *~pre-pu, humorous, word of Sonja~* any animal from the Procyonidae family, such as raccoons, coatis, kinkajous, olingos, ringtails and cacomistles\n\t← Finnish *kierteishäntäkarhu* ‘kinkajou’ ← *kierteis* ‘spiral’ + *häntä* ‘tail’ + *karhu* ‘bear’',
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
            'mulapisu': '***mulapisu*** – *~post-pu, humorous, word of Sonja~* pizza\n\t←?',
            'mun': '***mun*** – *~pu~* moon, night sky object, star\n\t← English *moon*',
            'musi': '***musi*** – *~pu~* artistic, entertaining, frivolous, playful, recreation\n\t← Esperanto *amuzi* ‘have fun’ ← French *amuser*',
            'mute': '***mute*** – *~pu~* many, a lot, more, much, several, very; quantity | *~alt. usage~* three (or more)\n\t← Esperanto *multe* ‘a lot’ ← Latin *multus*',
            'n': '***n*** – *~post-pu~* [interjection] indicating thinking or pondering; hum, humming',
            'namako': '***namako*** – *~pu~* {see ***sin***} | *~alt. usage~* embellishment, spice; extra additional\n\t← Persian نمک *namak* ‘salt’',
            'nanpa': '***nanpa*** – *~pu~* -th (ordinal number); numbers\n\t← Tok Pisin *namba* ‘number, (ordinal marker)’ ← English *number*',
            'nasa': '***nasa*** – *~pu~* unusual, strange; foolish, crazy; drunk, intoxicated\n\t← Tok Pisin *nasau* ‘stupid’',
            'nasin': '***nasin*** – *~pu~* way, custom, doctrine, method, path, road\n\t← Serbo-Croatian *начин način* ‘way, method’',
            'neja': '***neja*** – *~post-pu~* four\n\t← Finnish *neljä* ‘four’',
            'nena': '***nena*** – *~pu~* bump, button, hill, mountain, nose, protuberance\n\t← Finnish *nenä* ‘nose’',
            'ni': '***ni*** – *~pu~* that, this {see ***ona***}\n\t← Cantonese 呢 *ni* ‘this’',
            'nimi': '***nimi*** – *~pu~* name, word\n\t← Finnish *nimi* ‘name’',
            'noka': '***noka*** – *~pu~* foot, leg, organ of locomotion; bottom, lower part | *~alt. usage~* ten; twenty; negate five\n\t← Serbo-Croatian *нога noga* ‘foot, leg’',
            'nu': '***nu*** – *~post-pu, humorous~* {see ***nuwa***, ***sin***}\n\t← English *new*',
            'nun': '***nun*** – *~post-pu~* the digit ‘5’\n\t← Cantonese 五 / 伍 *ńgh* ‘five’',
            'nuwa': '***nuwa*** – *~post-pu, humorous~* {see ***nu***, ***sin***}\n\t← English *newer*',
            'o': '***o*** – *~pu~* hey! O! (vocative, imperative, or optative) {see ***li***}\n\t← Georgian -ო -*o* ‘(vocative suffix)’ & English *oh*',
            'oke': '***oke*** – *~post-pu~* (acknowledgement or acceptance) {see ***ke***}\n\t← English *okay*',
            'okepuma': '***okepuma*** – *~post-pu, humorous~* boomer, Baby Boomer, inconsiderate elder\n\t← English *okay boomer*',
            'oko': '***oko*** – *~pu~* {see ***lukin***} | *~alt. usage~* eye, ocular, visual {cf. ***lukin***}\n\t← Serbo-Croatian *око oko* ‘eye’',
            'olin': '***olin*** – *~pu~* love, have compassion for, respect, show affection to\n\t← Serbo-Croatian *волим volim* ‘I love’',
            'omekapo': '***omekapo*** – *~post-pu, humorous~* goodbye, farewell, see you later, eat a good fish\n\t← toki pona o.m.e.ka.po. ← ‘o moku e kala pona’ ← coined by janMaliku in reference to the message jan Sonja wrote on their pu during the Texas meetup',
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
            'sama': '***sama*** – *~pu~* same, similar; each other; sibling, peer, fellow; as, like\n\t← Finnish *sama* ‘same’ (← PG \\**samaz* ‘same, alike’) & Esperanto *sama* ‘same’ (← English *same*)',
            'samu': '***samu*** – *~post-pu, humorous, word of Sonja~* wanting to create new words\n\t← jan Samu, a user who attempted to propose a new word',
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
            'te': '***te*** – *~post-pu~* introduces a quote\n\t← Japanese って tte ‘quotative’',
            'teje': '***teje*** – *~post-pu~* right, the right side\n\t← Welsh de (/deː/) ‘right’',
            'telo': '***telo*** – *~pu~* water, liquid, fluid, wet substance; beverages\n\t← Acadian French *de l’eau* ‘(some) water’',
            'ten': '***ten*** – *~post-pu~* {shortened variant of ***tenpo***}\n\t← toki pona *tenpo*',
            'tenpo': '***tenpo*** – *~pu~* time, duration, moment, occasion, period, situation\n\t← Esperanto *tempo* ‘time’ ← Latin *tempus*',
            'to': '***to*** – *~post-pu~* particle closing a quote\n\t← Japanese と to ‘quotative’',
            'toki': '***toki*** – *~pu~* communicate, say, speak, talk, use language, think\n\t← Tok Pisin *tok* ← English *talk*',
            'tomo': '***tomo*** – *~pu~* indoor space; building, home, house, room\n\t← Esperanto *domo* ‘house’ ← Polish *dom*, Latin *domus*, Ancient Greek *δόμος*',
            'tonsi': '***tonsi*** – *~post pu~* trans, gender-non-conforming, non-binary {see ***meli***, ***mije***, ***kule***}\n\t← Mandarin 同志 *tóngzhì* ‘comrade (same will/purpose); LGBT+’',
            'tu': '***tu*** – *~pu~* two | *~alt. usage~* separate, cut {see ***kipisi***}\n\t← English *two* & Esperanto *du*',
            'tuli': '***tuli*** – *~pre-pu~* three {see ***san***}\n\t← English *three*',
            'unpa': '***unpa*** – *~pu~* have sexual or marital relations with\n\t←? onomatopoeia',
            'uta': '***uta*** – *~pu~* mouth, lips, oral cavity, jaw\n\t← Serbo-Croatian *уста usta* ‘mouth’',
            'utala': '***utala*** – *~pu~* battle, challenge, compete against, struggle against\n\t← Serbo-Croatian *ударати udarati* ‘strike, hit, hurt’',
            'wa': '***wa*** – *~post-pu~* [interjection] indicating awe or amazement',
            'waleja': '***waleja*** – *~post-pu~* context, topic, salience, pertinent, topical, pertain to, be relevant\n\t← Quenya *valdea* ‘of moment, important’',
            'walo': '***walo*** – *~pu~* white, whitish; light-coloured, pale\n\t← Finnish *valko*- ‘white’',
            'wan': '***wan*** – *~pu~* unique, united; one\n\t← English *one*',
            'waso': '***waso*** – *~pu~* bird, flying creature, winged animal\n\t← French *oiseau* ‘bird’',
            'wawa': '***wawa*** – *~pu~* strong, powerful; confident, sure; energetic, intense\n\t← Finnish *vahva* ‘strong, powerful, thick’',
            'wawajete': '***wawajete*** – *~post-pu, humorous~* something that appears to break the rules but doesn\'t; faux edginess, provocation\n\t← toki pona *wuwojiti* (all phonotactically unviable CV syllables in toki pona)',
            'we': '***we*** – *~post-pu~* (acts as a transition from one complete sentence to another)\n\t←Spanish *güey* ‘man’ ← English *man* (sentence tag)',
            'weka': '***weka*** – *~pu~* absent, away, ignored\n\t← Dutch *weg* ‘away, gone’',
            'wekama': '***wekama*** – *~post-pu~* leave and come back, be temporarily absent with the expectation of returning\n\t← toki pona weka kama',
            'wi': '***wi*** – *~post-pu, humorous~* we (excluding you, i.e. 1st person exclusive) {see ***mi***}\n\t← English *we*',
            'wile': '***wile*** – *~pu~* must, need, require, should, want, wish\n\t← Dutch *willen* ‘want, desire’',
            'yupekosi': '***yupekosi*** – *~post-pu, humorous, word of Sonja~* to behave like George Lucas and revise your old creative works and actually make them worse; “nobody knows how to pronounce the *y*”\n\t← ?'
        }
        self.tpt_dict = {
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
        self.linja_pona_substitutions = {
            '': {"glyph": '', "mark": ''},
            "pake": {"glyph": u"\uE696", "mark": u"\uF227"},
            "oko": {"glyph": u"\uE695", "mark": u"\uF226", "sup": u"\uE728"},
            "namako": {"glyph": u"\uE694", "mark": u"\uF225"},
            "monsuta": {"glyph": u"\uE693", "mark": u"\uF224", "mini": u"\uF004"},
            "leko": {"glyph": u"\uE692", "mark": u"\uF223"},
            "kipisi": {"glyph": u"\uE691", "mark": u"\uF222", "sup": u"\uE719"},
            "kin": {"glyph": u"\uE690", "mark": u"\uF221"},
            "wile": {"glyph": u"\uE677", "mark": u"\uF220"},
            "weka": {"glyph": u"\uE676", "mark": u"\uF219"},
            "wawa": {"glyph": u"\uE675", "mark": u"\uF218"},
            "waso": {"glyph": u"\uE674", "mark": u"\uF217"},
            "wan": {"glyph": u"\uE673", "mark": u"\uF216"},
            "walo": {"glyph": u"\uE672", "mark": u"\uF215", "mini": u"\uE825"},
            "utala": {"glyph": u"\uE671", "mark": u"\uF214", "mini": u"\uE930"},
            "uta": {"glyph": u"\uE670", "mark": u"\uF213"},
            "unpa": {"glyph": u"\uE66F", "mark": u"\uF212", "mini": u"\uE872"},
            "tu": {"glyph": u"\uE66E", "mark": u"\uF211"},
            "tomo": {"glyph": u"\uE66D", "mark": u"\uF210", "sup": u"\uF022"},
            "toki": {"glyph": u"\uE66C", "mark": u"\uF209", "sup": u"\uE725", "mini": u"\uF014"},
            "tenpo": {"glyph": u"\uE66B", "mark": u"\uF208", "base": u"\uF024", "mini": u"\uE925"},
            "telo": {"glyph": u"\uE66A", "mark": u"\uF207", "outside": u"\uE955"},
            "tawa": {"glyph": u"\uE669", "mark": u"\uF206", "base": u"\uF026", "mini": u"\uE915"},
            "taso": {"glyph": u"\uE668", "mark": u"\uF205"},
            "tan": {"glyph": u"\uE667", "mark": u"\uF204"},
            "suwi": {"glyph": u"\uE666", "mark": u"\uF203", "base": u"\uE813"},
            "supa": {"glyph": u"\uE665", "mark": u"\uF202", "base": u"\uE945"},
            "suno": {"glyph": u"\uE664", "mark": u"\uF201", "sup": u"\uE724", "mini": u"\uF038"},
            "suli": {"glyph": u"\uE663", "mark": u"\uF200"},
            "su": {"glyph": u"\uE698", "mark": u"\uF12A"},
            "soweli": {"glyph": u"\uE662", "mark": u"\uF199", "sup": u"\uE944"},
            "sona": {"glyph": u"\uE661", "mark": u"\uF198", "mini": u"\uE961"},
            "sitelen": {"glyph": u"\uE660", "mark": u"\uF197", "outside": u"\uF010", "mini": u"\uF013"},
            "sinpin": {"glyph": u"\uE65F", "mark": u"\uF196", "sup": u"\uE94A"},
            "sina": {"glyph": u"\uE65E", "mark": u"\uF195"},
            "sin": {"glyph": u"\uE65D", "mark": u"\uF194", "uppermini": u"\uE840"},
            "sike": {"glyph": u"\uE65C", "mark": u"\uF193", "outside": u"\uE913"},
            "sijelo": {"glyph": u"\uE65B", "mark": u"\uF192", "base": u"\uE941", "mini": u"\uE923"},
            "sewi": {"glyph": u"\uE65A", "mark": u"\uF191", "mini": u"\uF015"},
            "seme": {"glyph": u"\uE659", "mark": u"\uF190"},
            "selo": {"glyph": u"\uE658", "mark": u"\uF189", "base": u"\uE942"},
            "seli": {"glyph": u"\uE657", "mark": u"\uF188", "mini": u"\uE823"},
            "sama": {"glyph": u"\uE656", "mark": u"\uF187", "base": u"\uF029", "mini": u"\uE871"},
            "pu": {"glyph": u"\uE655", "mark": u"\uF186"},
            "pona": {"glyph": u"\uE654", "mark": u"\uF185", "sup": u"\uE843", "mini": u"\uF011"},
            "poki": {"glyph": u"\uE653", "mark": u"\uF184", "mini": u"\uF011"},
            "poka": {"glyph": u"\uE652", "mark": u"\uF183"},
            "pipi": {"glyph": u"\uE651", "mark": u"\uF182"},
            "pini": {"glyph": u"\uE650", "mark": u"\uF181", "base": u"\uF02A"},
            "pimeja": {"glyph": u"\uE64F", "mark": u"\uF180", "mini": u"\uE829"},
            "pilin": {"glyph": u"\uE64E", "mark": u"\uF179"},
            "pi": {"glyph": u"\uE64D", "mark": u"\uF178"},
            "pana": {"glyph": u"\uE64C", "mark": u"\uF177"},
            "pan": {"glyph": u"\uE64B", "mark": u"\uF176"},
            "palisa": {"glyph": u"\uE64A", "mark": u"\uF175", "base": u"\uE812"},
            "pali": {"glyph": u"\uE649", "mark": u"\uF174", "sup": u"\uE949"},
            "pakala": {"glyph": u"\uE648", "mark": u"\uF173", "mini": u"\uE896"},
            "open": {"glyph": u"\uE647", "mark": u"\uF172", "sup": u"\uE723"},
            "ona": {"glyph": u"\uE646", "mark": u"\uF171"},
            "olin": {"glyph": u"\uE645", "mark": u"\uF170"},
            "o": {"glyph": u"\uE644", "mark": u"\uF169"},
            "noka": {"glyph": u"\uE643", "mark": u"\uF168", "uppermini": u"\uE838"},
            "nimi": {"glyph": u"\uE642", "mark": u"\uF167", "outside": u"\uE831"},
            "ni": {"glyph": u"\uE641", "mark": u"\uF166"},
            "nena": {"glyph": u"\uE640", "mark": u"\uF165"},
            "nasin": {"glyph": u"\uE63F", "mark": u"\uF164"},
            "nasa": {"glyph": u"\uE63E", "mark": u"\uF163", "mini": u"\uE824"},
            "nanpa": {"glyph": u"\uE63D", "mark": u"\uF162", "sup": u"\uE722", "mini": u"\uE921"},
            "mute": {"glyph": u"\uE63C", "mark": u"\uF161"},
            "musi": {"glyph": u"\uE63B", "mark": u"\uF160", "sup": u"\uE721"},
            "mun": {"glyph": u"\uE63A", "mark": u"\uF159", "mini": u"\uF036"},
            "mu": {"glyph": u"\uE639", "mark": u"\uF158"},
            "monsi": {"glyph": u"\uE638", "mark": u"\uF157", "sup": u"\uE948"},
            "moli": {"glyph": u"\uE637", "mark": u"\uF156", "sup": u"\uE727"},
            "moku": {"glyph": u"\uE636", "mark": u"\uF155", "sup": u"\uE947"},
            "mije": {"glyph": u"\uE635", "mark": u"\uF154", "uppermini": u"\uE867"},
            "mi": {"glyph": u"\uE634", "mark": u"\uF153"},
            "meli": {"glyph": u"\uE633", "mark": u"\uF152", "outside": u"\uE870", "uppermini": u"\uE866"},
            "mani": {"glyph": u"\uE632", "mark": u"\uF151"},
            "mama": {"glyph": u"\uE631", "mark": u"\uF150", "upper": u"\uE864", "uppermini": u"\uE865"},
            "ma": {"glyph": u"\uE630", "mark": u"\uF149", "base": u"\uF020", "mini": u"\uF012"},
            "lupa": {"glyph": u"\uE62F", "mark": u"\uF148", "sup": u"\uE950"},
            "lukin": {"glyph": u"\uE62E", "mark": u"\uF147", "base": u"\uE726"},
            "luka": {"glyph": u"\uE62D", "mark": u"\uF146", "base": u"\uE850", "sup": u"\uE851", "uppermini": u"\uE837"},
            "lon": {"glyph": u"\uE62C", "mark": u"\uF145", "base": u"\uF028"},
            "loje": {"glyph": u"\uE62B", "mark": u"\uF144", "mini": u"\uE828"},
            "lipu": {"glyph": u"\uE62A", "mark": u"\uF143"},
            "linja": {"glyph": u"\uE629", "mark": u"\uF142", "base": u"\uE842"},
            "lili": {"glyph": u"\uE628", "mark": u"\uF141", "sup": u"\uF065", "mini": u"\uE800"},
            "li": {"glyph": u"\uE627", "mark": u"\uF140"},
            "lete": {"glyph": u"\uE626", "mark": u"\uF139", "mini": u"\uE801"},
            "len": {"glyph": u"\uE625", "mark": u"\uF138", "upper": u"\uF070", "sup": u"\uE943"},
            "lawa": {"glyph": u"\uE624", "mark": u"\uF137", "sup": u"\uE946", "uppermini": u"\uE836"},
            "laso": {"glyph": u"\uE623", "mark": u"\uF136", "mini": u"\uE827"},
            "lape": {"glyph": u"\uE622", "mark": u"\uF135", "sup": u"\uE720"},
            "la": {"glyph": u"\uE621", "mark": u"\uF134"},
            "kute": {"glyph": u"\uE620", "mark": u"\uF133"},
            "kulupu": {"glyph": u"\uE61F", "mark": u"\uF132"},
            "kule": {"glyph": u"\uE61E", "mark": u"\uF131", "mini": u"\uE819"},
            "kon": {"glyph": u"\uE61D", "mark": u"\uF130", "outside": u"\uE830"},
            "ko": {"glyph": u"\uE61C", "mark": u"\uF129"},
            "kiwen": {"glyph": u"\uE61B", "mark": u"\uF128"},
            "kili": {"glyph": u"\uE61A", "mark": u"\uF127"},
            "kepeken": {"glyph": u"\uE619", "mark": u"\uF126"},
            "ken": {"glyph": u"\uE618", "mark": u"\uF125"},
            "kasi": {"glyph": u"\uE617", "mark": u"\uF124", "base": u"\uE805", "sup": u"\uF021", "mini": u"\uE818"},
            "kama": {"glyph": u"\uE616", "mark": u"\uF123", "base": u"\uF025"},
            "kalama": {"glyph": u"\uE615", "mark": u"\uF122"},
            "kala": {"glyph": u"\uE614", "mark": u"\uF121"},
            "jo": {"glyph": u"\uE613", "mark": u"\uF120"},
            "jelo": {"glyph": u"\uE612", "mark": u"\uF119", "mini": u"\uE826"},
            "jan": {"glyph": u"\uE611", "mark": u"\uF118", "uppermini": u"\uE835"},
            "jaki": {"glyph": u"\uE610", "mark": u"\uF117", "mini": u"\uE820"},
            "insa": {"glyph": u"\uE60F", "mark": u"\uF116"},
            "ilo": {"glyph": u"\uE60E", "mark": u"\uF115", "base": u"\uE718"},
            "ike": {"glyph": u"\uE60D", "mark": u"\uF114", "base": u"\uF062", "mini": u"\uE919"},
            "ijo": {"glyph": u"\uE60C", "mark": u"\uF113"},
            "esun": {"glyph": u"\uE60B", "mark": u"\uF112"},
            "en": {"glyph": u"\uE60A", "mark": u"\uF111"},
            "e": {"glyph": u"\uE609", "mark": u"\uF110"},
            "awen": {"glyph": u"\uE608", "mark": u"\uF109", "base": u"\uF027"},
            "anu": {"glyph": u"\uE607", "mark": u"\uF108"},
            "ante": {"glyph": u"\uE606", "mark": u"\uF107"},
            "anpa": {"glyph": u"\uE605", "mark": u"\uF106"},
            "ale": {"glyph": u"\uE604", "mark": u"\uF105"},
            "ali": {"glyph": u"\uE604", "mark": u"\uF105"},
            "alasa": {"glyph": u"\uE603", "mark": u"\uF104"},
            "ala": {"glyph": u"\uE602", "mark": u"\uF103", "sup": u"\uF064", "mini": u"\uE917"},
            "akesi": {"glyph": u"\uE601", "mark": u"\uF102"},
            "a": {"glyph": u"\uE600", "mark": u"\uF101"},
            "tonsi": {"glyph": u"\uE697", "mark": u"\uF228"}
        }
        self.newudspcs = dict()
        self.newdefaultglyphs = dict()
        self.tp_substitutions = {
            'A' : ['_a', '_akesi', '_ala', '_alasa', '_ale', '_ali', '_anpa', '_ante', '_anu', '_awen'],
            'E' : ['_e', '_en', '_esun'],
            'I' : ['_ijo', '_ike', '_ilo', '_insa'],
            'J' : ['_jaki', '_jan', '_jelo', '_jo'],
            'K' : ['_kala', '_kalama', '_kama', '_kasi', '_ken', '_kepeken', '_kili', '_kin', '_kiwen', '_ko', '_kon', '_kule', '_kulupu', '_kute'],
            'L' : ['_la', '_lape', '_laso', '_lawa', '_len', '_lete', '_li', '_lili', '_linja', '_lipu', '_loje', '_lon', '_luka', '_lukin', '_lupa'],
            'M' : ['_ma', '_mama', '_mani', '_meli', '_mi', '_mije', '_moku', '_moli', '_monsi', '_mu', '_mun', '_musi', '_mute'],
            'N' : ['_namako', '_nanpa', '_nasa', '_nasin', '_nena', '_ni', '_nimi', '_noka'],
            'O' : ['_o', '_oko', '_olin', '_ona', '_open'],
            'P' : ['_pakala', '_pali', '_palisa', '_pan', '_pana', '_pi', '_pilin', '_pimeja', '_pini', '_pipi', '_poka', '_poki', '_pona', '_pu'],
            'S' : ['_sama', '_seli', '_selo', '_seme', '_sewi', '_sijelo', '_sike', '_sin', '_sina', '_sinpin', '_sitelen', '_sona', '_soweli', '_suli', '_suno', '_supa', '_suwi'],
            'T' : ['_tan', '_taso', '_tawa', '_telo', '_tenpo', '_toki', '_tomo'],
            'U' : ['_unpa', '_uta', '_utala'],
            'W' : ['_walo', '_wan', '_waso', '_wawa', '_weka', '_wile']
        }
        self.particles = {'li', 'pi', 'e', 'o', 'la'}
        self.contentwords = {'kule', 'nun', 'pake', 'sona', 'take', 'suli', 'weka', 'seme', 'wi', 'likujo', 'sin', 'tonsi', 'ten', 'walo', 'pini', 'peto', 'tuli', 'nuwa', 'loje', 'kapa', 'kalama', 'open', 'ike', 'pakala', 'jaki', 'okepuma', 'kili', 'itomi', 'wile', 'soweli', 'lete', 'monsuta', 'pata', 'kala', 'ante', 'toki', 'kepeken', 'san', 'polinpin', 'suno', 'alasa', 'soko', 'anu', 'unpa', 'kijetesantakalu', 'jans', 'mi', 'pa', 'kajo', 'pona', 'wawa', 'a', 'melome', 'pimeja', 'nimi', 'neja', 'loku', 'samu', 'epiku', 'laso', 'supa', 'sama', 'nasa', 'ken', 'nena', 'pomotolo', 'iki', 'poki', 'mijomi', 'sike', 'kulupu', 'majuna', 'moku', 'palisa', 'poka', 'wan', 'kiwen', 'soto', 'kute', 'kin', 'po', 'akesi', 'sina', 'tenpo', 'wekama', 'lipu', 'jan', 'pali', 'jatu', 'seli', 'luka', 'noka', 'nu', 'jasima', 'nanpa', 'waleja', 'lanpan', 'teje', 'ini', 'isipin', 'ilo', 'esun', 'te', 'ipi', 'powe', 'to', 'ete', 'lenke', 'lon', 'insa', 'kipisi', 'awen', 'selo', 'apeja', 'mun', 'linja', 'omekapo', 'sitelen', 'ala', 'moli', 'wawajete', 'lupa', 'slape', 'se', 'pana', 'ijo', 'jo', 'mani', 'monsi', 'kuntu', 'ni', 'n', 'uta', 'tu', 'je', 'we', 'ki', 'kan', 'jaku', 'musi', 'lukin', 'su', 'mulapisu', 'jami', 'tawa', 'telo', 'nasin', 'pasila', 'lili', 'mama', 'ke', 'omen', 'waso', 'ale', 'ko', 'wuwojiti', 'tomo', 'wa', 'sewi', 'peta', 'len', 'jelo', 'pipo', 'yupekosi', 'sijelo', 'kama', 'leko', 'namako', 'alu', 'sikomo', 'linluwi', 'kulu', 'kasi', 'ona', 'ma', 'mu', 'lokon', 'jalan', 'pilin', 'olin', 'pan', 'kapesi', 'pipi', 'kamalawala', 'oke', 'lawa', 'kon', 'meli', 'mije', 'misikeke', 'ewe', 'anpa', 'sinpin', 'tan', 'suwi', 'oko', 'utala', 'lape', 'patu', 'en', 'ali', 'taso', 'pu', 'mute'}
        
    async def iftokipona(self, ctx):
        try:
            return config[str(ctx.guild.id)]['tp'] is not None
        except:
            return False

    async def tp_check(self, text):
        step1 = re.sub(r'\|\|[^\|]+\|\|', '', text, flags=re.S) #Removes things behind spoiler bars
        step2 = demojize(step1) #Turns emojis into ascii characters
        step3 = re.sub(r':[\w-]+:', '', step2) #Removes now textified emojis
        step4 = re.sub(r'https\S+', '', step3) #Removes links
        step5 = re.sub('j?[A-Z][a-z]+', '', step4) #Removes proper names
        step6 = re.sub(r'[\W_0-9]', ' ', step5) #Removes non-letter characters, such as punctuation
        step7 = await self.removeduplicates(step6) #Removes repeated letters
        step8 = re.split(r'\s+', step7) #Splits the string and prepares it for analysis
        for dj in step8:
            if dj not in self.tpwords:
                return False
        return True

    async def removeduplicates(self, s):
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

    async def compoundglyphs(self, baseword, modifiers):
        newphrase = ''
        if 'base' in self.linja_pona_substitutions[baseword] \
        and all('sup' in self.linja_pona_substitutions[m] for m in modifiers):
        
            newphrase += self.linja_pona_substitutions[baseword]['base']
            for m in modifiers:
                newphrase += self.linja_pona_substitutions[m]['sup']
                    
        elif 'outside' in self.linja_pona_substitutions[baseword] \
        and all('mini' in self.linja_pona_substitutions[m] for m in modifiers):
            newphrase += self.linja_pona_substitutions[baseword]['outside']
            for m in modifiers:
                newphrase += self.linja_pona_substitutions[m]['mini']

        elif 'upper' in self.linja_pona_substitutions[baseword] \
        and all('uppermini' in self.linja_pona_substitutions[m] for m in modifiers):
            newphrase += self.linja_pona_substitutions[baseword]['upper']
            for m in modifiers:
                newphrase += self.linja_pona_substitutions[m]['uppermini']

        else:
            newphrase += self.linja_pona_substitutions[baseword]['glyph']
            for m in modifiers:
                newphrase += self.linja_pona_substitutions[m]['mark']

        return newphrase

    async def sitelen_replacements(self, text, authorid, guildid):
        #search for fg
        authorid = str(authorid)
        guildid = str(guildid)
        fg_search = re.search(r'(fg=[^ ]+)', text)
        if fg_search:
            fg = fg_search.group(0)[3:]
            text = re.sub(r' fg=[^ ]+|fg=[^ ]+ |fg=[^ ]+', '', text)
        elif authorid in config[guildid]['tp']['udspc']:
            fg = config[guildid]['tp']['udspc'][authorid]['fg']
        else:
            fg = 'white'
        #search for bg
        bg_search = re.search(r'(bg=[^ ]+)', text)
        if bg_search:
            bg = bg_search.group(0)[3:]
            text = re.sub(r' bg=[^ ]+|bg=[^ ]+ |bg=[^ ]+', '', text)
        elif authorid in config[guildid]['tp']['udspc']:
            bg = config[guildid]['tp']['udspc'][authorid]['bg']
        else:
            bg = '#36393E'
        #search for border width
        border_search = re.search(r'(border=[^ ]+)', text)
        if border_search:
            border = border_search.group(0)[7:]
            text = re.sub(r' border=[^ ]+|border=[^ ]+ |border=[^ ]+', '', text)
        else:
            border = 5
        #search for font size
        size_search = re.search(r'(size=[^ ]+)', text)
        if size_search:
            fontsize = size_search.group(0)[5:]
            text = re.sub(r' size=[^ ]+|size=[^ ]+ |size=[^ ]+', '', text)
        else:
            fontsize = 48
        #integerifies the integers
        border = int(border)
        fontsize = abs(int(fontsize))
        #replace with single-character equivalents
        if re.search(r'<@!?\d+>', text):
            for i in config[guildid]['tp']['defaultglyphs']:
                if i in text:
                    text = re.sub(f'<@!?{i}>', config[guildid]['tp']['defaultglyphs'][i], text)
        text = await self.substitute_names(text)
        
        for phrase in re.findall(r'[a-z\-]+', deepcopy(text)):
            newphrase = ""
            
            if "-" in phrase:
                modifiers = re.split(r"\-", phrase)
                baseword = modifiers.pop(0)
                
                if baseword in self.linja_pona_substitutions \
                and all(m in self.linja_pona_substitutions for m in modifiers):

                    if baseword == 'pi':
                        picount = 1
                        for i in deepcopy(modifiers):
                            if i == '':
                                picount += 1
                                modifiers.remove(i)
                            else:
                                break
                        
                        if picount > 2:
                            newphrase += u"\uE734"
                        elif picount == 2:
                            newphrase += u"\uE733"
                        else:
                            newphrase += u"\uE730"
                        
                        if len(modifiers) == 1:
                            modifier = modifiers[0]
                            if modifier in self.linja_pona_substitutions:
                                newphrase += self.linja_pona_substitutions[modifier]['glyph']
                            else:
                                newphrase += modifier
                        elif len(modifiers) == 0:
                            newphrase = self.linja_pona_substitutions['pi']['glyph']
                        else:
                            newphrase += await self.compoundglyphs(modifiers[0], modifiers[1:])
                    
                    else:
                        newphrase += await self.compoundglyphs(baseword, modifiers)
                
                else:
                    if baseword in self.linja_pona_substitutions:
                        newphrase += self.linja_pona_substitutions[baseword]['glyph']
                    else:
                        newphrase += baseword
                    
                    for m in modifiers:
                        if m in self.linja_pona_substitutions:
                            newphrase += self.linja_pona_substitutions[m]['mark']
                        else:
                            newphrase += m
                                    
            else:
                if phrase in self.linja_pona_substitutions:
                    newphrase += self.linja_pona_substitutions[phrase]['glyph']
                else:
                    newphrase += phrase

            text = text.replace(phrase, newphrase, 1)
            
        return text, fg, bg, border, fontsize

    async def safesend(self, ctx, english, tokipona):
        if config[str(ctx.guild.id)]['tp'] == None:
            await ctx.send(english)
        elif ctx.channel.id in config[str(ctx.guild.id)]['tp']['tasochannelids']:
            await ctx.send(tokipona)
        else:
            await ctx.send(english)

    def tp_sbstitute(self, matchobj):
        return '[' + ''.join([choice(self.tp_substitutions[c]) for c in matchobj.group('name')]) + ']'

    async def substitute_names(self, text):
        return re.sub(r"\[(?P<name>[AEIJKLMNOPSTUW]*)\]", self.tp_sbstitute, text)

    async def isthepigood(self, wordlist):
        if wordlist[0] == 'pi' or wordlist[len(wordlist)-1] == 'pi' or len(wordlist) < 4:
            return False
        phrase = ' '.join(wordlist)
        piseparated = re.split(' pi ', phrase)
        piseparated.pop(0)
        for i in piseparated:
            if len(re.split(' ', i)) < 2:
                return False
        return True

    async def isproperpropername(self, wordlist):
        if wordlist[0] not in self.tpwords and wordlist[0] != '':
            return 0
        for word in wordlist[1:]:
            if word not in self.tpwords:
                if not re.fullmatch('[A-Z][a-z]+', word) and word != '':
                    return 1
                elif re.fullmatch('[a-z]+', word):
                    return word
        return 2

    async def sentenceparse(self, sentence, index):
        subjects = []
        predicates = []
        objects = []
        tempsubj = []
        temppred = []
        tempobj = []
        mode = 'subject'
        sentencetype = ''
        wordno = 0
        reason = ''
        the_sentence_is_good = True
        ordinal = lambda n: "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))

        wordlist = re.split(r'\s+', sentence)

        if wordlist[0] in ['mi', 'sina'] and wordlist[1] == 'li':
            the_sentence_is_good = False
            reason += f'Incorrect usage of li after a single mi or sina in the {ordinal(index)} sentence\n'

        #this is mostly to break up the sentence into its parts, although it does pick out a few errors
        for word in wordlist:

            #o
            if word == 'o':
                if sentencetype == 'indicative':
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of o after li in the {ordinal(index)} sentence\n'
                if wordlist[wordno-1] in {'o', 'li', 'e', 'pi'}:
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of o directly after a particle in the {ordinal(index)} sentence\n'
                if mode == 'subject' and tempsubj != []:
                    subjects.append(tempsubj)
                    tempsubj = []
                if mode == 'object' and tempobj != []:
                    objects.append(tempobj)
                    tempobj = []
                if mode == 'predicate' and temppred != []:
                    predicates.append(temppred)
                    temppred =[]
                mode = 'predicate'
                sentencetype = 'imperative'
                wordno += 1
                continue

            #li
            if word == 'li':
                if sentencetype == 'imperative':
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of li after o in the {ordinal(index)} sentence\n'
                if wordlist[wordno-1] in self.particles:
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of li directly after a particle in the {ordinal(index)} sentence\n'
                if mode == 'subject' and tempsubj != []:
                    subjects.append(tempsubj)
                    tempsubj = []
                elif mode == 'subject':
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of li at the beginning of a sentence in the {ordinal(index)} sentence\n'
                if mode == 'object' and tempobj != []:
                    objects.append(tempobj)
                    tempobj = []
                if mode == 'predicate' and temppred != []:
                    predicates.append(temppred)
                    temppred =[]
                mode = 'predicate'
                sentencetype = 'indicative'
                wordno += 1
                continue

            #e
            if word == 'e':
                if wordlist[wordno-1] in self.particles:
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of e after a particle in the {ordinal(index)} sentence\n'
                if mode == 'subject' and tempsubj != []:
                    subjects.append(tempsubj)
                    tempsubj = []
                elif mode == 'subject':
                    the_sentence_is_good = False
                    reason += f'Incorrect placement of e directly after subject or at the beginning of the sentence in the {ordinal(index)} sentence\n'
                if mode == 'predicate' and temppred != []:
                    predicates.append(temppred)
                    temppred = []
                if mode == 'object' and tempobj != []:
                    objects.append(tempobj)
                    temppobj = []
                mode = 'object'
                wordno += 1
                continue

            #en
            if word == 'en':
                if wordlist[wordno-1] in self.particles:
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of en directly after a particle in the {ordinal(index)} sentence\n'
                if mode == 'predicate':
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of en in a predicate in the {ordinal(index)} sentence\n'
                    wordno += 1
                    continue
                if mode == 'object':
                    the_sentence_is_good = False
                    reason += f'Incorrect usage of en in an object in the {ordinal(index)} sentence\n'
                    wordno += 1
                    continue
                if tempsubj == []:
                    the_sentence_is_good = False
                    reason += f'Cannot begin a sentence with en, found in the {ordinal(index)} sentence\n'
                    wordno += 1
                    continue
                subjects.append(tempsubj)
                tempsubj = []
            
            #subjects
            if mode == 'subject':
                tempsubj.append(word)
                if word in {'mi', 'sina'}:
                    mode = 'predicate'
                    subjects.append(tempsubj)
                    tempsubj = []
                    wordno += 1
                    continue
            #predicates
            if mode == 'predicate':
                temppred.append(word)
            #objects
            if mode == 'object':
                tempobj.append(word)

            wordno += 1

        if tempsubj != []:
            subjects.append(tempsubj)
        if temppred != []:
            predicates.append(temppred)
        if tempobj != []:
            objects.append(tempobj)

        #debugging code
        #print(subjects, predicates, objects)
        #print(sentence)

        #making sure all words are content words, use pi's correctly, and have proper names in the correct form and place
        #subjects
        for subject in subjects:
            if not all(i in self.contentwords for i in subject):

                if not all(i in self.tpwords for i in subject):
                    proper = await self.isproperpropername(subject)
                    if proper == 0:
                        the_sentence_is_good = False
                        reason += f'Unknown word acting as a head in a subject of the {ordinal(index)} sentence\n'
                    elif proper == 1:
                        the_sentence_is_good = False
                        reason += f'Incorrect proper name form in a subject of the {ordinal(index)} sentence\n'
                    elif isinstance(proper, str):
                        the_sentence_is_good = False
                        reason += f'Non-toki pona word {proper} used as a toki pona word in a subject of the {ordinal(index)} sentence\n'

                if 'pi' in subject:
                    if not await self.isthepigood(subject):
                        the_sentence_is_good = False
                        reason += f'Incorrect usage of pi in a subject of the {ordinal(index)} sentence\n'
                    
        #predicates
        for pred in predicates:
            if not all(i in self.contentwords for i in pred):

                if not all(i in self.tpwords for i in pred):
                    proper = await self.isproperpropername(pred)
                    if proper == 0:
                        the_sentence_is_good = False
                        reason += f'Unknown word acting as a head in a predicate of the {ordinal(index)} sentence\n'
                    elif proper == 1:
                        the_sentence_is_good = False
                        reason += f'Incorrect proper name form in a predicate of the {ordinal(index)} sentence\n'
                    elif isinstance(proper, str):
                        the_sentence_is_good = False
                        reason += f'Non-toki pona word {proper} used as a toki pona word in a predicate of the {ordinal(index)} sentence\n'

                if 'pi' in pred:
                    if not await self.isthepigood(pred):
                        the_sentence_is_good = False
                        reason += f'Incorrect usage of pi in a predicate of the {ordinal(index)} sentence\n'

        #objects
        for obj in objects:
            if not all(i in self.contentwords for i in obj):

                if not all(i in self.tpwords for i in obj):
                    proper = await self.isproperpropername(obj)
                    if proper == 0:
                        the_sentence_is_good = False
                        reason += f'Unknown word acting as a head in an object of the {ordinal(index)} sentence\n'
                    elif proper == 1:
                        the_sentence_is_good = False
                        reason += f'Incorrect proper name form in an object of the {ordinal(index)} sentence\n'
                    elif isinstance(proper, str):
                        the_sentence_is_good = False
                        reason += f'Non-toki pona word {proper} used as a toki pona word in an object of the {ordinal(index)} sentence\n'

                if 'pi' in obj:
                    if not await self.isthepigood(obj):
                        the_sentence_is_good = False
                        reason += f'Incorrect usage of pi in an object of the {ordinal(index)} sentence\n'
        
        return the_sentence_is_good, reason

    async def parsetext(self, text):
        sentences = re.split(r'[\.|\?|!|,|:] ?', re.sub('["\']', '', text))
        the_sentence_is_good = True
        reason = ''
        ordinal = lambda n: "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))
        for sentence in sentences:
            index = sentences.index(sentence)+1

            #if the string is empty, carry on
            if sentence == '':
                continue

            #DON'T CAPITALIZE SENTENCES
            if sentence[0] in 'AEIOUMNPTKSLWJ':
                the_sentence_is_good = False
                reason += f'The {ordinal(index)} sentence is incorrectly capitalized\n'

            #when there's a la
            if ' la ' in sentence:
                laphrases = re.split(' la ', sentence)
                sentencewithoutla = laphrases.pop(len(laphrases)-1)
                for phrase in laphrases:
                    words = re.findall(r'\w+', phrase)
                    if any(i in words for i in ['li', 'e']) or words[0] in ['mi', 'sina']:
                        s, r = await self.sentenceparse(phrase, index)
                        if not s:
                            the_sentence_is_good = False
                            reason += r
                    elif 'o' in words:
                        the_sentence_is_good = False
                        reason += f'Invalid o in la phrase in the {ordinal(index)} sentence\n'
                    elif 'la' in words:
                        the_sentence_is_good = False
                        reason += f'Incorrect placement of la in the {ordinal(index)} sentence\n'
                    elif 'pi' in words and not await self.isthepigood(words):
                        the_sentence_is_good = False
                        reason += f'Incorrect usage of pi in the {ordinal(index)} sentence\n'
                s, r = await self.sentenceparse(sentencewithoutla, index)
                if not s:
                    the_sentence_is_good = False
                    reason += r

            else:
                s, r = await self.sentenceparse(sentence, index)
                if not s:
                    the_sentence_is_good = False
                    reason += r
        return the_sentence_is_good, reason

    @commands.command(aliases=['k', 'kpnn'])
    async def kon_pi_nimi_ni(self, ctx, *words):
        "sina toki e ni la mi toki e kon pi nimi pi toki sina. jan Kaje li kama e toki ni tan *lipu nimi pi toki pona taso.* ona li ante lili e toki ona.\nni li jo ala e nimi ale pona. sina wile e kon pi nimi pi pu ala la sina o pali e ona o pana e ona tawa jan Kaje lon lipu GitHub."
        if not await self.iftokipona(ctx):
            return
        if len(words) == 0:
            await ctx.send('o toki e nimi a.')
            return
        if len(words) > 10:
            await ctx.send('mute nimi pi toki sina li ike. mi wile ala toki e ona ale.')
            return
        for i in words:
            if i in self.tpt_dict:
                await ctx.send(self.tpt_dict[i])
            elif i in self.tp_dict:
                await ctx.send(f'toki pona la mi sona ala e kon pi nimi ni. ni li kon ona pi toki Inli:\n{self.tp_dict[i]}')
            else:
                await ctx.send(f'mi sona ala e nimi "{i}".')

    @commands.command(aliases=['check_for_tp', 'ctp',])
    async def tpcheck(self, ctx, *, text):
        '''Checks if the input text is toki pona or not.'''
        if not await self.iftokipona(ctx):
            return
        if await self.tp_check(text):
            await self.safesend(ctx, 'toki pona confirmed. :sleepy:', 'ni li toki pona. pona a!')
        else:
            await self.safesend(ctx, ":rotating_light: Not toki pona! :rotating_light:", 'ni li toki pona ala a! o weka e ona :angry:')

    @commands.command(aliases=['g'])
    async def grammarcheck(self, ctx, *, text):
        """Runs the given text through a toki pona grammar checker. It only looks for grammatical errors, not whether or not something makes sense or is likely to be said. Currently, it doesn't allow for `pi ... en ...` structures, and considers commas as full sentence breaks."""
        if not await self.iftokipona(ctx):
            return
        s, r = await self.parsetext(text)
        if s:
            await self.safesend(ctx, 'I found no errors in this text.', 'sona mi la toki ni li pona :+1:')
        else:
            await self.safesend(ctx, f'I found it to be incorrect. Here are the errors that I found:\n{r}', f'sona mi la toki ni li ike. ni li ike toki (pi toki Inli):\n||{r}||')

    @commands.command(aliases=['s', 'sp', 'sitelenpona', 'sitelen_pona'])
    async def sitelen(self, ctx, *, text):
        """Displays the given text in sitelen pona.\n\nYou can use border=# to define border width, size=# to define font size, and fg=[color] and bg=[color] to define the text color and background color."""
        if not await self.iftokipona(ctx):
            return
        try:
            async with ctx.channel.typing():
                text, fg, bg, border, fontsize = await self.sitelen_replacements(text, ctx.author.id, ctx.guild.id)
                #loads font
                font = ImageFont.truetype(font=str(os.path.dirname(os.path.abspath(__file__)))[:-4]+'linja_pona_modified.otf', size=fontsize)
                size = font.getsize_multiline(text) #calculates size
                finalsize = (size[0]+2*border, int((size[1]+2*border)*1.1)) #adds border to size
                if finalsize[0]*finalsize[1] > 1000000:
                    await ctx.send('too big!')
                    return
                img = Image.new('RGB', finalsize, color=bg) #new image
                draw = ImageDraw.Draw(img)
                draw.text((border, border), text, fill=fg, font=font) #draws text
                img.save(str(ctx.author.id)+'.png') #saves image
            await ctx.send(file=discord.File(open(str(ctx.author.id)+'.png', 'rb')))
            os.remove(str(ctx.author.id)+'.png') #deletes image
        except Exception as e:
            await ctx.send(e)

    @commands.command(aliases=['color', 'c'])
    async def colors(self, ctx, fg, bg):
        '''Sets user-specific default color scheme for sitelen pona generation.'''
        if not await self.iftokipona(ctx):
            return
        try:
            ImageColor.getrgb(fg)
        except ValueError:
            await ctx.send(f'{fg} is an invalid color')
            return
        try:
            ImageColor.getrgb(bg)
        except ValueError:
            await ctx.send(f'{bg} is an invalid color')
            return
        config[str(ctx.guild.id)]['tp']['udspc'][str(ctx.author.id)] = {'fg': fg, 'bg': bg}
        try:
            self.newudspcs[str(ctx.guild.id)] = self.newudspcs[str(ctx.guild.id)]
        except:
            self.newudspcs[str(ctx.guild.id)] = dict()
        self.newudspcs[str(ctx.guild.id)][str(ctx.author.id)] = {'fg': fg, 'bg': bg}
        await ctx.send('Updated successfully.')

    @commands.command(aliases=['glyphs'])
    async def myglyphs(self, ctx, *, text):
        '''Sets default sitelen pona text to replace when people mention you in sitelen pona.'''
        if not await self.iftokipona(ctx):
            return
        newtext, _, _, _, _ = await self.sitelen_replacements(text, ctx.author.id, ctx.guild.id)
        if re.search(r'[a-zA-Z1-9]', newtext):
            await ctx.send('Invalid sitelen pona.')
            return
        config[str(ctx.guild.id)]['tp']['defaultglyphs'][str(ctx.author.id)] = text
        try:
            self.newdefaultglyphs[str(ctx.guild.id)] = self.newdefaultglyphs[str(ctx.guild.id)]
        except:
            self.newdefaultglyphs[str(ctx.guild.id)] = dict()
        self.newdefaultglyphs[str(ctx.guild.id)][str(ctx.author.id)] = text
        await ctx.send('Updated successfully.')
