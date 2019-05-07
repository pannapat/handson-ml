#!/usr/bin/env python
# coding: utf-8

# In[1]:


def readfile(filename):
    file = open(filename, 'rt')
    original_text = file.read()
    file.close()
    
    return original_text


# In[2]:


def writefile(filename, content):
    file = open(filename, 'w')
    file.write(str(content))
    file.close()


# In[3]:


def preprocess_data(text, is_test=False):
    # remove punctuations !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    punctuation_list = ["!","\"","#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~","–","€","•","«","»","’","“","”","£"]
    if(is_test):
        punctuation_list.remove('{')
        punctuation_list.remove('}')
        punctuation_list.remove('|')
    for punctuation in punctuation_list:
        text = text.replace(punctuation, "")

    # remove numbers
    RE_NUMBERS = re.compile('[0-9]+')
    text = RE_NUMBERS.sub(r'', text)

    # remove emojis
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    text = RE_EMOJI.sub(r'', text) # still have ⛈ corcra❄ gorm❄

    # substitute multiple spaces with a single space
    text = re.sub(' +', ' ', text)
    
    # trim leading and trailing spaces
    text = text.strip()

    # normalize text to lower case
    text = text.lower()
    
    return text


# In[4]:


def count_unigram(text):
    count_dict = {}
    unigram_words = text.split()

    for word in unigram_words:
        if word in count_dict:
            count_dict[word] += 1
        else:
            count_dict[word] = 1
    return count_dict


# In[5]:


def count_bigram(text):
    count_dict = {}
    sentences = text.split("\n")

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


# In[6]:


def count_trigram(text):
    count_dict = {}
    sentences = text.split("\n")

    for sentence in sentences:
        
        # trim leading and trailing spaces
        sentence = sentence.strip()
        
        sentence = "^ " + sentence + " $"
        words = sentence.split()

        for i in range(len(words)-2):
            word_k_2 = words[i];
            word_k_1 = words[i+1]
            word_k = words[i+2]
            
            trigram = word_k_2 + " " + word_k_1 + " " + word_k

            if trigram in count_dict:
                count_dict[trigram] += 1
            else:
                count_dict[trigram] = 1

    return count_dict


# In[7]:


