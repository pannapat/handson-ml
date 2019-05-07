#!/usr/bin/env python
# coding: utf-8

# In[5]:


keyword_pair_dict = {
    "a|á": { "keywords": ["a","á"], "probability": 0 },
    "ais|áis": { "keywords": ["ais","áis"], "probability": 0 },
    "aisti|aistí": { "keywords": ["aisti","aistí"], "probability": 0 },
    "ait|áit": { "keywords": ["ait","áit"], "probability": 0 },
    "ar|ár": { "keywords": ["ar","ár"], "probability": 0 },
    "arsa|ársa": { "keywords": ["arsa","ársa"], "probability": 0 },
    "ban|bán": { "keywords": ["ban","bán"], "probability": 0 },
    "cead|céad": { "keywords": ["cead","céad"], "probability": 0 },
    "chas|chás": { "keywords": ["chas","chás"], "probability": 0 },
    "chuig|chúig": { "keywords": ["chuig","chúig"], "probability": 0 },
    "dar|dár": { "keywords": ["dar","dár"], "probability": 0 },
    "do|dó": { "keywords": ["do","dó"], "probability": 0 },
    "gaire|gáire": { "keywords": ["gaire","gáire"], "probability": 0 },
    "i|í": { "keywords": ["i","í"], "probability": 0 },
    "inar|inár": { "keywords": ["inar","inár"], "probability": 0 },
    "leacht|léacht": { "keywords": ["leacht","léacht"], "probability": 0 },
    "leas|léas": { "keywords": ["leas","léas"], "probability": 0 },
    "mo|mó": { "keywords": ["mo","mó"], "probability": 0 },
    "na|ná": { "keywords": ["na","ná"], "probability": 0 },
    "os|ós": { "keywords": ["os","ós"], "probability": 0 },
    "re|ré": { "keywords": ["re","ré"], "probability": 0 },
    "scor|scór": { "keywords": ["scor","scór"], "probability": 0 },
    "te|té": { "keywords": ["te","té"], "probability": 0 },
    "teann|téann": { "keywords": ["teann","téann"], "probability": 0 },
    "thoir|thóir": { "keywords": ["thoir","thóir"], "probability": 0 },
}


# In[6]:


def readfile(filename):
    file = open(filename, 'rt')
    original_text = file.read()
    file.close()
    
    return original_text


# In[7]:


def writefile(filename, content):
    file = open(filename, 'w')
    file.write(str(content))
    file.close()


# In[8]:


def preprocess_data(text, is_test=False):
    # remove punctuations !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    punctuation_list = ["!","\"","#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~","–","€","•","«","»","’","“","”","£"]
    if(is_test):
        punctuation_list.remove('{')
        punctuation_list.remove('}')
        punctuation_list.remove('|')
    for punctuation in punctuation_list:
        text = text.replace(punctuation, "")

#     remove numbers
    RE_NUMBERS = re.compile('[0-9]+')
    text = RE_NUMBERS.sub(r'', text)

    # remove emojis
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    text = RE_EMOJI.sub(r'', text) # ⛈ corcra❄ gorm❄

    # substitute multiple spaces with a single space
    text = re.sub(' +', ' ', text)
    
    # trim leading and trailing spaces
    text = text.strip()

    # normalize text to lower case
    text = text.lower()
    
    return text


# In[9]:


def count_unigram(text):
    count_dict = {}
    unigram_words = text.split()

    for word in unigram_words:
        if word in count_dict:
            count_dict[word] += 1
        else:
            count_dict[word] = 1
    return count_dict


# In[10]:


def count_bigram(text):
    count_dict = {}
    sentences = text.split('\n')

    for sentence in sentences:
        
        # trim leading and trailing spaces
        sentence = sentence.strip()
        
        bigram_words = sentence.split()

        for i in range(len(bigram_words)):

            if i == 0:
                # a word with nothing preceding
                preceding_word = "^";
            else:
                 # normal pairs of words   
                preceding_word = bigram_words[i-1];

            bigram = preceding_word + " " + bigram_words[i]

            if bigram in count_dict:
                count_dict[bigram] += 1
            else:
                count_dict[bigram] = 1

        # count when the word is the last word of the sentence
        bigram = bigram_words[-1] + " $"
        if bigram in count_dict:
            count_dict[bigram] += 1
        else:
            count_dict[bigram] = 1
    return count_dict


# In[11]:


def calculate_unigram_prob():
    for key in keyword_pair_dict:
        word_1 = keyword_pair_dict[key]["keywords"][0]
        word_2 = keyword_pair_dict[key]["keywords"][1]

        prob_word_1 = unigram_count_dict[word_1]
        prob_word_2 = unigram_count_dict[word_2]

        normalized_prob_word_1 = prob_word_1 / (prob_word_1 + prob_word_2)

        keyword_pair_dict[key]["probability"] = normalized_prob_word_1


# In[ ]:





# In[12]:


