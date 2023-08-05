# -*- coding: UTF-8 -*-
#
"""
        history
        Names, first names, last names, foreign names.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading
4.0    - fixed a bug
3.0.2    -fixed names_japanese
3.0.3    - removed the german names from the names_last because it messes up certain things in pagebuster
evb
"""

__version__ = '4.0'



# ------------------------------------------------------
#    names
#
content = {
    'corporation_japanese': [
        '<#name_japanese#><#p_corporateform#>',
        '<#name_japanese#><#p_oldbiz_corporateform#>',
        '<#name_japanese#>-<#name_japanese#><#p_corporateform#>',
        '<#name_japanese#>-<#name_japanese#><#p_oldbiz_corporateform#>',
    ],
    'name': [
        '<#name_first_last#>',
        '<#names_px_scientific#> <#name_first_last#>',
        '<#names_px_scientific#> <#name_first_last#>',
    ],
    'name_first_last':[
        '<#names_first#> <#names_last#>',
        '<#names_first#> <#names_last#>',
        '<#names_first#> <#names_last#>',
        '<#names_first#> <#names_last#>',
        '<#names_first#> <#names_last#>',
        '<#names_first#> <#names_initial_weighted#><#names_last#>',
        '<#names_first#> <#names_initial_weighted#><#names_last#>',
        '<#names_first#> <#names_last#>-<#names_last#>',
        '<#names_first#> <#names_last#><#names_sx_weighted#>',
        '<#names_initial_weighted#><#names_first#> <#names_last#>',
    ],
    'name_english': [
        'Gibbs', 'McLaren', 'Miller', 'Kwon', 'Little', 'Reage', 'Keaney', 'Muller', 'Chou',
        'Lamberti', 'Feldman', 'Michaelson', 'Cho', 'Davis', 'Hoffman', 'Marsh', 'Suh', 
        #'Trump', Oh no, no longer getting that attention
        'Fernandez', 'Fitzpatrick', 'Lin', 'Vanderbeck', 'Lee', 'Larssen','Vanderkeere',
        'Nobelman','Frime','Mustcado','Fnimble','Handersjen','Devries','Naaktgeboren',
        'McNaville','Stormby','Stromby','McMillen','Wrombley','Zóchi','Ångstrøm',
        'Jansen','Janson','Janssen','Hendrikson','Pwolley','Marinski','Rwandi','Pagréwski',
        'Jønne','Vilår',
        'Kobayashi','Gallagher','Baker','Duvall','Vazquez','Murphy','Rutkowski','Vogel',
        'Meyerson','DiLorenzo','Schneider','Abbott','Marlowe','Kaye','Wynn','Davidoff',
        'Li','Smith','Lam','Martin','Brown','Roy','Tremblay','Lee','Gagnon','Wilson',
        'Clark','Johnson','White','Williams','Côté','Taylor','Campbell','Anderson',
        'Chan','Jones','Hernández','Visigoth','García','Martínez','González',
        'López','Rodríguez','Pérez','Sánchez','Ramírez','Flores','Ruiz',
        'Dominguez','Fernandez','Muñoz','Gomez','Álvarez','Suarez','Torres','Cruz',
        'Martin','Reyes','Ortiz','Santos','Smith','Jiménez',
        'smith', 'mitchell', 'jones', 'kelly', 'williams', 'cook', 'taylor', 'carter', 'brown', 'richardson',
        'davies', 'bailey', 'evans', 'collins', 'wilson', 'bell', 'thomas', 'shaw', 'johnson', 'murphy', 'roberts',
        'miller', 'robinson', 'cox', 'thompson', 'richards', 'wright', 'khan', 'walker', 'marshall', 'white', 'anderson',
        'edwards', 'simpson', 'hughes', 'ellis', 'green', 'adams', 'hall', 'singh', 'lewis', 'begum', 'harris', 'wilkinson',
        'clarke', 'foster', 'patel', 'chapman', 'jackson', 'powell', 'wood', 'webb', 'turner', 'rogers', 'martin',
        'gray', 'cooper', 'mason', 'hill', 'ali', 'ward', 'hunt', 'morris', 'hussain', 'moore', 'campbell', 'clark',
        'matthews', 'lee', 'owen', 'king', 'palmer', 'baker', 'holmes', 'harrison', 'mills', 'morgan', 'barnes',
        'allen', 'knight', 'james', 'lloyd', 'scott', 'butler', 'phillips', 'russell', 'watson', 'barker', 'davis',
        'fisher', 'parker', 'stevens', 'price', 'jenkins', 'bennett', 'murray', 'young', 'dixon', 'griffiths', 'harvey',
    ],
    'name_french': [
        'Jean',
        'Jeanne',
        'Philipe',
        'Pierre',
        'Jacques',
        'François',
        'Françoise',
    ],
    'name_female': [
        '<#names_first_female#> <#names_last#>',
        '<#names_first_female#> <#names_last#>',
        '<#names_first_female#> <#names_last#>',
        '<#names_first_female#> <#names_last#>',
        '<#names_first_female#> <#names_last#>',
        '<#names_first_female#> <#names_initial_weighted#><#names_last#>',
        '<#names_first_female#> <#names_initial_weighted#><#names_last#>',
        '<#names_first_female#> <#names_last#>-<#names_last#>',
        '<#names_first_female#> <#names_last#><#names_sx_weighted#>',
        '<#names_initial_weighted#><#names_first_male#> <#names_last#>',
    ],
    'name_german': [
        '<#name_german_descent#><#name_german_base#><#name_german_limb#>',
        '<#name_german_descent#><#name_german_base#><#name_german_heimat#>',
        '<#name_german_descent#><#name_german_base#>',
    ],
    'name_german_base': [
        '<#!^,name_german_px1#><#name_german_px2#><#name_german_px3#>',
        '<#!^,name_german_noun#><#name_german_px3#><#name_german_heimat#><#name_german_px3#>',
        '<#!^,name_german_noun#><#name_german_px3#>',
        '<#!^,name_german_noun#><#name_german_px3#>',
        '<#!^,name_german_noun#>',
    ],
    'name_german_descent': [
        'von ',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
    ],
    'name_german_heimat': [
        'dorf',
        'stadt',
        'burg',
        'bürg',
        'stuhl',
        'berg',
        'tal',
        'bach',
        'teich',
        'meer',
        'see',
        'hof',
        'heim',
        'land',
        'mark',
        'wald',
        'mann',
        'felt',
        'acker',
    ],
    'name_german_limb': [
        'hand',
        'handt',
        'kopf',
        'bein',
        'fuss',
        'fuß',
        'tropp',
        'tropf',
        'tröpf',
        'strauss',
        'mund',
        'münd',
    ],
    'name_german_male': [
        '<#name_german_title_male#><#name_german_base#>',
        '<#name_german_title_male#><#name_german_base#>',
        '<#name_german_title_male#><#name_german_base#>',
        '<#names_first_absurdlyGerman#>-<#names_first_absurdlyGerman#> <#name_german_base#>',
        '<#names_first_absurdlyGerman#> <#name_german_base#>',
        '<#names_first_absurdlyGerman#> <#name_german_base#>',
        '<#names_first_absurdlyGerman#> <#name_german_base#>-<#name_german_base#>',
        '<#name_german_title_male#><#name_german_base#>-<#name_german_base#>',
        '<#name_german_title_male#><#name_german_title_profession#><#name_german_base#>',
        '<#name_german_title_male#><#name_german_title_profession#><#name_german_base#>',
        '<#name_german_title_male#><#name_german_title_profession#><#name_german_base#>',
    ],
    'name_german_noun': [
        'fisch',
        'schrein',
        'bäck',
        'hack',
        'metz',
        'dort',
        'doof',
        'depp',
        'arl',
        'mann',
        'eber',
        'kuh',
        'schaf',
        'münch',
        'müll',
        'lietz',
        'ditz',
        'koch',
        'bach',
        'wagen',
        'bauer',
        'mauer',
        'heim',
        'tal',
        'brand',
        'aden',
        'mack',
        'mark',
        'schuss',
        'schrick',
        'schwein',
        'tier',
        'hoh',
        'hoch',
        'tief',
        'breier',
        'birn',
        'lager',
        'schuh',
        'stiefel',
        'enkel',
        'schu',
        'schlie',
    ],
    'name_german_px1': [
        'sch',
    ],
    'name_german_px2': [
        'iff',
        'off',
        'uff',
        'ripp',
        'orl',
        'ank',
        'reck',
        'isch',
        'esch',
        'osch',
        'wank',
        'ein',
        'an',
        'auf',
        'euf',
    ],
    'name_german_px3': [
        'en',
        'er',
        'en',
        'er',
        'en',
        'er',
        'en',
        'er',
        'en',
        'er',
        'ler',
        'inger',
        'elen',
        'erler',
        'erle',
        'erli',
        'mann',
        'auer',
    ],
    'name_german_title_female': [
        'Frau ',
        '',
        '',
        '',
    ],
    'name_german_title_male': [
        'Herr ',
        '',
        '',
        '',
    ],
    'name_german_title_profession': [
        'Doktor ',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
    ],
    'name_japanese': [
        '<#name_japanese_px#><#name_japanese_sx#>',
        '<#name_japanese_px#><#name_japanese_sx#><#name_japanese_sx#>',
        '<#name_japanese_px#><#name_japanese_sx#><#name_japanese_sx#>',
        '<#name_japanese_px#><#name_japanese_sx#><#name_japanese_sx#><#name_japanese_sx#>',
    ],
    'name_japanese_px': [
        'Sun',
        'San',
        'Son',
        'Su',
        'So',
        'Sa',
        'Yo',
        'Ya',
        'Ka',
        'Ko',
        'Mi',
        'Ma',
        'Ta',
        'To',
        'Ti',
    ],
    'name_japanese_sx': [
        'yi',
        'yo',
        'ya',
        'yu',
        'yan',
        'ki',
        'ka',
        'ko',
        'kan',
        'bi',
        'ban',
        'so',
        'san',
        'ta',
        'to',
        'ti',
        'shi',
        'sha',
        'sho',
        'tsu',
        'tsi',
        'hi',
        'ha',
        'ho',
        'mi',
        'ma',
        'mo',
    ],
    'name_male': [
        '<#names_first_male#> <#names_last#>',
        '<#names_first_male#> <#names_last#>',
        '<#names_first_male#> <#names_last#>',
        '<#names_first_male#> <#names_last#>',
        '<#names_first_male#> <#names_last#>',
        '<#names_first_male#> <#names_initial_weighted#><#names_last#>',
        '<#names_first_male#> <#names_initial_weighted#><#names_last#>',
        '<#names_first_male#> <#names_last#>-<#names_last#>',
        '<#names_first_male#> <#names_last#><#names_sx_weighted#>',
        '<#names_initial_weighted#><#names_first_male#> <#names_last#>',
    ],
    'name_somewhiteguy': [
        '<#names_first_patrician#> <#names_initial_weighted#><#names_last_patrician#>',
        '<#names_first_patrician#> <#names_initial_weighted#><#names_last_patrician#><#names_sx_weighted#>',
        '<#names_first_patrician#> <#names_last_patrician#> <#names_last_patrician#><#names_sx_weighted#>',
        '<#names_last_patrician#> <#names_initial_weighted#><#names_last_patrician#><#names_sx_weighted#>',
        '<#names_initial_weighted#><#names_last_patrician#> <#names_last_patrician#><#names_sx_weighted#>',
        '<#names_initial_weighted#><#names_first_patrician#> <#names_last_patrician#><#names_sx_weighted#>',
    ],
    'names_first': [
        '<#names_first_male#>',
        '<#names_first_female#>',
    ],
    'names_first_absurdlyBritish': [
        'Nigel',
        'Simon',
        'Cecil',
        'Jeremy',
        'Alastair',
        'Chesterton',
        'Oscar',
        'Augustus',
        'Isambard',
        'Morris',
        'Kingsley',
        'Neville',
    ],
    'names_first_absurdlyGerman': [
        'Jochen',
        'Achim',
        'Karl',
        'Adolf',
        'Heinz',
        'Klaus',
        'Hans',
        'Helmut',
        'Erich',
        'Gunther',
        'Brunhilda',
        'Edeltraut',
    ],
    'names_first_female': [
        'Jennifer',
        'Claudia',
        'Amy',
        'Erin',
        'Siobhan',
        'Susan',
        'Patricia',
        'Mary',
        'Elizabeth',
        'Nan',
        'Rosemary',
        'Meghan',
        'Leigh',
        'Bethany',
        'Justine',
        'Isabel',
        'Kirsten',
        'Ingeborg',
        'Petra',
        'Josie',
        'May',
        'Phoebe',
        'Zoe',
        'Karla',
        'Helen',
        'Theresa',
        'Tina',
        'Ellen',
        'Dara',
        'Penny',
        'Eloise',
        'Courtney',
        'Carmen',
        'Anna',
        'Daphne',
        'Laura',
        'Karen',
        'Bridget',
        'Sandra',
        'Emily',
        'Madeleine',
        'Tricia',
        'Kate',
        'Liz',
        'Jen',
        'Andrea',
        'Connie',
        'Lynn',
        'Thisbe',
    ],
    'names_first_male': [
        'Bill',
        'David',
        'Sasha',
        'Charles',
        'Michael',
        'Ted',
        'Donald',
        'Eugene',
        'Victor',
        'Tomasso',
        'Giovanni',
        'Kurt',
        'Marc',
        'Brad',
        'Philip',
        'Franco',
        'Paul',
        'Irwin',
        'Torben',
        'Erik',
        #'Petr', # Nah, too specific recognizable.
        'Maarten',
        'Jasper',
        'Michiel',
        'Isaac',
        'Patrick',
        'Alexander',
        'Martin',
        'Raoul',
        'Carl',
        'Clifford',
        'Nigel',
        'Ian',
        'Ross',
        'Walter',
        'Scott',
        'Marcus',
        'Craig',
        'Dieter',
        'George',
        'Warren',
        'Peter',
        'Rob',
        'Tyler',
        'Greg',
        'Arch',
        'Bob',
        'James',
        'Alan',
        'Jeremy',
        'Miles',
        'Graham',
        'Stuart',
    ],
    'names_first_patrician': [
        'Bill',
        'David',
        'Charles',
        'Michael',
        'Eugene',
        'Brad',
        'Philip',
        'Paul',
        'Patrick',
        'Alexander',
        'Martin',
        'Clifford',
        'Ross',
        'Walter',
        'Scott',
        'Craig',
        'George',
        'Warren',
        'Peter',
        'Robert',
        'Tyler',
        'Greg',
        'Bob',
        'James',
        'Alan',
        'Stewart',
        'Walter',
        'Ted',
        'Ronald',
        'Gerald',
        'Richard',
        'Dick',
        'Lyndon',
        'Dwight',
        'John',
        'Burton',
        'Eustus',
        'Hollings',
        'Morgan',
        'Earl',
        'Felix',
        'Anthony',
        'Daniel',
        'Everett',
        'Chad',
    ],
    'names_first_purewhitetrash': [
        'Cletus',
        'Dallas',
        'Donald',
        'Shasta',
        'Billy Rae',
        'Booker',
        'Jimbo',
        'Dee Dee',
        'Tiffany',
        'Kimberly',
        'Brittany',
    ],
    'names_initial_weighted': [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        'A. ',
        'B. ',
        'C. ',
        'D. ',
        'E. ',
        'F. ',
        'G. ',
        'H. ',
        'J. ',
        'L. ',
        'M. ',
        'N. ',
        'P. ',
        'R. ',
        'S. ',
        'T. ',
        'V. ',
        'W. ',
    ],
    'names_last': [
        '<#^,name_english#>',
        '<#^,name_english#>',
        '<#^,name_english#>',
        '<#^,name_english#>',
        '<#^,name_english#>',
        '<#^,name_english#>',
        '<#^,name_french#>',
        '<#^,name_japanese#>',
        '<#^,name_german#>',
    ],
    'names_last_absurdlyBritish': [
        'Balliol',
        'St. James',
        'St. John-Smythe',
        'Warburton',
        'Welby',
        'Northmore',
        'Pugh',
        'Sinclair',
    ],
    'names_last_patrician': [
        'Davenport',
        'Archer',
        'Bourne',
        'Whitney',
        'White',
        'Sterling',
        'Calder',
        'Stern',
        'Markham',
        'Tate',
        'Caldecott',
        'Davies',
        'Fitzsimmons',
        'Vanderpool',
        'Morgan',
        'Fisher',
        'Carnegie',
        'Ryan',
        'Jennings',
        'Dunbar',
        'Emerson',
        'Bryant',
        #'Trump', Oh no, no longer getting that attention
        'Stanley',
        'Sinclair',
        'Forbes',
        'Rowe',
        'Lawson',
        'Upton',
        'Palmer',
        'Adams',
        'Clark',
        'Knox',
        'Walters',
        'Carson',
        'Parham',
        'Mills',
        'Riley',
        'Bushnell',
        'Dupont',
        'Harrison',
        'Kennerley',
        'Johnson',
        'MacArthur',
        'Acheson',
        'Winslow',
        'Price',
        'Harper',
        'Sloane',
        'Polk',
        'Parker',
        'Franklin',
        'Blockland',
        'Johns',
        'Foster',
    ],
    'names_px_scientific': [
        'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 
        'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 'Prof. ', 
        'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ',
        'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ', 'Dr. ',
        # See https://degree.studentnews.eu/s/4113/77169-Degree-abbreviations.htm
        'DArts. ',          # Doctor of Art      
        'DBMS. ',           # Biomedical Science        
        'DBEnv. ',          # Built Environment    
        'DBA ', 'D.B.A. ',  # Doctor of Business Administration   
        'DCL. ',            # Doctor of Civil Law  
        'DCaM. ',           # Doctor of Coaching and Mentoring        
        'DCommEd. ',        # Doctor of Community Learning & Development   
        'DDes. ',           # Doctor of Design        
        'DEd. ', 'EdD. ',   # Doctor of Education 
        'EntD. ',           # Doctor of Enterprise        
        'JD. ',             # Doctor of Jurisprudence  
        'LLD. ',            # Doctor of Laws   
        'MusD. ', 'DMus. ', # Doctor of Music     
        'PhD. ', 'DPhil. ', # Doctor of Philosophy   
        'DPS. ',            # Doctor of Professional Studies  
        'DSc. ', 'ScD. ',   # Doctor of Science   
        'MBA. ', 'EMBA. ',  # Executive MBA   
        'FdA. ', 'FDA. ', 
        'FDArts. ',         # Foundation of Arts (Foundation degree)  
        'FdSc. ',           # Foundation of Sciences (Foundation degree)      
        'Mart',             # Master in Arts  MART    Mart
        'MArch', 
        'M.Arch. ',         # Master of Architecture  
        'MA. ', 'M.A. ',    # Master of Arts  
        'MComp. ',          # Master of Computing
        'MLA. ',            # Master of Liberal Arts   
        'MMath. ',          # Master of Mathematics     
        'MSc', 'MSci', 
        'M.S. ', 'MS. ', 
        'M.Sc. ', 'M.Sci. ', 
        'S.M. ', 'Sc.M. ', 
        'Sci.M. ',          # Master of Science 
    ],
    'names_sx': [
        ', Jr.',
        ', Jr.',
        ', Jr.',
        ' III',
        ' III',
        ' IV',
    ],
    'names_sx_weighted': [
        '',
        '',
        '',
        '',
        '',
        '<#names_sx#>',
    ],
        }



if __name__ == "__main__":
    def test():
        """
            >>> from pagebot.contributions.filibuster.blurb import blurb 
            >>> blurb.getBlurb('name')
        """
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

