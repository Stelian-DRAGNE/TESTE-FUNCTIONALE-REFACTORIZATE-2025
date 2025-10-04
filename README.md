# TESTE FUNCTIONALE REFACTORIZATE 2025
TESTE FUNCTIONALE REFACTORIZATE 2025

Acest repozitoriu are drept scop prezentarea testelor care se afla in repo-ul : https://github.com/Stelian-DRAGNE/STELIAN_DRAGNE-PROIECT_SEPTEMBRIE_2024, insa refactorizate.

Testele "originale" din repozitoriul specificat mai sus au fost facute cu ocazia finalizarii unui curs cu specific de testare software si QA, iar la momemntul respectiv adica in 2024, au fost "construite" pe baza informatiilor dobandite in acel curs.

Acum insa a venit momentul ca aceste teste sa fie refactorizate, pentru a arata cat la "profi". In acest sens am creat acest repozitoriu, in care voi incerca ca acele teste sa fie cat mai "profi" refactorizate.

Proiectul are in compunere 15 teste automate.

Testele vor fi aplicate sectiunilor afisate in cadrul site-ului ales pentru testare.

Aceste teste sunt:
1.	Test verificare status pagină principală - Acest test va verifica dacă pagina principală a site-ului ales pentru testare este activă și nu returnează un cod de eroare, cel pregonizat fiind 200.
2.	Test acceptare cookie-uri pagină principală - Acest test acceptă politica de Cookie a site-ului ales pentru testare.
3.	Test scroll pe verticală pagină principală - Acest test va face scroll pe verticală a paginii principale a site-ului ales pentru testare.
4.	Test accesare secțiunea 'DESPRE NOI' - Acest test va accesa secțiunea `DESPRE NOI’, prezentă in cadrul site-ului ales pentru testare și completarea formularului online disponibil, urmata de simularea trimiterii formularului completat.
5.	Test "Intra pe cont" pe site – Acest test va simula crearea unui cont utilizator/client fara a se transmite solicitarea. Se va continua cu logarea în cont de utilizator/client creat în prealabil, verificare a uneia dintre secțiunile disponibile, și apoi 'Logout'.
6.	Test funcționare caseta 'Cauta in site ...' din pagina principală - Acest test va verifica funcționalitatea casetei 'Cauta in site ...' din pagina principală a site-ului ales pentru testare.
7.	Test cautare produs 1 in caseta 'Cauta in site ...' din pagina principală și simulare finalizare comandă - Acest test va efectua cautarea unui produs în cadrul site-ului ales pentru testare, se va accesa produsul respectiv, se adaugă în coș și se finalizează comanda.
8.	Test cautare produs 2 in caseta 'Cauta in site ...' și test adaugare produs 2 in cos, urmate de simulare finalizare comandă - Acest test va efectua cautarea unui produs în cadrul site-ului ales pentru testare, se va accesa produsul respectiv, se adaugă în coș. În continuare se va efectua cautarea unui alt produs în cadrul site-ului ales pentru testare, se va accesa produsul respectiv, se adaugă în coș și se simuleaza finalizarea comenzii pentru cele doua produse alese.
9.	Test sortare 'Biciclete Mountainbike' din secțiunea 'TOATE PRODUSELE' - Acest test va efectua sortarea produselor 'Biciclete Mountainbike' din secțiunea "TOATE PRODUSELE", în urma aplicării filtrelor dorite, disponibile pe pagina 'Biciclete Mountainbike'.
10.	Test accesare secțiunea 'BLOG' - Acest test va efectua accesarea secțiunii "BLOG", secțiune prezenta in cadrul site-ului ales pentru testare.
11.	Test accesare secțiunea "BRANDURI" - Acest test va prezenta lista brand-urilor comercializate de către site-ul ales pentru testare, în ordinea numărului de pagini disponibile in această secțiune a site-ului.
12.	Test accesare secțiunea "RETUR/GARANTIE" și completare Formular de Retur - Acest test va efectua accesarea și completarea formularului online cu privire la returnarea unui produs nou comandat online, produs care la primire, prezintă urme de uzura. Acest test va simula transmiterea formularului.
13.	Test accesare secțiunea "RETUR/GARANTIE" si completare Formular de Garantie - Acest test va efectua accesarea și completarea formularului online cu privire la aplicarea condițiilor de garanție comerciala asupra unui produs nou, puțin utilizat, care prezintă diverse neconcordanțe funcționale și de formă. Acest test va simula transmiterea formularului.
14.	Test accesare secțiunea "CONTACT" - Acest test va efectua accesarea secțiunii "CONTACT", secțiune prezentă în cadrul site-ului ales pentru testare și completarea formularului on-line disponibil. Acest test va simula transmiterea formularului.
15.	Test abonare la 'Newsletter' - Acest test va efectua abonarea la 'Newsletter', secțiune prezentă în cadrul site-ului ales pentru testare. Acest test va simula abonarea la 'Newsletter'.
    
In cadrul proiectului menționat mai sus, suplimentar, se prezintă și următoarele teste :

•	Test broken-links - rezultat preconizat 200.

•	Test Syncron.

•	Test Asyncron - Response 200.

•	Test Asyncron - Response 404
