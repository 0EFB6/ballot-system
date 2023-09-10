# Ballot ID (27 digits)
*** ** 000 *** ** **************  
Before 000 divider  
DUN:
-   Area, state  
After 000 divider  
Parliament:
-   Area, no., state  
Last 14 digits are hash digits created from ic number

## Custom number as identifier
### DUN
#### Area (no. from real world N**)
- Selangor
    - 031 Subang Jaya
    - 030 Kinrara
    - 036 Bandar Utama
    - 048 Sentosa
    - 025 Kajang

#### State
- 01	Johor
- 02	Kedah
- 03	Kelantan
- 04	Malacca
- 05	Negeri Sembilan
- 06	Pahang
- 07	Penang
- 08	Perak
- 09	Perlis
- 10	Selangor
- 11	Terengganu
- 12	Sabah
- 13	Sarawak
- 14	Federal Territory of Kuala Lumpur
- 15	Federal Territory of Labuan
- 16	Federal Territory of Putrajaya 

### Parliament
#### Area (no. from real world P**)
- Selangor
    - 108 Shah Alam
    - 106 Damansara
    - 107 Sungai Buloh
    - 110 Klang
    - 096 Kuala Selangor

#### State
- 01	Johor
- 02	Kedah
- 03	Kelantan
- 04	Malacca
- 05	Negeri Sembilan
- 06	Pahang
- 07	Penang
- 08	Perak
- 09	Perlis
- 10	Selangor
- 11	Terengganu
- 12	Sabah
- 13	Sarawak
- 14	Federal Territory of Kuala Lumpur
- 15	Federal Territory of Labuan
- 16	Federal Territory of Putrajaya 

## Test Cases
- Ballot ID: 0311000010810**************  
DUN: Subang Jaya, Selangor  
Parliament: Shah Alam, Selangor  

- Ballot ID: 0301000010610**************  
DUN: Kinrara, Selangor  
Parliament: Damansara, Selangor  

- Ballot ID: 0361000010710**************  
DUN: Bandar Utama, Selangor  
Parliament: Sungai Buloh, Selangor  

- Ballot ID: 0481000011010**************  
DUN: Sentosa, Selangor  
Parliament: Klang, Selangor  

- Ballot ID: 0251000010610**************  
DUN: Kajang, Selangor  
Parliament: Damansara, Selangor  