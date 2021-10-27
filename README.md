# ENGG4000 - Automated Musician

<p align="center">
    <img src="https://media.giphy.com/media/NU8tcjnPaODTy/giphy.gif" width="480" height="282" />
</p>

## Overview
Our team’s goal is to model the naturally occurring algorithmic nature of music and music theory by constructing algorithms of varying sizes. We hope to build up from smaller algorithms such as generating a chord (combination of 3 notes) into building full musical phrases. Once our toolbox of musical algorithms is sufficient, we intend on introducing some deep learning/AI technology to analyze and learn common musical norms then utilize the algorithms we have designed in the creation of entirely automated musical compositions.

This project will use advanced algorithm building techniques to model the complexities of music in a consistent and usable way. It will also have the aforementioned interface with AI to give our algorithms life in the form of actual music.

## System Infrastructure Tools and Technologies

An appropriate selection of tools is incredibly important for the success of a software development team. The first tool we have decided to utilize is Trello which has a Kanban board, allowing us to keep track of our progression as well as outline user stories and individual tasks. We will be implementing a tailored Scrum methodology with many similar scrum events, for example; we will have daily standup meetings to share our individual progress. Python has been selected to be our main language as all team members have some level of proficiency with it. Additionally, the extensive libraries and information that come with choosing Python allows for more focus on project content and less on pure code-base. The tool selected for the team's main communication is Discord with a dedicated channel for daily stand ups to ensure we remain focused and on the right path.

