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
        self.tp_dict = json.loads(open(f'{dir_path}/data/tp_dict.json').read())
        self.tpt_dict = json.loads(open(f'{dir_path}/data/tpt_dict.json').read())
        self.linja_pona_substitutions = json.loads(open(f'{dir_path}/data/linja_pona_substitutions.json').read())
        self.proper_names = json.loads(open(f'{dir_path}/data/proper_names.json').read())
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
        self.newudspcs = dict()
        self.newdefaultglyphs = dict()
        
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
            if dj not in self.tpwords and dj != '':
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
        """Runs the given text through a toki pona grammar checker. It only looks for grammatical errors, not whether or not something makes sense or is likely to be said."""
        if not await self.iftokipona(ctx):
            return
        reasons = []
        sentenceindex = 0

        sentences = re.split(r'[\.!\?:\n] ?|(?<! la)(?<! taso), (?!la)', text)
        for sentence in sentences:
            wordlist = re.split(r'\s+', sentence)
            wordindex = 0
            wordno = 1
            underpi = False
            pos = 'subj'
            ismodifier = False
            mood = None
            requirescontentword = False
            beginningofsent = True
            for word in wordlist:

                word = re.sub(r'\A\W|\W\Z', '', word)

                if word == '':
                    wordindex += 1
                    continue

                #Non-native tp word check
                if word not in self.tpwords:
                    if re.fullmatch('[A-Z][a-z]+', word) and ismodifier:
                        wordindex += 1
                        wordno += 1
                        requirescontentword = False
                        continue
                    elif word.lower() in self.tpwords:
                        reasons.append({'reason': f'Found incorrectly capitalized toki pona word "{word}"', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    elif re.fullmatch('[A-Z][a-z]+', word):
                        reasons.append({'reason': f'Found proper name "{word}" acting as a head', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    else:
                        reasons.append({'reason': f'Found unknown word "{word}"', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                
                #taso
                elif word == 'taso' and beginningofsent and wordlist[wordindex+1] not in {'la', 'la,'}:
                    wordindex += 1
                    wordno += 1
                    beginningofsent = False
                    continue

                #Content words
                elif word in {'kule', 'nun', 'pake', 'sona', 'take', 'suli', 'weka', 'seme', 'wi', 'likujo', 'sin', 'tonsi', 'ten', 'walo', 'pini', 'peto', 'tuli', 'nuwa', 'loje', 'kapa', 'kalama', 'open', 'ike', 'pakala', 'jaki', 'okepuma', 'kili', 'itomi', 'wile', 'soweli', 'lete', 'monsuta', 'pata', 'kala', 'ante', 'toki', 'kepeken', 'san', 'polinpin', 'suno', 'alasa', 'soko', 'anu', 'unpa', 'kijetesantakalu', 'jans', 'mi', 'pa', 'kajo', 'pona', 'wawa', 'a', 'melome', 'pimeja', 'nimi', 'neja', 'loku', 'samu', 'epiku', 'laso', 'supa', 'sama', 'nasa', 'ken', 'nena', 'pomotolo', 'iki', 'poki', 'mijomi', 'sike', 'kulupu', 'majuna', 'moku', 'palisa', 'poka', 'wan', 'kiwen', 'soto', 'kute', 'kin', 'po', 'akesi', 'sina', 'tenpo', 'wekama', 'lipu', 'jan', 'pali', 'jatu', 'seli', 'luka', 'noka', 'nu', 'jasima', 'nanpa', 'waleja', 'lanpan', 'teje', 'ini', 'isipin', 'ilo', 'esun', 'te', 'ipi', 'powe', 'to', 'ete', 'lenke', 'lon', 'insa', 'kipisi', 'awen', 'selo', 'apeja', 'mun', 'linja', 'omekapo', 'sitelen', 'ala', 'moli', 'wawajete', 'lupa', 'slape', 'se', 'pana', 'ijo', 'jo', 'mani', 'monsi', 'kuntu', 'ni', 'n', 'uta', 'tu', 'je', 'we', 'ki', 'kan', 'jaku', 'musi', 'lukin', 'su', 'mulapisu', 'jami', 'tawa', 'telo', 'nasin', 'pasila', 'lili', 'mama', 'ke', 'omen', 'waso', 'ale', 'ko', 'wuwojiti', 'tomo', 'wa', 'sewi', 'peta', 'len', 'jelo', 'pipo', 'yupekosi', 'sijelo', 'kama', 'leko', 'namako', 'alu', 'sikomo', 'linluwi', 'kulu', 'kasi', 'ona', 'ma', 'mu', 'lokon', 'jalan', 'pilin', 'olin', 'pan', 'kapesi', 'pipi', 'kamalawala', 'oke', 'lawa', 'kon', 'meli', 'mije', 'misikeke', 'ewe', 'anpa', 'sinpin', 'tan', 'suwi', 'oko', 'utala', 'lape', 'patu', 'ali', 'taso', 'pu', 'mute'}:
                    if word in {'mi', 'sina'} and beginningofsent and wordlist[wordindex+1] != 'pi':
                        if wordlist[wordindex+1] == 'li':
                            reasons.append({'reason': f'Cannot use li after a single mi or sina that acts as the subject', 'word': 'li', 'wordindex': wordindex+1, 'sentence': sentence, 'sentenceindex': sentenceindex})
                        pos = 'pred'
                    elif underpi and not ismodifier and wordlist[wordindex-1] != 'en':
                        ismodifier = True
                        requirescontentword = True
                    else:
                        ismodifier = True
                        requirescontentword = False

                #o
                elif word == 'o':
                    if mood == 'ind':
                        reasons.append({'reason': f'Cannot use o when the mood is already indicative', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    elif mood == None:
                        mood = 'imp'
                    if wordindex > 0:
                        if wordlist[wordindex-1] in {'li', 'e', 'o', 'pi'}:
                            reasons.append({'reason': f'Cannot use o directly after {wordlist[wordindex-1]}', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    pos = 'pred'
                    ismodifier = False
                    underpi = False

                #li
                elif word == 'li':
                    if mood == 'imp':
                        reasons.append({'reason': f'Cannot use li when the mood is already imperative', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    elif mood == None:
                        mood = 'ind'
                    if pos == 'subj':
                        pos = 'pred'
                    if wordindex > 0:
                        if wordlist[wordindex-1] in {'li', 'e', 'o', 'pi', 'la'}:
                            reasons.append({'reason': f'Cannot use li directly after {wordlist[wordindex-1]}', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                        elif not ismodifier and wordlist[wordindex-1] not in {'mi', 'sina'}:
                            reasons.append({'reason': f'There is no subject before a li', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    pos = 'pred'
                    ismodifier = False
                    underpi = False

                #e
                elif word == 'e':
                    if pos == 'subj':
                        reasons.append({'reason': f'No predicate found before an e', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    if wordindex > 0:
                        if wordlist[wordindex-1] in {'li', 'e', 'o', 'pi', 'la'}:
                            reasons.append({'reason': f'Cannot use e directly after {wordlist[wordindex-1]}', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    pos = 'obj'
                    ismodifier = False
                    underpi = False

                #la
                elif word == 'la':
                    if wordindex > 0:
                        if wordlist[wordindex-1] in {'li', 'e', 'o', 'pi', 'la'}:
                            reasons.append({'reason': f'Cannot use la directly after {wordlist[wordindex-1]}', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    else:
                        reasons.append({'reason': f'Cannot use la at the beginning of a sentence', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    pos = 'subj'
                    ismodifier = False
                    underpi = False
                    beginningofsent = True

                #pi
                elif word == 'pi':
                    if not ismodifier:
                        if wordindex == 0:
                            reasons.append({'reason': f'Cannot use pi to begin a sentence', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                        else:
                            reasons.append({'reason': f'Cannot use pi directly after {wordlist[wordindex-1]}', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    requirescontentword = False
                    underpi = True
                    ismodifier = False

                #en
                elif word == 'en':
                    if not ismodifier:
                        if wordindex == 0:
                            reasons.append({'reason': f'Cannot use en to begin a sentence', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                        else:
                            reasons.append({'reason': f'Cannot use en directly after {wordlist[wordindex-1]}', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    elif pos != 'subj' and not underpi:
                        reasons.append({'reason': f'Cannot use en anywhere besides in a subject or under a pi phrase', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})
                    elif underpi:
                        requirescontentword = True
                    ismodifier = False
                
                if word != 'la':
                    beginningofsent = False

                if word in {'li', 'e', 'o', 'la'} and requirescontentword:
                    reasons.append({'reason': f'pi requires at least two content words after it, unless nesting', 'word': word, 'wordindex': wordindex, 'sentence': sentence, 'sentenceindex': sentenceindex})

                wordindex += 1
                wordno += 1

            if requirescontentword:
                reasons.append({'reason': f'pi requires at least two content words after it, unless nesting', 'word': word, 'wordindex': wordindex-1, 'sentence': sentence, 'sentenceindex': sentenceindex})
            if beginningofsent and sentence != '':
                reasons.append({'reason': f'la cannot end a sentence', 'word': word, 'wordindex': wordindex-1, 'sentence': sentence, 'sentenceindex': sentenceindex})
            if not ismodifier:
                if wordlist[wordindex-1] == 'pi':
                    reasons.append({'reason': f'pi cannot end a sentence', 'word': word, 'wordindex': wordindex-1, 'sentence': sentence, 'sentenceindex': sentenceindex})
                elif wordlist[wordindex-1] == 'li':
                    reasons.append({'reason': f'li cannot end a sentence', 'word': word, 'wordindex': wordindex-1, 'sentence': sentence, 'sentenceindex': sentenceindex})
                elif wordlist[wordindex-1] == 'e':
                    reasons.append({'reason': f'e cannot end a sentence', 'word': word, 'wordindex': wordindex-1, 'sentence': sentence, 'sentenceindex': sentenceindex})
            
            sentenceindex += 1

        reasonstr = ''
        for i in reasons:
            reasonstr += i['reason']
            reasonstr += f' (in sentence number {i["sentenceindex"]+1})'
            reasonstr += '\n\n```'
            reasonstr += i['sentence']
            reasonstr += '\n'
            wordlist = re.split(r'\s+', i['sentence'])
            if 0 < i['wordindex'] < (len(wordlist)-1):
                wordmatch = re.search(f'{wordlist[i["wordindex"]-1]}\\s({i["word"]}),?\\s{wordlist[i["wordindex"]+1]}', i['sentence'])
            elif 0 < i['wordindex']:
                wordmatch = re.search(f'{wordlist[i["wordindex"]-1]}\\s({i["word"]})', i['sentence'])
            elif i['wordindex'] < (len(wordlist)-1):
                wordmatch = re.search(f'({i["word"]}),?\\s{wordlist[i["wordindex"]+1]}', i['sentence'])
            else:
                wordmatch = re.search(f'({i["word"]})', i['sentence'])
            reasonstr += ' ' * wordmatch.start(1)
            reasonstr += '^' * len(i['word'])
            reasonstr += '```\n'

        if reasonstr == '':
            await self.safesend(ctx, 'I found no errors in this text.', 'sona mi la toki ni li pona :+1:')
        else:
            await self.safesend(ctx, reasonstr, f'sona mi la toki ni li ike. ni li ike toki (pi toki Inli):\n||{reasonstr}||')

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

    @commands.command(aliases=['n', 'propername'])
    async def name(self, ctx, *, name):
        '''Gives the English equivalent of a toki pona proper name or the toki pona equivalent of an English proper name, according to the "place names" and "language names" sections in pu. Needs the "ma" or "toki" before it in order to work.'''
        if await self.iftokipona(ctx):
            await self.safesend(ctx, self.proper_names.get(name, 'Not found.'), self.proper_names.get(name, 'mi sona ala.'))