def calculate_trigram_prob(sentence):
    sentence = "^ " + sentence + " $" # this guarantee that index of {w|w'} won't be 0 or length - 1
    start_index = sentence.find("{")
    end_index = sentence.find("}")
    
    word_choice = sentence[(start_index+1):end_index] # "thoir|thóir"

    if word_choice:
        [word_choice_1, word_choice_2] = word_choice.split('|'); # word_choice_1 = "thoir" and word_choice_2 = "thóir"

        words = sentence.split();
        index = words.index("{" + word_choice + "}")
        
        w_k_minus_2 = words[index-2] if index >= 2 else ""
        w_k_minus_1 = words[index-1] if index >= 1 else ""
        w_k = word_choice_1
        w_k_prime = word_choice_2
        w_k_plus_1 = words[index+1] if index+1 < len(words) else ""
        w_k_plus_2 = words[index+2] if index+2 < len(words) else ""
        
        word_1_bigram_1 = (w_k_minus_2 + " " + w_k_minus_1).replace('  ',' ')
        word_1_bigram_2 = (w_k_minus_1 + " " + word_choice_1).replace('  ',' ')
        word_1_bigram_3 = (word_choice_1 + " " + w_k_plus_1).replace('  ',' ')
        
        word_2_bigram_1 = (w_k_minus_2 + " " + w_k_minus_1).replace('  ',' ')
        word_2_bigram_2 = (w_k_minus_1 + " " + word_choice_2).replace('  ',' ')
        word_2_bigram_3 = (word_choice_2 + " " + w_k_plus_1).replace('  ',' ')

        count_word_1_bigram_1 = bigram_count_dict[word_1_bigram_1] if word_1_bigram_1 in bigram_count_dict else 0
        count_word_1_bigram_2 = bigram_count_dict[word_1_bigram_2] if word_1_bigram_2 in bigram_count_dict else 0
        count_word_1_bigram_3 = bigram_count_dict[word_1_bigram_3] if word_1_bigram_3 in bigram_count_dict else 0
        
        count_word_2_bigram_1 = bigram_count_dict[word_2_bigram_1] if word_2_bigram_1 in bigram_count_dict else 0
        count_word_2_bigram_2 = bigram_count_dict[word_2_bigram_2] if word_2_bigram_2 in bigram_count_dict else 0
        count_word_2_bigram_3 = bigram_count_dict[word_2_bigram_3] if word_2_bigram_3 in bigram_count_dict else 0
        
        
        word_1_trigram_1 = (w_k_minus_2 + " " + w_k_minus_1 + " " + w_k).replace('  ',' ')
        word_1_trigram_2 = (w_k_minus_1 + " " + w_k + " " + w_k_plus_1).replace('  ',' ')
        word_1_trigram_3 = (w_k + " " + w_k_plus_1 + " " + w_k_plus_2).replace('  ',' ')
        
        word_2_trigram_1 = (w_k_minus_2 + " " + w_k_minus_1 + " " + w_k_prime).replace('  ',' ')
        word_2_trigram_2 = (w_k_minus_1 + " " + w_k_prime + " " + w_k_plus_1).replace('  ',' ')
        word_2_trigram_3 = (w_k_prime + " " + w_k_plus_1 + " " + w_k_plus_2).replace('  ',' ')
       
        
    
        # E.g. Tá Dora agus Bróigín ar {thoir|thóir} réalt-ainmhithe in éineacht le Pegaso.
        # p1 = P(thoir|Bróigín ar) * P(réaltainmhithr|ar thoir) * P(in|thoir réaltainmhithr)
        # c1 = count("Bróigín ar thoir") * count("ar thoir réaltainmhithe") * count(thoir réaltainmhithr in)

        # p2 = P(thòir|Bróigín ar) * P(réaltainmhithr|ar thòir) * P(in|thòir réaltainmhithr)
        # c2 = count("Bróigín ar thòir") * count("ar thòir réaltainmhithe") * count(thòir réaltainmhithr in)
        
        # P(thoir) = p1/(p1+p2)
        # P(thoir) = c1/(c1+c2)

        count_word_1_trigram_1 = trigram_count_dict[word_1_trigram_1] if word_1_trigram_1 in trigram_count_dict else 0
        count_word_1_trigram_2 = trigram_count_dict[word_1_trigram_2] if word_1_trigram_2 in trigram_count_dict else 0
        count_word_1_trigram_3 = trigram_count_dict[word_1_trigram_3] if word_1_trigram_3 in trigram_count_dict else 0

        count_word_2_trigram_1 = trigram_count_dict[word_2_trigram_1] if word_2_trigram_1 in trigram_count_dict else 0
        count_word_2_trigram_2 = trigram_count_dict[word_2_trigram_2] if word_2_trigram_2 in trigram_count_dict else 0
        count_word_2_trigram_3 = trigram_count_dict[word_2_trigram_3] if word_2_trigram_3 in trigram_count_dict else 0

        # calculate using conditional probabilities + add-k smoothing
        p_word_1_trigram_1 = (count_word_1_trigram_1 + K) / (count_word_1_bigram_1 + (K*V))
        p_word_1_trigram_2 = (count_word_1_trigram_2 + K) / (count_word_1_bigram_2 + (K*V))
        p_word_1_trigram_3 = (count_word_1_trigram_3 + K) / (count_word_1_bigram_3 + (K*V))

        p_word_2_trigram_1 = (count_word_2_trigram_1 + K) / (count_word_2_bigram_1 + (K*V))
        p_word_2_trigram_2 = (count_word_2_trigram_2 + K) / (count_word_2_bigram_2 + (K*V))
        p_word_2_trigram_3 = (count_word_2_trigram_3 + K) / (count_word_2_bigram_3 + (K*V))

        p1 = (p_word_1_trigram_1 * p_word_1_trigram_2) * p_word_1_trigram_3
        p2 = (p_word_2_trigram_1 * p_word_2_trigram_2) * p_word_2_trigram_3

        prob_word_choice_1 = p1 / (p1 + p2)
        
    return prob_word_choice_1


# In[8]:


def generate_trigram_submission():
    test_text = readfile('test.txt')
    test_text = preprocess_data(test_text, True)

    test_sentences = test_text.split("\n")
    answer_list = ["Id,Expected"]
    running_number = 1
    for test_sentence in test_sentences:
        if test_sentence:
            prob = calculate_trigram_prob(test_sentence)

            answer_list.append("{},{:.20f}".format(running_number, prob))
            running_number += 1
    answer = "\n".join(answer_list)
    return answer


# In[9]:


import re

text = readfile('train.txt')

text = preprocess_data(text)

unigram_count_dict = count_unigram(text)
bigram_count_dict = count_bigram(text)
trigram_count_dict = count_trigram(text)

K = 1
N = len(text.split())
V = len(unigram_count_dict)


# In[10]:


writefile('submission_trigram_add_1_smoothing_24.csv', generate_trigram_submission())


# In[ ]:




