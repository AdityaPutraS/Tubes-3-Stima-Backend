import json

def simpan(data,nama):
    json.dump(data,open(nama+'.json','w'))
def buka(nama):
    data = json.load(open(nama+'.json','r'))
    return data

stopWord = buka('app/static/stopwords-id')
sinonim = buka('app/static/sinonim')
soal = buka('app/static/soal')
jawaban = buka('app/static/jawaban')


#Menghitung border function dari string s
def computeFail(s):
    fail = [0 for i in range(len(s))]
    fail[0] = 0
    m = len(s)
    i, j = 1, 0
    while(i < m):
        if(s[j] == s[i]):
            fail[i] = j+1
            i += 1
            j += 1
        elif (j > 0):
            j = fail[j-1]
        else:
            fail[i] = 0
            i += 1
    return fail

#Mencocokan pattern di text (apakah pattern ada di text)
#Merupakkan exact match
#Algoritma sesuai slide matkul Stima 2019 dengan modifikasi
#agar bisa mengembalikan panjang kata terpanjang yang mirip
#O(m+n)
#Return : [index, maxLen kata yang mirip]
def kmpITB(text, pattern):
    #Hitung border function
    n = len(text)
    m = len(pattern)
    fail = computeFail(pattern)
    i, j = 0, 0
    maxLen = 0
    while(i < n):
        if(pattern[j] == text[i]):
            if(j == m-1):
                return [i-m+1, j+1] #Ketemu
            i += 1
            j += 1
        else:
            if(maxLen < j):
                maxLen = j
            if (j > 0):
                j = fail[j-1]
            else:
                i += 1
    return [-1, maxLen] #Tidak ketemu

#Menghitung last occurence untuk boyer-moore dari string s
def computeLast(s):
    last = [-1 for i in range(128)]
    for i in range(len(s)):
        last[ord(s[i])] = i
    return last

#Mencocokan pattern di text
#Merupakan exact match
#Algoritma sesuai slide matkul Stima 2019 dengan modifikasi
#agar bisa mengembalikan panjang kata terpanjang yang mirip
#O(nm + A), A = banyak alphabet
#Return : [index, maxLen kata yang mirip]
def bmITB(text, pattern):
    last = computeLast(pattern)
    n, m = len(text), len(pattern)
    i = m-1
    if(i > n-1):
        return bmITB(pattern, text)
    j = m-1
    maxLen = 0
    go = True
    temp = 0
    while(go):
        if(pattern[j] == text[i]):
            temp += 1
            if(j == 0):
                return [i, m]
            else:
                i -= 1
                j -= 1
        else:
            if(maxLen < temp):
                maxLen = temp
            temp = 0
            lo = last[ord(text[i])]
            i = i + m - min(j, lo+1)
            j = m-1
        if(i > n-1):
            go = False
    return [-1, maxLen]

def hapusStopWord(s):
    tempKata = s.split(' ')
    mark = [False for i in tempKata]
    for sw in stopWord:
        while(sw in tempKata):
            tempKata.remove(sw)
    return ' '.join(tempKata)

def hitungCocok(text, pattern):
    text = text.lower()
    pattern = pattern.lower()
    if(kmpITB(pattern, text)[0] > -1):
        return 1
    else:
        totalCocok = 0
        #Cocokkan per kata (Boleh sesuai spek)
        for tS in text.split(' '):
            tS = tS.strip()
            if(tS != ''):
                maxCocok = 0
                for p in pattern.split(' '):
                    for s in getSinonim(p):
                        #print("Match ", s, ", ", t)
                        hasKMP = kmpITB(s, tS)
                        hasBM = bmITB(s, tS)
                        has = hasKMP
                        if(hasKMP[1] > hasBM[1]):
                            has = hasKMP
                        if(maxCocok < has[1]):
                            maxCocok = has[1]
                        if(has[0] > -1):
                            break
                if(maxCocok != 0):
                    totalCocok += 1
                totalCocok += maxCocok
        return min(totalCocok/len(text), 1)
    
def getSinonim(kata):
    hasil = {kata}
    if(kata in sinonim):
        if('sinonim' in sinonim[kata]):
            hasil = hasil.union(set(sinonim[kata]['sinonim']))
    # for s in sinonim:
    #     if(kata in sinonim[s]['sinonim']):
    #         hasil = hasil.union(set([s]))
    for h in hasil:
        if(kmpITB(kata, h) == -1 and kmpITB(h, kata) == -1):
            hasil.union(getSinonim(h))
    return hasil

def getJawaban(pertanyaan):
    pertanyaan = pertanyaan.lower().strip()
    pertanyaan = hapusStopWord(pertanyaan)
    if(len(pertanyaan) == 0):
        return []
    mirip = []
    for idx, s in enumerate(soal):
        s = s.lower().strip()
        s = hapusStopWord(s)
        if(len(s) != 0):
            h = hitungCocok(s, pertanyaan)
            if(h >= 0.5):
                mirip.append({'jawaban':jawaban[idx], 'kemiripan' : h})
            if(h == 1):
                break
    mirip.sort(key = lambda x : x['kemiripan'], reverse=True)
    if(len(mirip) > 0):
        if(mirip[0]['kemiripan'] == 1):
            return mirip[:1]
    return mirip[:3]