import pandas as pd

def date_sorter():
    
    months_number = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6',
                     'Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}
    
    doc = []
    with open('dates.txt') as file:
        count =0 
        for line in file:
            #print('line ' + str(count)+': ' + line)
            doc.append(line)
            count = count +1

    df = pd.Series(doc)
    
    df1 = df.str.extract(r'((\d{1,2})[-/](\d{1,2})[-/](\d{2,4}))')
    df2 = df.str.extract(r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.]* (\d{1,2})(?:,? ) ?(\d{2,4}))')
    df3 = df.str.extract(r'((\d{1,2}) ?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]* (\d{2,4}))')
    df4 = df.str.extract(r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]* (\d{1,2})[thstndrd]{2}, (\d{2,4}))')
    df5 = df.str.extract(r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]* (\d{4}))')
    df7 = df.str.extract(r'((\d{1,2})[-/](\d{2,4}))')
    df6 = df.str.extractall(r'(\d{4})')
    
    
    #print(df7.dropna())
    
    ## replace the year in df1
    df1 = df1.dropna()
    df1[3] = df1[3].str.replace(r'(^\d{2}\b)', lambda x: '19'+x.groups()[0][:])
    #df1 = df1.set_index(df1.index.values)
    df1 = df1[[1,2,3]]
    
    ## replace the month in df2
    df2 = df2.dropna()
    df2[1] = df2[1].str.replace(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]*', lambda x: months_number[x.groups()[0][:]])
    df2 = df2[[1,2,3]]
    
    ## replace the month in df3 and swap day and month
    df3 = df3.dropna()
    cols = df3.columns.tolist()
    cols = cols[:1] + cols[2:3] + cols[1:2] + cols[3:]
    df3 = df3[cols]
    df3.columns = [0,1,2,3]
    df3[1] = df3[1].str.replace(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]*', lambda x: months_number[x.groups()[0][:]])
    df3 = df3[[1,2,3]]
    
    ## replace the month in df4 and insert the first day of the month
    df5 = df5.dropna()
    df5[3] = 1
    cols = df5.columns.tolist()
    cols = cols[:1] + cols[1:2] + cols[3:4] + cols[2:3]
    df5 = df5[cols]
    df5.columns = [0,1,2,3]
    df5[1] = df5[1].str.replace(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]*', lambda x: months_number[x.groups()[0][:]])
    df5 = df5[[1,2,3]]
    #print(df5)
    
    df7 = df7.dropna()
    df7[2] = df7[2].str.replace(r'(^\d{2}\b)', lambda x: '19'+x.groups()[0][:])
    df7[3] = 1
    cols = df7.columns.tolist()
    cols = cols[:1] + cols[1:2] + cols[3:4] + cols[2:3]
    df7 = df7[cols]
    df7.columns = [0,1,2,3]
    df7 = df7[[1,2,3]]
    #print(df7)
    
    ## insert the first of Jenuary of the year
    #df6 = df6.dropna()
    df6[1] = 1
    df6[2] = 1
    cols = df6.columns.tolist()
    cols = cols[1:3] + cols[:1]
    df6 = df6[cols]
    
    df_p1 = df1.append([df3,df2])
    #print(df_p1)
    
    intersection = pd.merge(df_p1,df5,how='outer',indicator=True, left_index=True, right_index=True)
    df5 = intersection[intersection['_merge'] == 'right_only']
    df5 = df5[['1_y', '2_y', '3_y']]
    df5.columns = [1,2,3]
    df_p2 = df_p1.append([df5])
    #print(df_p2)
    
    
    intersection = pd.merge(df_p2,df7,how='outer',indicator=True, left_index=True, right_index=True)
    df7 = intersection[intersection['_merge'] == 'right_only']
    df7 = df7[['1_y', '2_y', '3_y']]
    df7.columns = [1,2,3]
    df_p3 = df_p2.append([df7])
    #print(df_p3)
    
    
    df6 = df6[(df6[0].astype(int) < 2017)]
    df6 = df6.reset_index(level=['match'])
    intersection = pd.merge(df_p3, df6,how='outer',indicator=True, left_index=True, right_index=True)
    df6 = intersection[intersection['_merge'] == 'right_only']
    df6 = df6[['1_y', '2_y', 0]]
    df6.columns = [1,2,3]
    #print(df6)
    
    df_p4 = df_p3.append([df6])
    df_p4 = df_p4.astype(int)
    #print(df_p3[320:350])
    df_p4 = df_p4.sort_values(by=[3,1,2], ascending=[1,1,1])

    result = pd.Series(df_p4.index.values)
    #print(result)
    #print(type(result))
    #print(result.shape)
    
    return result

date_sorter()