## Project Set-up
* Install `Python`.
* Change your directory to `C:\...\eng4000\`.
* Run the command : `pip install -r requirements.txt` to install the required dependencies.

## Development Practices
* If a new package or library is added, make sure to add updates `requirements.txt` by running the command: `pip freeze > requirements.txt`.

## Group Members

###   Owen Lee
**Project Manager / Product Owner / Developer**
-   In charge of planning and coordinating weekly meetings.
-   Ensuring that the final product meets the specifications and requirements.
-   Frequent contact with team members to ensure shared vision.
-   Works alongside team members in developing the final product.
- _[[GitHub]](https://github.com/owenlee-dev)_ _[[LinkedIn]](https://www.linkedin.com/in/owen-lee-b3b3a2197/)_
    
###  Edward Chang
  **Integration Manager / Implementer / Head Developer**
- In charge of overlooking the integration of the whole project.
- Coordinates the team when merging different features together.
- Works alongside team members in developing the final product.
-  _[[GitHub]](https://github.com/edwardchang7)_  _[[LinkedIn]](https://www.linkedin.com/in/edward-chang-2134791a4/)_
    
### Thomas Campbell
**Quality Assurance Manager / Developer**
-   Ensuring standards set by the team are met.
-   Prepares a test plan with the team to ensure the final product is working as planned.   
-   Experienced Musician.    
-   Works alongside team members in developing the final product.
- 	 _[[GitHub]](https://github.com/tcampbe6UNB3035)_ _[[LinkedIn]](https://www.linkedin.com/in/thomas-campbell-a6a245184/)_   

### Elliot Chin
**Documentation Coordinator / Developer**
-   Takes meeting minutes during the weekly meetings.
-   Keeps track of all the deliverables and documents the progression of the team.
-   Builds documentation on completed portions of the project to increase usability and modifiability.
-   Works alongside team members in developing the final product.
- _[[GitHub]](https://github.com/Elliot-Chin)_  _[[LinkedIn]](https://www.linkedin.com/in/elliot-chin-90b4311a6/)_


## ABC Music Notation
Finding ABC Music: https://abcmusicnotation.weebly.com/tunes.html  
**Headers**
```
X:1          // the song number (file can have multiple songs
T:song name  // t stands for Tune
C:owen       // composer
M:4/4        // time signature
K:C          // key the song is in
```
Key can be any of the keys including modes
```
K:Cmix --> C mixolydian
K:F#   --> F sharp
```

**Writing music:**  
Can change pitch of note by changing case and adding ' and ,  
```
// C's from low to high:
C,, C, C c c' c''  
```
![image](https://user-images.githubusercontent.com/70532700/137584077-f9656902-9a08-407d-8bb0-7957c7608222.png)
```
// Major Scale
// z = rest
C D E F G A B c z  
```
![image](https://user-images.githubusercontent.com/70532700/137584024-cf7625d6-8061-406a-8248-a63438a582ae.png)

Note Lengths are denoted by numbers after notes - By default an 8th note  
```
// 16th note, 16th note(alternate notation), 8th note, 1/4 note, 1/2 note, whole note
C/2 C/ C C2 C4 C8 
```
![image](https://user-images.githubusercontent.com/70532700/137584244-7dc98732-8914-4afe-8a5f-3f87697a7b1c.png)

If you want to work with a default of 16th notes - can set the unit length note by using this header:
```
L: 1/16
```

Can attach notes in a beam - but the notes next to one another
```
CCCC/C/A/
```
![image](https://user-images.githubusercontent.com/70532700/137584324-54484e42-2ab9-4fd1-bf9d-54117792fb66.png)

Triplets
```
C C C2 (3ccc
```
![image](https://user-images.githubusercontent.com/70532700/137584391-47984635-1609-40d1-94c7-bbbf9649c30d.png)

Denoting flats and sharps
```
// Flat c, natural c, sharp c
_c =c ^c
```
![image](https://user-images.githubusercontent.com/70532700/137584490-fb2d3f51-a2d1-47db-a1ef-9e5339de2634.png)

Repeat and Bar Lines
```
// bar line, repeat and par line, double repeat, double bar line
CCCC | CCCC :| CCCC :: CCCC ||
```
![image](https://user-images.githubusercontent.com/70532700/137584635-71250ee0-0232-4599-9dd6-426e2afb72f0.png)

You can order your repeats and add bold bar lines like this
```
// [| = bold bar line, adding numbers after bar lines will signal what order
[| CCCC |1 EEEE :|2 GGGG |] CCCC ||
```
![image](https://user-images.githubusercontent.com/70532700/137584883-f2044704-32e6-49f7-9e44-6432f5c76733.png)

Chord Symbols
```
"D"D "DM7"D "Dm7"D
```
![image](https://user-images.githubusercontent.com/70532700/137585091-9f8eea60-119b-4c60-a01f-140fcc607689.png)

Chords
```
// chords denoted by square brackets
[CEG]4 [GBD]2 [ceg]4
```
![image](https://user-images.githubusercontent.com/70532700/137585341-8a2383da-4045-424c-aee6-89f3213dcc12.png)
```
// Can add as many notes as we want
[CC,c'E,EGg'g'']4 [GG,g'b'b,d']4
```
![image](https://user-images.githubusercontent.com/70532700/137585501-360886e7-60ff-4403-9011-a062ebeffcaa.png)

Ties, slurs and dotted notes
```
// Tying two notes together is done with a dash
// Slurring is done with brackets between notes
// Dotted notes are done with a period
C2-C2 .C (C E F G) C
```
![image](https://user-images.githubusercontent.com/70532700/137585690-36f68a07-e85b-4de5-9050-3db547d620fe.png)

Grace and roll notes
```
// grace notes denoted with curly braces
// roll notes denoted with tilda
|~C ~D ~E {E}F {F}G ~A ~B ~c|
```
![image](https://user-images.githubusercontent.com/70532700/137585761-a2a22dda-e003-42d6-8451-81735c1e01cd.png)

**Twinkle Twinkle Little Star Example**  
```
CCGG|AAG2|FFEE|DDC2:|
|:GGFF|EED2|GGFF|EED2|
CCGG|AAG2|FFEE|DDC2:|
```
![image](https://user-images.githubusercontent.com/70532700/137585810-07530219-b6fb-4308-900a-07aa6133ea7b.png)

Full Syntax guide: https://abcwiki.org/abc:syntax


