import random as rd

def random_num(max_num):
    return rd.randint(0, max_num -1)

pronouns =
['it','I','you','he','they','we','she','who','them','me','him','one','her','us','something','nothing','anything','himself','everything','someone','themselves','everyone','itself','anyone','myself']
auxiliaryverbs =
['can','could','do','have','may','might','must','shall','should','will','would']
verbs = ['am', 'is', 'are',
'be','have','say','get','make','go','know','take','see','come','think','look','want','give','use','find','tell','ask','work','seem','feel','try','leave','call']
nouns =
['area','book','business','case','child','company','country','day','eye','fact','family','government','group','hand','home','job','life','lot','man','money','month','mother','Mr','night','number','part','people','place','point','problem','program','question','right','room','school','state','story','student','study','system','thing','time','water','way','we','week','woman','word','work','world','year']
adjectives =
['good','new','first','last','long','great','little','own','other','old','right','big','high','different','small','large','next','early','young','important','few','public','bad','same','able']
adverbs =
['up','so','out','just','now','how','then','more','also','here','well','only','very','even','back','there','down','still','in','as','too','when','never','really','most']


count_prons = len(pronouns)
count_auxvs = len(auxiliaryverbs)
count_verbs = len(verbs)
count_nouns = len(nouns)
count_adjs = len(adjectives)
count_advs = len(adverbs)

for x in range(10)
    rand_pron_id = random_num(count_prons)
    rand_auxv_id = random_num(count_auxvs)
    rand_verb_id = random_num(count_verbs)
    rand_noun_id = random_num(count_nouns)
    rand_adj_id = random_num(count_adjs)
    rand_adv_id = random_num(count_advs)

    sentence = pronouns[rand_pron_id] + " " +
    auxiliaryverbs[rand_auxv_id] + " " + verbs[rand_auxv_id] + " " +
    nouns[rand_noun_id] + " " + adjectives[rand_adj_id] + " " + adverbs[rand_adv_id]

pronoun = rd.randint(0,len(pronouns)-1).capitalize()
auxil = rd.randint(0,len(auxiliaryverbs)-1)
verb = rd.randint(0,len(verbs)-1)
noun = rd.randint(0,len(nouns)-1)
adjec = rd.randint(0,len(adjectives)-1)
adverb = rd.randint(0,len(adverbs)-1)

list= [pronoun, auxil,verb,noun,adjec,adverb]
output= ' '.join(list)
print(output)
