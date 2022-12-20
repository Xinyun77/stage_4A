{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fswiss\fcharset0 Helvetica-Bold;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc0\levelnfcn0\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{decimal\}.}{\leveltext\leveltemplateid1\'02\'00.;}{\levelnumbers\'01;}\fi-360\li720\lin720 }{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{hyphen\}}{\leveltext\leveltemplateid2\'01\uc0\u8259 ;}{\levelnumbers;}\fi-360\li1440\lin1440 }{\listname ;}\listid1}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}}
\paperw11900\paperh16840\margl1440\margr1440\vieww28240\viewh19580\viewkind0
\pard\tx220\tx720\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\li720\fi-720\sl480\slmult1\pardirnatural\partightenfactor0
\ls1\ilvl0
\f0\fs24 \cf0 {\listtext	1.	}
\fs28 Fichier \'e0 ex\'e9cuter : 
\f1\b run_.py. 
\f0\b0 Dans
\f1\b  
\f0\b0 cet example de teste je n\'92ai pris que 10 lignes de demande.
\f1\b \
\ls1\ilvl0
\f0\b0 {\listtext	2.	}Fichier d\'92entr\'e9es sont dans le INPUTS : fichier Json : new_network.json , 
\f1\b fichier de teste pour la demande
\f0\b0  :  test_uber1.csv. (contient que des PersonalVehicle)\
\pard\tx940\tx1440\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\li1440\fi-1440\sl480\slmult1\pardirnatural\partightenfactor0
\ls1\ilvl1\cf0 {\listtext	\uc0\u8259 	}Ligne 127 - 132 du run_.py g\'e9n\'e8re par le programme en rajoutant un pourcentage de UBER( ici 10%) dans test_uber1.csv sera : test_uber_.csv (contiendra 10% de UBER, se trouvera dans INPUTS).\
{\listtext	\uc0\u8259 	}Ligen 130 g\'e9n\'e8re le pourcentage de UBER.\
\pard\tx220\tx720\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\li720\fi-720\sl480\slmult1\pardirnatural\partightenfactor0
\ls1\ilvl0\cf0 {\listtext	3.	}Ajouter des d\'e9p\'f4ts\
\pard\tx940\tx1440\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\li1440\fi-1440\sl480\slmult1\pardirnatural\partightenfactor0
\ls1\ilvl1\cf0 {\listtext	\uc0\u8259 	}Ligne  119 -124 du run_.py. Il y a 4 exemples de d\'e9p\'f4ts,
\f1\b  quand j\'92ajoute plus que 1 d\'e9p\'f4ts, programme se plaindre au bout de certaines minutes avec erreur qui resemble \'e0:  self.depot[veh._current_node["vehicles"].remove(veh.id)    KeyError: '0'
\f0\b0 \
\pard\tx220\tx720\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\li720\fi-720\sl480\slmult1\pardirnatural\partightenfactor0
\ls1\ilvl0\cf0 {\listtext	4.	}Fichier de sorties se trouvera dans OUTPUTS\
\pard\tx940\tx1440\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\li1440\fi-1440\sl480\slmult1\pardirnatural\partightenfactor0
\ls1\ilvl1\cf0 {\listtext	\uc0\u8259 	}Dans le 
\f1\b veh.csv
\f0\b0  il n\'92y a que des PersonalVehicle, mais dans 
\f1\b path.csv
\f0\b0  il affiche que l\'92usager a bien pris le UBER.\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\sl480\slmult1\pardirnatural\partightenfactor0
\cf0 \
\
}