def calculate_bigram_prob(sentence):
    
    start_index = sentence.find("{")
    end_index = sentence.find("}")
    
    word_choice = sentence[(start_index+1):end_index] # "thoir|thóir"

    if word_choice:
        [word_choice_1, word_choice_2] = word_choice.split('|'); # word_choice_1 = "thoir" and word_choice_2 = "thóir"

        words = sentence.split();
        index = words.index("{" + word_choice + "}")
        if index == 0:
            prev_word = "^"
            next_word = words[1]

        elif index == len(words)-1:
            prev_word = words[index - 1]
            next_word = "$"

        else:
            prev_word = words[index - 1]
            next_word = words[index + 1]

        # E.g. Tá Dora agus Bróigín ar {thoir|thóir} réalt-ainmhithe in éineacht le Pegaso.
        # p1 = P(thoir|ar) * P(réaltainmhithe|thoir) 
        # c1 = count("ar thoir") * counbt("thoir réaltainmhithe")

        # p2 = P(thòir|ar) * P(réaltainmhithe|thòir)
        # c2 = count("ar thòir") * count("thòir réaltainmhithe")
        # P(thoir) = p1/(p1+p2)
        # P(thoir) = c1/(c1+c2)

        word_1_bigram_1 = prev_word + " " + word_choice_1 # "ar thoir"
        word_1_bigram_2 = word_choice_1 + " " + next_word # "thoir réaltainmhithe"

        word_2_bigram_1 = prev_word + " " + word_choice_2 # "ar thòir"
        word_2_bigram_2 = word_choice_2 + " " + next_word # "thòir réaltainmhithe"

        count_word_1_bigram_1 = bigram_count_dict[word_1_bigram_1] if word_1_bigram_1 in bigram_count_dict else 0
        count_word_1_bigram_2 = bigram_count_dict[word_1_bigram_2] if word_1_bigram_2 in bigram_count_dict else 0

        count_word_2_bigram_1 = bigram_count_dict[word_2_bigram_1] if word_2_bigram_1 in bigram_count_dict else 0
        count_word_2_bigram_2 = bigram_count_dict[word_2_bigram_2] if word_2_bigram_2 in bigram_count_dict else 0
        
        count_prev_word = unigram_count_dict[prev_word] if prev_word in unigram_count_dict else 0
        count_next_word = unigram_count_dict[next_word] if next_word in unigram_count_dict else 0
        count_keyword_1 = unigram_count_dict[word_choice_1] if word_choice_1 in unigram_count_dict else 0
        count_keyword_2 = unigram_count_dict[word_choice_2] if word_choice_2 in unigram_count_dict else 0
        
        p_word_1_bigram_1 = (count_word_1_bigram_1 + K) / (count_prev_word + (K*V)) # "ar thoir"
        p_word_1_bigram_2 = (count_word_1_bigram_2 + K) / (count_keyword_1 + (K*V)) # "thoir réaltainmhithe"
        
        p_word_2_bigram_1 = (count_word_2_bigram_1 + K) / (count_prev_word + (K*V)) # "ar thòir"
        p_word_2_bigram_2 = (count_word_2_bigram_2 + K) / (count_keyword_2 + (K*V)) # "thòir réaltainmhithe"
        
        p1 = (p_word_1_bigram_1 * p_word_1_bigram_2)
        p2 = (p_word_2_bigram_1 * p_word_2_bigram_2)
        
        prob_word_choice_1 = p1 / (p1 + p2)
        
    return prob_word_choice_1


# In[25]:


def generate_submission_unigram():
    test_text = readfile('test.txt')
    test_text = preprocess_data(test_text, True)
    
    test_sentences = test_text.split("\n");
    test_word_choices = []
    answer_list = ["Id,Expected"]
    running_number = 1
    
    for sentence in test_sentences:
        start_index = sentence.find("{")
        end_index = sentence.find("}")

        word_choice = sentence[(start_index+1):end_index] # "thoir|thóir"

        if word_choice:
            [word_choice_1, word_choice_2] = word_choice.split('|');
            
            prob = keyword_pair_dict[word_choice]["probability"]
            answer_list.append("{},{}".format(running_number, prob))
            
            running_number += 1
        answer = "\n".join(answer_list)
    return answer


# In[19]:


def generate_submission_bigram():
    test_text = readfile('test.txt')
    test_text = preprocess_data(test_text, True)

    test_sentences = test_text.split("\n")
    answer_list = ["Id,Expected"]
    running_number = 1
    for test_sentence in test_sentences:
        if test_sentence:
            prob = calculate_bigram_prob(test_sentence)

            answer_list.append("{},{:.20f}".format(running_number, prob))
            running_number += 1
    answer = "\n".join(answer_list)
    return answer


# In[23]:


import re

text = readfile('train.txt')

text = preprocess_data(text)

unigram_count_dict = count_unigram(text)
calculate_unigram_prob()

bigram_count_dict = count_bigram(text)

K = 0.5
N = len(text.split())
V = len(unigram_count_dict)


# In[26]:


generate_submission_unigram()


# In[27]:


# writefile('submission_bigram_add_0.5_smoothing_18.csv', generate_submission_bigram())
writefile('submission_unigram_22.csv', generate_submission_unigram())


# In[ ]:




