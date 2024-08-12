pattern_list = {
                    'ИНН' : r"^\d{14}$", # ИНН
                    'authority' : r'^MKK[\d-]+$', # орган выдачи
                    'date_pointed' : r'^\d{2}\.\d{2}\.\d{4}$', # date_of_birth/date_of_expiry/date_of_issue # 31.12.2004
                    'date_unpointed' : r"^\d{8}$", # date_of_birth/date_of_expiry/date_of_issue  # 31122004
                    'gender' : r'[FM]', # Male or Female search # M or F
                    'passport_no' : r'\b(AN|ID)\d{7}\b', # ID1234567 и AN1234567
                    'otchestvo' : r'^[а-яА-Я]+(?:ВИЧ|ВНА)$', # Улукманапович
                    }

words_to_skip = [ # Слова на паспорте которые могут мешать так как имя/фамилия по своим свойствам похожи на слова
                    # front side
                    'patronymic', 'document', 'nationality', 
                    'the', 'kyrgyz', 'republic', 'the kyrgyz', 'kyrgyz republic', 'the kyrgyz republic', 
                    'thekyrgyzrepublic', 'thekyrgyz', 'kyrgyzrepublic',
                    'identity', 'card', 'identity card', 
                    'surname', 'name', 'sex', 'date of birth', 'dateofbirth', 
                    'signature', 'document', 'document#', 'document #', 
                    'date', 'dateof', 'date of', 'dateofexpiry', 'date of expiry', 
                    
                    # back side
                    'place', 'place of', 'place of birth', 'placeofbirth', 'authority',
                    'dateofissue', 'date of issue', 'personal', 'number', 'personal number', 'personal number',
                    ]