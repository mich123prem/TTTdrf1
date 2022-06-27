# TTT app backend
## A backend to support the TTT mobile app
## Models

* Zone 
  - Represents a zone in a library.
    Zones in a library have a preset order enforced by the app
* Activity
  - Represents one of a number of standard activities 
    patrons are engaged in within a zone
* Counting
  - Representing a round of counting of patrons engaged in 
    activities through all the zones of a library
* Project
 - A number of countings within a time span 
   for which a trafic rythm is of interest
   
## Views
* UserViewSet
* GroupViewSet
* CountingViewSet