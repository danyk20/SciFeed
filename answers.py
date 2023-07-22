from transformers import pipeline

qa_model = pipeline("question-answering")
question = "Is there enough cybersecurity experts?"
context = """
Masaryk University Faculty of Informatics
 Automated Problem Generation for Cybersecurity Games
Bachelor’s Thesis
Daniel Košč
Brno, Spring 2021

Masaryk University Faculty of Informatics
 Automated Problem Generation for Cybersecurity Games
Bachelor’s Thesis
Daniel Košč
Brno, Spring 2021

This is where a copy of the official signed thesis assignment and a copy of the Statement of an Author is located in the printed version of the document.

Declaration
Hereby I declare that this paper is my original authorial work, which I have worked out on my own. All sources, references, and literature used or excerpted during elaboration of this work are properly cited and listed in complete reference to the due source.
Advisor: RNDr. Jan Vykopal, Ph.D.
Daniel Košč
i

Acknowledgements
I sincerely thank my supervisor, RNDr. Jan Vykopal, Ph.D. for his em- pathy, valuable advice, and guidance during this remarkable journey. He always found time to answer and provide constructive feedback on my actual progress. Furthermore, his high demands and precision always pushed me to enhance my work what I am very grateful for. His friendly, supportive, and responsible approach have made the entire process a very pleasant experience, even though it was really challenging.
I would not finish this thesis without the neverending support and help of friends who always offered me a helping hand with my difficulties. Therefore I feel profound gratitude also to them.
iii

Abstract
Cybersecurity games are a successful tool for training current experts or educating new ones to satisfy fast-growing demand in this area. Therefore we created a mechanism based on the games, to test cyber- security skills more effectively and eliminate cheating. The student is provided with a personalized sandbox that represents a game envi- ronment with generated random values and flags for each individual. The sandbox is build at student’s host by Vagrant, and generated flags are uploaded to the game portal. Thanks to that, our solution offers the possibility to check if a student found the correct personalized flag. Students can find the flag after successfully solving the challenge and submitting that flag to the game portal, which was enhanced by a new plugin. If they submit someone else’s or the wrong flag, it will be logged for further analysis, and their flag will not be accepted. Finally, our prototype was integrated into homework within the introductory security course enrolled by more than 200 students.
iv

Keywords
cybersecurity games, KYPO, Capture the Flag, Python, Ansible, Va- grant, CTFd plugin, Automated Problem Generation, education, sand- box, assessment
v

Contents
1 Introduction 1
2 Background 3
2.1 Seriousgames ........................ 3 2.2 CapturetheFlag....................... 4 2.3 Cybersecuritycompetitions ................ 6 2.4 Assessmentandplagiarism ................ 7 2.5 Sandbox ........................... 10
3 Capture the flag platform 13
3.1 WorkflowwithinCTFd................... 14 3.2 Benefits............................ 17 3.3 Pluginarchitecture ..................... 19 3.4 Coreimplementation.................... 21
4 Automated problem generation 23
4.1 Users’perspective...................... 24 4.2 Generatorapplication.................... 26 4.3 Configurationfile ...................... 29 4.4 Generatorlibrary ...................... 32 4.5 CTFdPlugin......................... 35
5 Testing 39
5.1 Testingduringdevelopment................ 39 5.2 Testingwithinasecuritycourse.............. 42
6 Conclusion 47
6.1 Futurework ......................... 48
A Archive Content 49 Bibliography 51
vii

List of Tables
4.1 Table of supported attributes for each variable type 31
ix

List of Figures
3.1 3.2 3.3 3.4
3.5 3.6
3.7
3.8
4.1 4.2
4.3 4.4
CTFd welcome screen. 14
Creating new challenge form. 15
Creating new challenge pop-up window. 16
Three different challenges (one already solved) types in two
categories. 17
CTFd statistic. 17
Incorrect flag submitted in Dynamic challenge with three hints
in uniform challenge design. 18
Correct flag submitted in Static challenge with an attached
downloadable file in uniform challenge design. 19
CTFd directory tree of mentioned important directories. 20
Use Case Diagram of APG for cybersecurity assignments. 24
The error message displayed after a flag that belongs to the another player is submitted. 25
Sequence Diagram of the APG application. 27
Entity Relationship Diagram (ERD) of Individual flag. 37
xi

1 Introduction
Recent studies show that lack of professionals is causing a massive financial impact on global companies because they are often victims of a hacker attack [1]. Almost half of the employees thought that their company would hire more cybersecurity professionals within the next year [2]. To solve this situation, we should educate more experts in IT and security management.
Overcoming this deficit by education is taking a while. Therefore, new methods which are more effective are being developed. One of them is learning new skills by playing, but not every game brings the same benefits because there is a wide scale of different types: escape room, point & click, test/exam, interactive roleplay, puzzle cards & board game, serious game and others. We are going to focus more on the serious game and compare them to the others. This game usually uses storytelling with a simulation of any possible situation to prepare players for real life. It is played in a virtual environment combining entertainment and learning into one activity where players are involved in a real situation and use real instruments. Without this kind of experience, people might not react appropriately in a sudden situation because they learned theory, but applying it to a working example might miss.
Cybersecurity games originally came from security contest where they are still used to find new talents and experts. It is a subcategory of serious games where players are usually provided with a working environment that consists of several virtual machines. During the time, games became one of the elements in today educational content. Reached score in these games might be taken into account in the final grade, leading students to find ways to get a better grades with less effort. So, sometimes results may be distorted by cheating players who stole data from the original author. Research at National University of Singapore in 2018 and during the CTF competition called PicoCTF confirm that around 15% of players break the rules by submitting a shared flag [3, 4]. We will show how to avoid this situation and solve some other small issues which can occur during playing.
The main goal of this work is to generate different problems (tasks) automatically but within the same difficulty level and make them
1

1. Introduction
available to play either locally or on KYPO Cyber Range Platform [5, 6]. We have extended already existing games that are currently played in the local sandbox by generating individual tasks feature. To make it possible, it requires minor design changes in the sandbox. Moreover, we enhanced the submission portal with a custom plugin to be able to check personalized answers. This thesis can increase the efficiency of education provided by these games and help their future expansion. Additionally, current development enables game usage as one of the educational materials in university courses or even exams.
This thesis is divided into 6 chapters. Chapter 2 reviews the current state and concepts in this field to understand the problem in a bigger picture. Chapter 3 focuses on a specific platform that played a key role in our approach to solve the problem. Chapter 4 presents in-depth our implementation of the applied part consisting of three key elements. Chapter 5 is dedicated to testing and deployment into homework within the security course. Chapter 6 summarizes the work and add a suggestion for future work in this area.
 2

2 Background
This chapter starts with Section 2.1 introducing serious games, which are essential to understand the whole concept. It is followed by the Section 2.2 describing Capture The Flag games, the most common format of cybersecurity games and Section 2.3 is dedicated to current cybersecurity competitions where Capture The Flag games are applied. Then a comparison between Formative and Summative assessment, including reported research in this area, can be found in Section 2.4. Finally, Section 2.5 focus on Sandbox, where it is defined structure and use cases in local or cloud environment.
2.1 Serious games
Serious games are games category whose is aiming learning or prac- tising a skill in the first place, but fun and entertainment are essential elements. These games are a subcategory of serious storytelling [7] and share some features with simulations, however enriched with added pedagogical value. Nevertheless, serious games are attractive from a business point of view because it offers cheap alternative how to fast educate the mass of people at the same time.
Serious games industry
The application of these games can be found in a variety of different areas. This segment is increasing, especially in fields like education, defence, aeronautics, science or health. Possible use case varies from training first aid crews in emergencies to leading a management team, teaching arithmetic or practising a foreign language. [8]. This growth is accompanied by massive investments and research. Moreover, next growth is expected in upcoming years.
Advantages
Expansion of IT into different sectors raised demand for well experi- enced and qualified professionals in cybersecurity. The safest way to gain new experience is to use software that can emulate real systems in
3

2. Background
diverse situations. This approach prevents from causing any potential damage to hardware or data. What is more, it is easily adjustable and repeatable to train the same problem in various ways. An additional benefit of simulation is an option to experience threat from both per- spectives: as an attacker or as a defender. This practice is one of the most important for future professionals because it can provide them with an overview. Only the people who know weak places and how to abuse them can efficiently protect a computer system. They need to keep updated about current vulnerabilities, prepare themselves to face new attacks successfully and apply state of the art theory into a defense strategy. One of the answers to these needs is the cybersecurity game.
Positive aspects of these games are clearly visible from the first look. In contrast to other learning material, these ones are easily replicable and interactive. Learners attention is cached for a much longer time period, and they can build positive addiction to the game. One of the main advantages is allowing trainees to experience circumstances that are really hard or impossible to create in real conditions because of safety, money, and time. For example, we can observe military squad leaders who are trained not in real war conflict but in serious games.[9]
It may sound surprising, but students who use a serious game to learn, achieve better results and are less likely to burn out by learning than students who learn using other sources. [10] This observation leads to implementing the serious game in the education process to improve. In that case, the teacher position is slightly changing from someone who teaches to someone who interacts and discusses with students. In the end, students learned how to solved different chal- lenges on their own with support from the teacher. Other research [11] shows that just filling already existing entertainment games (for in- stance Minecraft) with educational content make a difference. Players tested by the traditional method after the game reach better results even though they did not become aware of learning.
2.2 Capture the Flag
Capture the Flag (CTF) games are games in cybersecurity whose main objective is to get the answer, also called flag in CTF terminology. This
4
 
2. Background
flag is hidden in purpose, and players need to prove their knowledge and gained skills to capture it in a limited time. Duration can differ from few hours to few days [4]. The flag can be one word, number, IP or even the entire sentence. After submission of the flag, the player gets an instant response if the submitted flag was accepted. There are some CTF games the provide hints, but using these hints can be penalized. Other penalties may apply to users that are trying to guess the flag and enter too many attempts. CTF games can be designed to be a serious game or a series of questions that need to be answered correctly to continue on another question (also called challenge in CTF terminology) [12]. In this thesis, we focus on CTF games played in sandbox that is interacting with CTFd platform described in Chapter 3, but there are many others [13].
CTF cybersecurity games are becoming more and more popular in the last few years thanks to their outstanding combination of en- gaging story and educational value. These games are often built on an attractive story to catch players attention and make them feel like in a real-world situation. Significant added value is that players can practise theoretical concepts and become motivated to explore cyberse- curity more in-depth. Games also support creativity, problem-solving skills, analysing or evaluating methods [14]. All mentioned abilities are crucial for current or future security administrators.
Attack-Defense
Attack-Defense CTF type is much closer to the original sports game called “capture the flag“. Players are divided into two teams, and they have two main tasks: attack the opponent team but at the same time defeat their own PCs or server. The game starts with a bounded time to patch security holes in the own system. After that, team members start to discover vulnerabilities in opponents system a trying to exploit them. A team with a higher number of points win the game.
A special category is the attack-only that shares the main idea with the attack-defense. However, the defense team is missing, and the attacking teams are still completing offensive tasks in order to gain access to a computer or network. They usually need to exploit a vulnerable service that organizers previously created.
5
 
2. Background
Jeopardy
A Jeopardy-style CTF type is built on several challenges in a wide spectrum of different topics such as forensic analysis, cryptography, reverse engineering, mobile security, Internet of Things, secure pro- gramming. The task is often supplemented by a story that is taking players deeper into the game. Each task is evaluated based on dif- ficulty and complexity. Apart from this, Jeopardy-style CTF games raise popularity in online competitions [12]. Mainly because it is more comfortable for organization, and there is no need to connect teams on the same level of knowledge together or require an even number of participants[15]. The winner is the player or the team with the highest number of points.
2.3 Cybersecurity competitions
Everyone from complete beginners to an experienced cybersecurity researchers can play these games to get feedback or learn new skills. But only the best players can participate in the worldwide known com- petitions. Participants race against time to solve specific challenges, fight threats, or develop innovative cybersecurity tactics. Motivation for them could be prize money, job opportunity or public recognition. Cash prizes in this competitions go up to two million dollars for the winner of the DARPA [16] competition. These competitions are also called contests, generally take place at universities or software compa- nies all over the world and are mainly based on the CTF games (see Section 2.2). Participants of these events can be students, enthusiasts or professionals who want to compare themselves and learn new skills in their free time. This extra activity for the students different them from the average or distinguish themself and open them new opportunities in the future career.
Teams or individuals are aiming to collect points that are earned after submission of the correct flag. Their overall position or ranking is publicly accessed on the website [17], accumulating details about up- coming events and archiving past ones. Another website [18] focuses on a comprehensive list of major CTF competitions in chronological order containing a short description and awards of each competition.
6
 
2.4 Assessment and plagiarism
Assignments are an integral part of the education process where stu- dents need to demonstrate their knowledge, skills and overall under- standing of the topic. Teachers will get feedback on what educational goals and standards their students met and which they struggled with. The result of this assignment often influences final grade, work place- ment, curriculum, or merit scholarship. That can lead some dishonest students to break the rules on the way to a better outcome. However, there exist some solutions that can notice and avoid this practice.
Formative assessment
Formative assessment aims to evaluate and give feedback after each step within the teaching-learning process [19]. Teachers use a wide variety of methods [20] to manage in-process evaluations of student comprehension, learning needs, and educational progress during a course. Formative assessment reveals concepts that students have problems with, show abilities where students struggle. In general, purpose of formative assessment is to obtain data that will be used to adjust the learning process instruction for a student and improve their understanding. These data are continuously updated to figuring out what our students really know and where can be improvement done.
It is essential to give feedback to students before the final points or grade. This feedback could be constructive for students that know theoretical knowledge but are confused by the assignment. Confusion can be caused by misreading in time, stress, or overlooking some important information mentioned in the text. Without additional help, these students would lose or even fail despite the fact they have learned the appropriate topic.
A single data point of test or exam is not enough to raise the level of the learning process. We need to evaluate more data and more often during the process to respond to actual student needs. These needs may differ from student to students and may change during the learning process. Solving these needs leads to a better outcome at the end because students are more focused on learning goals, active learning and keeping on task [10]. However, this task may become
7
2. Background
 
2. Background
complicated, almost impossible in medium-sized or bigger classes if it is done manually [21].
Cybersecurity assignments or games are considered to be chal- lenging, and it leads some students to give it up. Motivation is one of the keys to complete a given task after failure. Formative assignment raises the motivation to improve work more than single feedback after test or exam [22]. An example of formative feedback is discussing with students that did not meet requirements and explaining unclarities or recommending detailed steps for improvement. [21]
Summative assessment
Summative assessment, sometimes also called summative feedback, is the exact opposite of formative assessment. This evaluation of students is based on some form of a test at the previously defined moment or period. The evaluation period is typically after each book chapter, after the last lesson of the course, at the end of the semester or school year. Teacher or tutors measure academic achievement, skill acquisition and work that was presented at that time. This method delivers information about the level of knowledge at a specific time in the form of grade or score.
The most common forms of summative assessment is written or oral tests, assignments or projects. Some of these are countrywide stan- dardised test, usually in math, reading, writing, and science operated by central authorities. However, it is important to keep in mind that all tests, assignments or task forms can be summative as well as formative. But, the way how they are used matters, and it decides which type of assignment it is [23]. Summative assessment loses interactivity and the possibility of changing the way of thinking of an individual. The practical use case can be making course placement decisions or college admissions processes, among other potential applications. The focus is put on meeting requirements and understanding basic concepts instead of measuring progress.
Using modern technologies, we are able to aggregate data from a longer time period and from more students and different courses. By analysing this data, teachers can closer see students’ weak places and improve future learning plan. Furthermore, it is possible to let students take the same test or assignment several times and learn from
8
 
2. Background
their own mistakes. These attitudes lead to vanish some differences between formative and summative assessment. Sometimes, it can be really tricky to decide if it is summative or formative assessment. A good example is an interim exam that is repeated several times during the education process.
The benefits of summative assessment [24]:
• Allow students to apply what they have learned.
• Motivate students to study and pay closer attention, • Help identify possible teaching gaps.
• Contribute positively to learning outcomes.
Plagiarism
One of the main summative assessment problems is easy unauthorized solution sharing or stealing if teachers use the same assessment for everyone. Some students may try to find any shortcuts on how to get the best grade with minimal spent effort. As a result, we see many attempts to submitting someone else solution as their own. Few cases were reported. In the experiment conducted at the National University of Singapore in 2018, it was observed during the course that 14% of teams submitted at least one shared flag. [4] Further, research in cybersecurity competitions shows that 14% of teams used at least one flag from someone else. Surprisingly as much as 68% of them who copy the flag were able to come with their own correct flag in the end. The majority of shared flags were between teams from the same university and during competitions that last longer. [3]
Especially now, in 2020–2021, when schools are closed, and almost every student is learning from home using digital technologies due to pandemic restrictions, traditional methods of avoiding unwanted teamwork are becoming useless. It is effortless and straightforward for some students to submit someone else’s answer and almost impossible to verify who was the original author. This problem appears not only in cybersecurity games but all over different summative assessments.
One approach how to minimize flag leak is to create a unique as- sessment for each student playing the game. However, it is becoming
9
 
2. Background
almost impossible to do manually for a higher number of players. Therefore we need some kind of automatization here. The most ef- fective is automatic problem generation (further APG) because it can assure the task with the same difficulty but with a different flag for each team or individual. The other positive APG effect is the chance to uncover the cheating scheme, who submit whose solution. There is still a chance that two different teams or individuals will get the utterly same challenge, but it is very limited.
Leak flags founded on the web can be effectively mapped to the individual students that let them be shared since there is a low chance of having two students with the same generated flag. This knowledge allows us to penalize this student for breaking the rules. A student who submitted this leaked flag can be penalized as well.
The educational benefit of APG can be hidden at first glance, but different flags of the same challenge are a great method to train. Apart from graded assignment or homework, we can permit access to the tasks with APG at any time and allow unlimited new attempts. Stu- dents can prepare themselves by getting an opportunity to repeatedly practise until they reach a point when they are confident enough. It is possible to try different approaches how to solve the given prob- lem and choose the best. Given problem has always the same type and belongs to the same category, but new environment values are generated every time.
2.5 Sandbox
In general, a sandbox stands for isolated software environment, mostly using virtual machines or emulators. It can represent a virtual world consisting of one host or a group of hosts connect with one or many networks. Sandbox offers the possibility to test potentially dangerous application the same way as on a real system without any risk because it does not affect the external infrastructure. It can provide special tools for better analysing all actions, but user using sandbox or application running in the sandbox should not notice any difference compared to a real system. [25, 26]
10
 
KYPO CRP
KYPO Cyber Range Platform (KYPO CRP) [6] is a open-source virtual cloud environment developed and operated by Masaryk University since 2013. Since then, it provides cyber ranges for education, cyber defense exercises, and training. KYPO CRP relies on state-of-the-art technologies such as OpenStack, microservices, containers, and in- frastructures as code. Developers focus on repeatability, scalability, automation, cost-efficient to make training affordable. [27]
In this thesis, we represent sandbox, prepared for the attack-only type of CTF game, as a directory with files and subdirectories, includ- ing Topology Definition, Sandbox Provisioning and other required data to create a complete training virtual environment. Sandbox Pro- visioning uses Ansible to describe machine content, data stored in JSON and YAML make Topology Definition easy to read. Both Topol- ogy Definition and Sandbox Provisioning are in detail described in Section 2.5.
KYPO CRP allows users accessing the sandbox using a supported web-browser. Users thus do not need to install a software tool or build a virtual environment on local machine. There exist two different roles: student and teacher. These two roles differ in privileges. Obviously, the teacher role has extended functionalities and permissions compared to the student role. They can manage a game via an administration portlet and remotely connect to any game’s hosts using the VNC _console_. If the sesssion is held online and students are in a different physical location, it is a really effective way how to help students. [28]
Local KYPO CRP sandbox
Sandbox can be developed, tested and used on a local machine with any common operating system. The locally deployed sandbox is still compatible with the KYPO CRP but is easier and faster to develop or debug. Local sandbox uses the Vagrant [29] tool to build and manage virtual environments using VirtualBox and keep them automatically controlled. It contains parameters required to create each defined host and connect them to a network. Vagrant is widely supported on Linux, Windows and macOS and is compatible with many virtual software development environments.
11
2. Background
 
2. Background
Created virtual machines are configured by Ansible [30], an open- source tool for provisioning, configuration management, application deployment, intra-service orchestration, and many other IT needs. It is used to install software, change files and execute commands in order to prepare a virtual environment automatically. To do so, it performs predefined instructions from playbooks.
 12

3 Capture the flag platform
CTFd is an open-source framework for CTF games developed for CSAW CTF (Cyber Security Awareness Week) (Capture The Flag) in 2014 and was released as open-source software in 2015. This frame- work is used by many different companies, universities, or clubs to host their own Capture The Flags competitions. It offers a web-based inter- face focusing on ease of use and customizability for users and admins (see Figure 3.1). Customers can choose one of three plans starting at 50 U.S. dollars per month, providing a managed hosting service available at https://ctfd.io/. Nonprofit organizations, schools or universities are offered an educational discount for classes and workshops. There- fore also smaller organization without enough hardware or personal recourses can afford basic CTFd hosting for 10 U.S. dollars. [31, 32]
In the following sections, we describe the CTFd workflow from both player’s (student’s) perspective and administrator’s (teacher’s) perspective in Section 3.1. Later we show the main benefits of this platform in Section 3.2. Then we describe plugin architecture since its understanding is essential for further extensions in Section 3.8. Finally, in the end, we dive into backend and frontend implementation of CTFd to discover what can be a newly created plugin capable of and how to implement it on top of the core CTFd application in Section 3.4. The valuable lesson that we learned in this chapter was applied to de- velopment of our custom plugin for games with personalized sandbox described in Section 4.5.
13

3. Capture the flag platform
Figure 3.1: CTFd welcome screen.
  3.1 Workflow within CTFd
When we start CTFd for the first time, we need to setup the game. We have to set the game name and select a team mode where multiple players cooperate or a user mode where each player plays indepen- dently. On the following form, we have to create one administrator account that will manage the game. All other options like selecting a theme or banner are there to customize the environment. After suc- cessful set up the environment, we get into the main screen logged as administrator, as it is seen in Figure 3.1.
14

3. Capture the flag platform
Figure 3.2: Creating new challenge form.
For administrator is the most crucial “admin panel“ in the top bar where he can manage the whole game. Administrator will see the current statistic and new top bar with all possible settings categories. After clicking on the challenges button, the administrator will get into a challenge setting to create, edit, or delete the challenges. It is necessary to create a challenge for each task or question (problem) that requires a player’s submission.
The administrator can choose from two built-in challenge types as shown in Figure 3.2. The other option is to add a plugin that ex- tends standard challenge types. The built-in basic types differ in the number of points earned by the player for submitting the correct flag. More advanced type like multiple-choice is offered as one of the paid challenge plugins. Furthermore, it is possible to append additional files or images to each challenge. Then administrator should choose visibility as it is seen in Figure 3.3 and add at least one correct flag to each created challenge to make it solvable.
15
  
3. Capture the flag platform
Figure 3.3: Creating new challenge pop-up window.
The flag can be static or regular expressions (special strings repre- senting a pattern to be matched) in the standard CTFd challenge type, but plugins can extend it and add new flag types. The flag will be compared with a player’s submission immediately to determine if it is correct. If the submission is correct, as it is seen in Figure 3.7, they will earn some point, and the challenge will be displayed with green back- ground. The gain point immediately reflects into position within the real-time leaderboard. Displayed players are shown under nicknames instead of real names or emails to protects their privacy. On the other hand, if players submit a wrong flag, as it is seen in Figure 3.6, they will receive a message that the submitted flag is incorrect. No matter if the submission is correct, it will be logged, and the administrator can later analyze all submissions.
If standard CTFd does not cover all needs, there are several plugins for CTFd that implement additional features. Some of them are free written by community volunteers, and the others are paid, which cost around 20$. [31] Anybody interested can contribute free plugins by creating an entirely new custom plugin. Documentation about CTFd plugins and web tutorials can help developers to discover the CTFd plugin implementation possibilities. [33]
16
  
3. Capture the flag platform
 3.2 Benefits
 Figure 3.4: Three different challenges (one already solved) types in two categories.
Various challenges can be set various points values (see Figure 3.4) reflected difficulty or use principle the first gets the most points. This motivates players to solve task faster and choose the harder ones.
Figure 3.5: CTFd statistic.
Automatic, real-time graph visualization shown in Figure 3.5 makes stored data easy to understand by plotting a graph that represents a large amount of data. It helps to get a quick basic overview of the
17
 
3. Capture the flag platform
current game situation and compare it to the past. Furthermore, if the administrator set automatic CTF starting and ending, the whole game process does not require any manual operation.
Figure 3.6: Incorrect flag submitted in Dynamic challenge with three hints in uniform challenge design.
Figure 3.6 shows hints that are a great way to help the students that are struggling and cannot continue. However, each hint may cost some point to ensure that only players who need it will take it.
18
  
3. Capture the flag platform
Figure 3.7: Correct flag submitted in Static challenge with an attached downloadable file in uniform challenge design.
Chaining challenges can make the game a bit dramatic because players cannot know how many challenges are still waiting for them. Furthermore, it guides a player in the right direction if the games contains more consecutive challenges. Solving one challenge make it green can unlock one or more new challenges, see Figure 3.4.
3.3 Plugin architecture
CTFd was designed to be easily extended by specially written Python modules as plugins, but the plugins are still separated from the core.
19
  
3. Capture the flag platform
Therefore, the CTFd core application can be upgraded without losing any custom plugin behaviour. The CTFd developers claim they are trying to improve the CTFd core with no impact on plugins. However, they notify us: “...keep in mind that the plugin interface is still under development and could change.” [31]
Official documentation defines the plugin’s structure and position within the internal CTFd directory tree. Figure 3.8 shows the relevant part of a directory tree and describes each file in the CTFd-plugin directory. All others required files for the plugin should be included too.
config.json requirements.txt __i_niniit__.p.ypy README.md
Figure 3.8: CTFd directory tree of mentioned important directories.
The internal plugin’s logic is performed by __init__.py, which is loaded by the CTFd core. This Python plugin script must imple- ment a load function that will initialize the plugin. The load function
20
  CTFd
    api
plugins
models
    Challenges
CTFd- plugin
Dynamic Challenges
      
3. Capture the flag platform
will be called from CTFd core with Flask [34] application as an argu- ment. This approach allows the plugin to modify or override internal functionalities.
Flag
The CTFd core contains the BaseFlag object that implements compare method which gets two flag. One of them is an original flag saved in the database, and the second one is submitted by the player. Internal logic in that method determines if the submitted flag can be accepted and return the bool value. Developers who decide to create a new flag type should use this default well-documented BaseFlag object and override the original compare method. The last step is adding the newly created flag object type into a global dictionary FLAG_CLASSES with the flag type name as the key to ensure the call of correct compare method for each flag type.
Challenge
Defining new challenge types is similar to defining a new flag, but there is a parent object called BaseChallenge from which all other types inherit functions that can be overridden. Developers can choose if they want to override all functions or some of them. The majority of use cases are overriding static method solve because it is called after the players submitted their flag. Finally, a new challenge also needs to be added into the global directory with the type name as the key.
3.4 Core implementation
Comprehension of the CTFd core implementation is essential to de- velop a properly working plugin. Therefore we shortly describe the fundamental parts of the CTFd that will be useful in plugin develop- ment.
Backend
The CTFd core is written in Python and structured in smaller modules that handle individual aspects. The web application is built on the
21
 
3. Capture the flag platform
Flask [34] framework with Jinja [35] templates. Flask also provides RESTful API that enhances plugins possibilities by creating a commu- nication interface to internal functions or other external applications. Examples of implemented API calls are available in CTFd/api/v1 di- rectory.
Database
All data are stored in a database that is provided by the SQLAlchemy [36] Python SQL toolkit supported by Flask. Each table model is defined as a child from SQLAlchemy which allow access to SQL database and executing SQL queries from Python. A model object contains the __tablename__ attribute and local variables that represent columns in the table with constraints. More advanced tables might require to set in __mapper_args__ directory key polymorphic_on on proper columns.
Frontend
There exist standardised frontend assets that ensure unified design across the CTFd platform. Specialized plugin visuals are called Themes are written in Jinja2, HTML, CSS, and Javascript. On the other hand, all plugins that extend challenge or flag types need to use some frontend assets. Windows that pop up while manipulating with different chal- lenges or flags are usually defined for each type in the assets directory as a template file with a corresponding script. Based on the use case, we can choose from predefined used in built-in types or create a new one that better reflects our needs.
 22

4 Automated problem generation
This chapter describes in details the design and implementation of au- tomated problem generation for cybersecurity assignments. It consists of an application that generates a personalized sandbox and plugin as an extension to the CTFd platform that checks if the submitted flag matches a flag from a generated sandbox. The application used our library explicitly developed for generating pseudorandom values of the selected type.
The first Section 4.1 shows how users (teacher, student) view and interact with the system shown on Figure 4.1 representing use case diagram. The next Section 4.2 is focused on the user interface and intervention of communication (based on REST architecture) with the personalized plugin. The following Section 4.3 describes what should be done in order to prepare their game for flag generator. Then we get deeper into the generation process and explain details of the created library in the Section 4.4. Finally, the Section 4.5 describes our CTFd extension by the custom plugin that evaluates the correctness of the submitted individual flag from the personalized sandbox.
23

4. Automated problem generation
4.1 Users’ perspective
   Create standard flag
Create dynamic flag
Add individual flag
Add flag
Generate individual flag
        <<include>>
Create Sandbox
Submit flag
extension points
other person's flag <<include>>
Add log
Create challenge
<<include>>
Inspect logs
Load saved flags
<<include>>
        CTFd with Personal plugin Generator library
Generator application
    Student Teacher
Figure 4.1: Use Case Diagram of APG for cybersecurity assignments.
Players’ perspective
From players’ point of view, there are two cases during the game when they come across the flag generator. The first one is when they create
24

4. Automated problem generation
a personalized sandbox using a command-line application (the blue oval in Figure 4.1, see Section 4.2). The application calls the generator library (red oval in Figure 4.1, see Section 4.4) in the background to generate individual flags, then uploads the generated flags to the CTFd server, and finally builds the sandbox. Later, when a player tries to submit a flag via CTFd plugin (green ovals in Figure 4.1, see Section 4.5) compares the submitted flag to flags saved in the database. If any player submits someone else’s solution, the “Incorrect! “message will be raised but the attempt is saved. The player is not specifically notified about it.
Figure 4.2: The error message displayed after a flag that belongs to the another player is submitted.
Teacher’s perspective
In the following text, teacher denotes a person responsible for game, so it can be, for example, an administrator or instructor in a school
25
  
4. Automated problem generation
environment. From teacher’s point of view, there is only an instance of CTFd extended by our new Personal Challange plugin described in Section 4.5. This user role has the privilege to create any new chal- lenges or flags except individual flags. Personal challenges (our new challenge type for tasks in personalized sandbox) have to be created before users run the Create Sandbox (see Section 4.2) to save gener- ated flags to the database successfully. Beyond that, all other features from the original CTFd are still available.
Our CTFd plugin collects and saves data about each attempt of up- loading flags and submitting someones else flags. These log files can be evaluated during or after the game by teachers. They can see when a suspicious flag was submitted, from which IP address, what was the flag’s content and whose flag it was in the cheater.log file. The ex- tension point of the submit flag cell, which adds log into cheater.log, is triggered by submitting a flag that was originally uploaded for another player. The other newly added file uploaded.log carry all records about uploaded flags. It is updated after each run of the create_sanbox.py script with email, IP address, flag and time. The teacher can then determine if there is any suspicious activity based on combining information from both files. A combination of standard logs from CTFd core implementation and extend logs added by our plugin may help with troubleshooting or testing.
4.2 Generator application
The generator application’s main objective is to enable utilization of generator library and communication with CTFd (see Figure 4.3). The application generates different flags based on requirements set by a sandbox developer in a configuration file see Section 4.3. Admittedly the generator library described in Section 4.4 handles the values gen- erating process. This library can be imported to another Python script if there will be demand for different APG application (e.g. different provisioning technologies). Afterwards, Ansible provisioning starts building a sandbox virtual environment from Jinja templates contain- ing variables filled with recently generated values. These templates are used to configure all settings and prepare virtual machines for the game games. Finally, when the game is ready to play, the application
26
 
4. Automated problem generation
uploads all generated flag values with the provided player email to specified CTFd Server via POST request.
Considering advantages and disadvantages, we decided not to up- load a flag if the sandbox build fails. Student can capture a correct flag if and only if they played a sandbox that finished building successfully. In case of a perfectly built game but several unsuccessful responses from the server, the application prints the error message to inform the student about the problem. In this situation, students should check their internet connection, provided mail, other optional arguments and run the application again. To see all possible arguments and their description, students can use -h or --help argument. Students that are getting an error should run an application as the administrator again with an assured stable internet connection. If they are not able to fix it, they should report the issue to the teacher.
    :run_vagrant
:Generator
:Loader
    run_vagrant.py
Player
path, url, id = parse_input()
c = get_randomized_command()
run_generator()
list = get_variables(path) dict = generate(list)
create_temp_file(dict)
upload_flag(url,path,id)
request(url,dict)
print(success)
Figure 4.3: Sequence Diagram of the APG application.
27
       init_loader() <<create>>(dict)
      loop
[for i in range(10)]
 opt
[success]
<<return>> success
success = db.add(f)
f:IndividualFlag
  
4. Automated problem generation
Application installation
We have implemented this application as command line application create_sandbox.py providing all necessary features in simple way. Pipenv [37] ensures the installation of all necessary parts using Pipfile. As a result, players need not worry about package dependencies or other troubles that might occur during manual downloading and in- stallation. Detail instructions on how to install and use this application can be found in README.md. Furthermore, communication with CTFd server is also running in the background. Error messages like missing arguments, wrong input arguments or network problems can be the only visible output for a player.
Input arguments
The application, requires three option arguments.The first is path to the sandbox because the library needs to know what to generate. More detailed information about games can be found in Section 2.5. The sec- ond parameter is the URL address of the CTFd server with our newly developed plugin installed. The third parameter is player’s email. Our goal is to generate unique flag for every player, which means flag has to be coupled with the identification of the solver. By flag solver we denote a player for whom was an individual flag generated for proving successfully done a specific assignment. Otherwise, we would not be able to recognize cheating between players. There exist an optional argument --dry-run for testing purposes when we do not need to instantiate a sandbox. In that case, the application only prints out a text command for instantiating the sandbox using vagrant. Since there might be up to four arguments, we decided to implement also –help. Therefore we chose argparse [38] library allows us to parse input parameters and showing help dialogue and improves user experience.
Application implementation
First, the input parameters are validated, and if no problem occurs, then the variable.yml file loads as Variable instancies into the Python list. Then generate function imported from the generator library is used, which provides the creation of new values within all require- ments. Now when everything is ready, a file containing generated
28
 
4. Automated problem generation
values in the YAML format will be created in the sandbox directory. This temporary file functions as a dictionary for a template in the game. After the simulated environment is successfully built, this temporary file will be deleted due to the potential risk of the revelation of flags data during training by players.
Building game environment
The final step in this process is executing vagrant up command con- taining a Vagrant working directory path and Ansible arguments that carry path to file where generated values (see Listing 4.1) are saved. When command execution is accomplished, players can start playing the game on their local hosts and submit flags to the CTFd server via a web browser.
level_2_flag : "If␣you␣don’t␣value␣your␣time,␣ neither␣will␣others.␣Stop␣giving␣away␣your␣ time␣and␣talents --start␣charging␣for␣it."
level_3_flag : "Fn0ndraz"
level_5_flag : "There␣are␣two␣types␣of␣people␣who
␣will␣tell␣you␣that␣you␣cannot␣make␣a␣ difference␣in␣this␣world:␣those␣who␣are␣afraid ␣to␣try␣and␣those␣who␣are␣afraid␣you␣will␣ succeed."
Listing 4.1: Example of generated.yml 4.3 Configuration file
Current sandbox definitions need to be extended by a file containing all necessary and optional information for the generation of individual flags. Required information are the name and the type, which specifies what data types of flags are supposed to be generated. Besides that, the sandbox developer can optionally also specify a range of values or deny some specific values. These restrictions help sandbox developer to specify sensible flags for each challenge.
Existing sandbox that do not include configuration file can be mod- ified to work with a flag generator application. The modification lies in the substitution of hardcoded constant values used in Ansible
29
 
4. Automated problem generation
provisioning for variables. The original values of sandbox environment can be stored as default values in the file main.yml inside the default directory located in sandbox/provisioning/roles/<host_name>. If generator is used, they will be overwritten by newly generated val- ues, otherwise they will be used. This approach makes the sandbox also operating without a generator application and using the fixed default values instead of generated ones.
File structure
The file variable.yml is containing all attributes required for the generation process in YAML format [39] and must be created during sandbox development. It has to be located in the top-level game’s directory, and the structure is divided into YAML dictionaries where each dictionary represents one generated value and has to have the same name as the value in a game template. All variable attributes are indented, followed by a colon space value. Otherwise, it may not be parsed correctly.
Listing 4.2 shows four different variables types. The first variable called level_1_flag, which will be uploaded on CTFd Server, con- tains a random user name. The second variable attacker_ip shows a usage of range restriction for generating IP address in the chosen network range except for prohibited addresses. The third variable encrypted_file will not be uploaded on the CTFd server because it does not contain challenge_id attribute. However, it will be used in sandbox provisioning. The last variable (level_5_flag) is similar to the first one, but it shows that it does not matter on attribute position because it is arbitrary and resulted in the same object.
Variable attributes and types
Variable attributes are min, max, prohibited, challenge_id and type. Attribute challenge_id must contain the ID of the existing challenge on the CTFd server. Values that do not contain the challenge_id Vari- able attribute will be used in Ansible provisioning but will not be uploaded to the CTFd database. These value will affect the only sand- box environment on the local machine and make it more authentic to match with the final generated flag that will be uploaded. Attribute
30
 
4. Automated problem generation
min sets a minimum value that is possible to generate, and max value restricts the highest one that is still possible to generate. Excluding val- ues that can not appear in generated values can be done by prohibited attribute.
The only obligatory attribute is type, and it can be chosen from five different types: username, password, text, IP, port. Each variable type represents a variable with slightly different properties and may support different attributes. The username variable type will generate a random string value that makes sense as a nickname. On the other side password, which also generates a random string, does not guar- antee any meaningful consisting of randomly chosen characters. For generating sentences, it is a prepared text variable type that generates a short quotation composed of one or two meaningful sentences. The last variable type generating the string is IP which generated a valid IPv4 address. And finally, the only integer variable type is a port gen- erating a number that is chosen from a range of unused port numbers in default. Variable types support various attributes that restrict the generated value, as is shown in Table 4.1.
 Table 4.1: Table of supported attributes for each variable type
IP
X X X X X -
31
   username
 password
 text
 port
 type:
 X
 X
 X
 X
 min:
 -
 -
 -
 X
 max:
 -
 -
 -
 X
 prohibited:
 X
 X
 -
 X
 challenge_id:
 X
 X
 X
 X
 length:
 X
 X
 -
 -
       
4. Automated problem generation
Listing 4.2: Example of variables.yml
level_1_flag:
type: username
challenge_id: 2
attacker_ip: type: ip
min: 192.168.1.1 max: 192.168.1.254
prohibited:
- 192.168.1.100
- 192.168.1.11 encrypted_file:
type: password
level_5_flag: challenge_id: 5
type: text
4.4 Generator library
The generator library is a Python package called “generator“, and it is capable of generating a five different variables ports, IP addresses, names, passwords and sentences. It requires a specifically prepared configuration file stored in sandbox to work correctly. The generator uses the Python built-in library random for pseudorandom numbers from given seed and then converts them to a selected type of variable. As it is known, pseudorandom numbers are not entirely random. How- ever, they are enough for this purpose. The deterministic behaviour of the Mersenne Twister generator [40] does not cause any serious prob- lems because players are not expected to compute the next random value. Many different techniques are used to achieve this conversion from number to value of wished type. Mapping is one of those that is applied to generate a name from a list of names. The list of names is stored as a file in a package directory. A similar principle is used to
32
 
4. Automated problem generation
generate a password, but instead of a list, it is used the ASCII table to get each character of the password. Also, There are some mathematical operations that modify the Integer value into a valid IPv4 address.
Internal structure
The generator library consists of few files which are going to be intro- duced one by one shortly. Starting with setup.py, the compulsory file of each package. This file contains basic information about the pack- age like name, author, and also the version which has been already mentioned above. The next file is README.md which briefly documents the whole library. Then we continue on Pipfile, where are stored all dependencies. There is also one hidden file named .gitlab-ci.yml, which creates CI/CD pipeline after each commit which selected com- mands and settings. These pipelines are saving time during devel- opment by making testing and generating distribution archives au- tomatically. Directory with source code scrips and text files essential for the generation process. All .txt files contains just prepared string values from which the generator picks based on actual preferences of user settings. More important is the var_object.py file, which stored the structure of Variables objects used in the generation process. No less interesting is the var_parser.py, which parses the input file (will be described later) from a user called variables.yml into variables objects. The most important is var_generator.py which uses both previous and for each variable object generate specific value based on selected settings or range. Finally __init__.py, which is obligatory for every package.
This library also contains unit tests stored in the directory tests and provided by a built-in unittest package. These tests help to verify if new changes in the code did not imply some unwanted behaviour and can be run automatically within CI/CD pipeline. Based on pytest
–cov-report is coverage around 97%. Generation process
Variables generating is completely managed by the application that imports library functions generate and parser_var_file. At the be- ginning, function parser_var_file is called with the file object as
33
 
4. Automated problem generation
the only argument. It is load using YAML library into the Python dictionary structure. Each key represents one variable name, and the value represents variable constraints like type, prohibited values, min and max value. For each item in the dictionary, it will append one corresponding var_objects into the result list that will be returned in the end.
Later, when a list of var_object is prepared, generate function is called. Besides the list of var_object, it requires a seed that guar- antees the same generated values for the same player no matter how many times a generate function was called or what device was used. However, if there are two variables of the same type in the input list, values will be generated differently because the seed value is in- cremented in each iteration. Each iteration processes one item from the list by assigning appropriate value into the generated_value at- tribute of var_object. A value is chosen based on the type attribute in var_object. Therefore it was implemented as an individual get func- tion that can generate a random value within set restrictions for each supported type. Types username and text are generated by choosing a random element from the source file with saved predefined values. This approach was chosen to produce only meaningful values, and all other types are generated straight from a given random number and do not use any predefined values. In the end, every var_object in the input list is mapped into a dictionary where the name attribute be- comes the key, and the generated_value attribute becomes the value. This dictionary is returned to the app for the next processing.
This library generating algorithm relies completely on the random package, which is included in standard python. However, we are aware of the Faker package existence that can generate numerous various data types. Therefore we are considering its implementation in future to enhance data types provided for APG.
Versioning
Each code update of the generation library comes with the new version adjusted in the setup.py file. The format of the version is x.y.z. Minor updates increase z value, bigger updates increase y values, and huge updates increase x value. After pushing a newer version into the Git repository, it will be built and deployed automatically new package
34
 
4. Automated problem generation
that is almost immediately available to download and use. All previous versions remain still available for backwards compatibility. The latest version is downloaded as default when using “>=“ in Pipfile by Pipenv. We developed more than 20 beta version of the library package until we finally made our product release. The automatic builds and tests with coverage of around 97% made this process much faster.
4.5 CTFd Plugin
CTFd Personal Challenge Plugin is an extension of the popular CTFd platform that enables the full potential of generated flags. This plugin brings new features provided by a new type of challenge called Personal and a new type of flag called Individual. Moreover, the plugin is released under MIT licence in the electronic attachment of this the- sis, as well as the original CTFd platform. All these attributes make the plugin perfect for many occasions like competitions, exams and homework.
Typical use case
Dozens, sometimes hundreds of players, usually participate in compe- titions, which bring enormous data to work with. In these situations comes in handy tool that can check each answer, make statistics and reveal cheating. An ideal situation will be when players have their own flags corresponding to the given assignment. Those flags will be generated for each player separately and independently. Submitted flags can be immediately automatically checked. Result of that is visi- ble for the player, and in case of cheating, all possible information will be automatically saved into the log for further analysis. We address this need by our Personal Flag plugin.
Development
During plugin development, we keep in mind possible CTFd core up- dates that may occur later. We implement all functionalities separately out from the core, even those which are affecting core behaviour. This approach remains modularity of the CTFd platform with adding new features. We faced problems with override inner API calls, database
35
 
4. Automated problem generation
structure, class inheritance and others. These aspects are described in detail in the following sections.
Individual flags
The main reason why we need a new type of flag is a lack of infor- mation carried by current flag types. Neither Static nor Regex type can carry additional information about a player at whom this flag aimed. A new type of flag called IndividualFlag solved this problem for us. It inherits all essential attributes and methods from parent class BaseFlag and adds support of one particular ownership per flag plus overrides compare method. This method has to compute with the customized input argument enriched with the ID of the player who has submitted a flag. If a player submits a flag saved in the database for another player and his or her flag is different, the return value will be the user ID of the player who generated this flag. If the player summit flag saved into the database under his or her ID, zero would be returned no matter on other players record in the database. Otherwise, a negative value will be returned.
Personal challenge
Personal challenges are based on the general BaseChallenge class implemented in the CTFd core. The difference between the original class is in the attempt method that loads IndividualFlag instead of Flags class along with user ID that is added into submission variable. IndividualFlag class inherits all attributes from its parent class Flag plus contains additional information about the solver of each particular flag. Discovering the potential sharing or even stealing flags between players is available only with Individual flags used in Personal chal- lenge. This constraint is caused by CTFd design that does not pass player’s ID to compare method defined in BaseFlag class. Both Static and Dynamic challenges suffer from the same limitation. Otherwise, when other types of flags are used, challenge behaviour is the same as Standard challenge. The frontend structure is almost identical to the Static challenge with minor upgrades in create.html.
36
 
Database
4. Automated problem generation
  Users
 PK customer_id int(10) NOT NULL
  U oauth_id int(10) NULL
name varchar(128) NULL password varchar(128) NULL
U email varchar(128) NULL type varchar(80) NULL secret varchar(128) NULL website varchar(128) NULL affiliation varchar(128) NULL country varchar(32) NULL bracket varchar(32) NULL hidden bit NULL
banned bit NULL banned bit NULL verified bit NULL
FK team_id int(10) NULL created date NULL
 Challenges
 PK id int(10) NOT NULL
  name varchar(80) NULL description varchar(255) NULL max_attempts int(10) NULL value int(10) NULL
category varchar(80)NULL
type varchar(80)NULL
state varchar(80) NOT NULL requirements varchar(255) NULL
         Flags
 PK id int(10) NOT NULL
  data varchar(255) NULL content varchar(255) NULL type varchar(80) NULL
FK challange_id int(10) NULL
     IndividualFlag
 FK flag_id int(10) NOT NULL
  FK user_id int(10) NULL
   Figure 4.4: Entity Relationship Diagram (ERD) of Individual flag.
More significant changes have been made in a database that is built on the SQLAlchemy [41] library. We add one new table IndividualFlag connecting flags and users see Figure 4.4. This is implemented as the table that contains foreign keys flag ID values and user ID values. This approach leads to a database that still follows third normal form (3NF) [42] restrictions. On top of it, we resolve the problem with an inheritance of database models cased by core CTFd database design that was not planned to extend each table by inheritance. The solu-
37

4. Automated problem generation
tion rests in overriding of Flag class with set __mapper_args__ to an appropriate value and creating child IndividualFlag.
SQLAlchemy (introduced in Section 3.4) offers an opportunity to read data from a database and create instances of different classes containing that data. Dictionary __mapper_args__ is responsible for this process that has to be included in each of these classes. Key polymorphic_on stores the name of the column according to which will be chosen one of the classes. Key polymorphic_identity stores value in that column that has to be the same in order to choose this class. In our case, we set polymorphic_identity on individual, and polymorphic_on on type is inherited from the Flag class.
Populate
For easier testing or demo purposes, we prepared predefined settings of CTFd that can be loaded by running populate_personal.py. Ten Per- sonal challenges with an ascending number of points per challenge will be created. Also, one administrator and ten users will be created, starting with ID 1 for administrator and from 2 to 11 for players. Ad- ministrator’s credentials are both the same “admin“. This short script saved us a lot of time during development. What is more, it can also be used with changed values to simulate real load on a server before training and perform a stress test. Optionally it is possible to simulate generator application usage with optional argument --flags.
Communication interface test
We also implemented a simple test script to verify if our newly cre- ated API within our plugin works as it is expected. It tests valid post request as well as invalid and checks the responded error messages. Modification of the test can be done by using optional arguments which can set different URL and numbers of challenges and players in the database during the test. All information about optional argu- ments can be shown using -h (help) argument when calling python3 store_test.py. Keep in mind that this test, stored in the same direc- tory as populate_personal.py, must be performed with an empty database.
38
 
5 Testing
Every application or IT system should go through integration testing in one of the last project phases. Tests can be performed by manual or automatic unit tests or human testers, which will simulate different scenarios with the motives of finding errors in software. Each part needs to be tested individually and also altogether as one working unit. The same code may be executed differently on various OS. Therefore it is crucial to perform tests on a wide scale of different OS in the best case also on different versions of the same OS.
Despite a lot of effort put into testing, it can not be guaranteed 100% functionality in any circumstances. There will still exist an unpre- dictable situation that can cause unwanted behaviour. Especially when the project relies on software tools created by third parties which are still under development, it may happen that some versions installed on end machines will cause an error. However, testing still catches the majority of the defects that were not found in the early stages of the software development life cycle.
5.1 Testing during development Gitlab
Active team cooperation on the code requires the ability to share the current version of the code simply and quickly. Gitlab offers exactly that, plus it is integrated into many popular IDEs what makes work- flows even better. It basically covers all our needs: continuous test, share, backup and review. Therefore we decided to use Gitlab as our central code collaboration platform. All project files, including instruc- tions, could be found on the university Git repository during the whole development.
Using Git as a version control system (VCS) highly increases the time effectiveness of the development. Creating new branches and committing features individually with message assists to keep code development clean and under control. Really helpful was the rollback feature in situations when a new version broke something we were
39

5. Testing
able to return to the last fully bug-free version. GitLab makes all of this available for everyone with a valid token.
Each newly uploaded version of the code trigger pipeline, YAML file containing a list of jobs in different stages to be executed. Each stage has some importance, starting with Continues Integration (CI) stages where integration was verified by unit test, and completing with Continues Delivery (CD) stage where the package was build and deployed. Thanks to the CI/CD pipeline on GitLab, developers save a lot of time by automatically creating the new package. [43] This software engineering approach helps to keep the package still updated to the newest version and runs a basic test automatically, decreasing the probability of failure in a package. Moreover, reporting issues with set priority helps manage time, fix a bug or expand functionality more productively. The next great advantage is cooperation and discussion of multiple people on one project at the same time.
We decided to adopt an iterative development approach for this project, which turn out to be a great choice. Our prototypes during the development were tested on one sandbox, but for final testing, in the education environment, we needed to use another sandbox. For this reason, we need slightly change the set of all possible generated names. Thanks to our modular design and automated CI/CD, it was enough to swap the source names.txt file for a new better fitting one plus increase the version number, and an all-new package will be produced automatically.
Docker
Docker [44] is an open-source tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and deploy it as one package. Thanks to the container, the developer can rest assured that the appli- cation will run on any other machine regardless of any customized settings that the machine might have that could differ from the device used for writing and testing the code.
The benefit of using Docker compared to Virtual Machine is using fewer recourses because all containers together share services of a single OS kernel. The rerun of the container takes only a couple of
40
 
5. Testing
second instead couple of minutes in virtual machines. [45] It supports all common OS and all common platform, even the newest M1 chip from Apple. [46] Besides the paid version, there also exists a free version that is sufficient for our use case. Finally, CTFd includes a docker image Dockerfile in its publicly open git repository.
PyCharm
PyCharm IDE (Integrated Development Environment) is used for programming, mainly for the Python language, to enhance productiv- ity. It takes care of the routine and makes several other tasks such as graphical debugging, visualizing, code navigation and analyzing, inte- grating with version control systems and unit testing easier. PyCharm works with Windows, macOS and Linux, and it is released under the Apache License. Students can get an free educational licence for the Pycharm professional version what makes this IDE popular in the academia.
From all advantages that PyCharm offers us, we mostly appreciate debugger. Some errors that appeared during each development itera- tion was difficult to resolve or find their cause in the code. Therefore breakpoints help to inspect code during the execution and monitor each variable value at the exact point while code execution is sus- pended. Then it is possible to jump on the following line or following breakpoint. This approach was also used when it was necessary to understand how original CTFd (see Chapter 3) implementation works and communicate in order to develop the plugin.
The other benefits like refactoring, Pylint, PEP8 auto formatting were used several times to decrease development time and increase code readability and cleanness. Also, an option to execute code with a different Python interpreter was tested to ensure code execution on newer Python versions 3.7 or 3.9. Even though all tests passed on both more recent versions, it is recommended to use Python 3.6 because all imported libraries are officially supported in this version. Some built-in features like autofill or on-the-fly syntax check prevent making typos in variable or function names and automatically offer possible Context Actions that can solve the error in some cases. Support of Markdown language makes writing README.md files directly from IDE comfortable because it can render the final document in real-time.
41
 
5. Testing
Testing on macOS
The macOS was used as our primary OS for development and testing from the early beginning. During the first phases, the project was divided into three components: Application, Library and Plugin. This decision had a massive influence on testing in the end because the error could be propagated out of one component. Therefore the testing of a new feature or functionality requires testing only the affected component.
One iteration usually took one or two weeks and contained patches of founded issues and few improvements. The last step of each iteration was manual unit testing, where we primarily tested newly added fea- ture in various conditions and also overall functionality. Testing CTFd with installed Personal challenge was done using Docker containers (see Subsection 5.1) and described in Section 4.5. The application was executed in Python virtual environment managed by Pipenv described in Section 4.2. To resolve problems deeper in code, we used Pycharm debugger (see Subsection 5.1) while simulating the error situation.
Helper script populate_personal.py drastically increases the ef- fectiveness of the testing because of the manual setup that consists of four registration forms. Time spent by filling in each form cell is not neglectable for the tester that needs to repeat it dozens of times. Each new test was done in a fresh environment with valid data to ensure that old or corrupted data do not influence the results. During testing, we populate the database using this script by calling it from the Docker CTFd container.
5.2 Testing within a security course
To have better control over the found problems during the testing, we decided to start using the Gitlab issues feature for reporting tasks, en- hancements, and bugs in our projects. It is a great bug tracker because it allows to discuss the possible fix or improvement, plus there is also a possibility to specify the priority. Every new issue will automatically deliver notification to the responsible person that will decide how to deal with it.
Before teachers from course information security and cryptogra- phy (PV080) tested our solution, we had provided complex testing of
42
 
5. Testing
all the different scenarios that we could make up to remove most of the problems. However, we expected some problems could happen on a different OS that were tested a bit or not at all. Six teachers were involved in testing with four different OS: Debian, Fedora, macOS, Windows. They reported few problems and suggested some improve- ments.
Lastly, after testing done by teachers, our tools were used as a part of the homework within PV080 course in the summer semester of the academic year 2020/2021. Therefore we got the best circumstances to final test it in real conditions with around 200 participating students. Their homework consists of eight challenges interacting with the local build sandbox. Four of eight challenges were personal challenges using our individual flags that were generated on students’ host. Students started on May 3, 2021, had two weeks to complete homework and submit all captured flags to the CTFd server.
Found issues and suggested improvements
Database-related issues
The first reported problem was that existing users could not be deleted from the CTFd database by administrator using web interface. It was caused by inappropriate design, which required deleting all individual flags of the chosen user before. This problem was solved by changing the database design and updating the code that handles deleting.
The next database-related issue was an indelible Individual flag. It was caused by the originally implemented delete function in CTFd that was not prepare for a situation when one flag is divided and stored in two different database tables. Therefore we overload the delete method in case of the Individual flag. Otherwise, it is used the original delete method.
Windows-related issues
Soon we got the first Windows problem caused by using Linux path syntax. The patch consisted of substitution path stored as one string for path stored as several strings nodes representing directories. Multiple
43
 
5. Testing
strings that are joined (os.path.join [47]) by the correct character based on the current OS solve this problem.
The most serious issue was that Windows needs a slightly different vagrant up command arguments to work with generated variables in the file. Therefore we needed to recognize the OS where our script is executed and then call a valid vagrant up command arguments. The implementation creates a short PowerShell script that ensures correct vagrant arguments are called in the case of Windows OS.
After that, we got reported that our .generated.yml file that should be hidden for the students is visible on Windows. Therefore we needed to implement setting of a hidden attribute on Windows to solve this problem while the file is creating.
Application-related issues
Unlike the other issues, the application contains problem caused by source file content limitations. Our text variable type was generated from the list of 100 quotes. However, there were almost 200 students involved in the testing. It resulted in a situation where only a few students get a unique flag. Therefore cheating detection was not very effective, and we fixed it by appending 500 more quotes into the source file, but the quotes distribution is still not optimal (some quotes are more likely to be generated than the others).
So far, the last discovered problem in our application was failing the sandbox_creator.py script after manually interrupting the sandbox build process. It was caused only on Windows because it was failing to override the already written hidden .generated.yml file. We solve this by skipping writing .generated.yml file if there is already one from the previous run.
Suggested improvements
The first suggestion was to add a username (part of the email) instead of the user ID into log files. This was purely for a practical reason because it is much easier to identify the student from an email address than from the ID that is created after registration to the game. This was implemented by mapping ID on usernames based on data from the database.
44
 
5. Testing
The following suggestion was to preset the arguments matching needs in PV080 course, i.e., path and URL of CTFd. Argparse library supports default values and optional arguments. So we just set a e- mail address as the only obligatory argument, and all others optional arguments were given default values.
Later, it was suggested to ensure that students spend a similar amount of time by cracking credentials with a generated username. In the prototype version, we generated a name from the list that is not included in the cracking tool by default. Therefore we updated our name list file and version number in the library, but we need not change any line of code in the library neither application thanks to our good design. As a result, the new name list caused the time difference between players, which use the crack tool to break username and password, becomes negligible.
Another suggestion was to remove .generated.yml file when it is no more necessary. It will prevent from being disclosed by students that might find the hidden file. We implemented removing the file as soon as it successfully built the sandbox environment.
Later, we were suggested to print a message to the users immedi- ately after starting the application to let them know it is being executed and remove or change all informative or error prints that disclose the generating values. All output strings were updated to describe the existing situation better.
The following suggestion aimed at sentences where generated con- tent might be potentially understood as offensive. Therefore we add fil- tering that hide all inappropriate or offensive words. It is implemented using the better_profanity package that can replace characters in an offensive term for ∗ signs.
 45

6 Conclusion
The rising lack of cybersecurity experts can be solved by training new ones. However, quality training requires spending a lot of effort and time not only from the trainee but also from the tutor. Therefore, it is crucial to make the training process as effective as possible, and it was our motivation to come up with this thesis. One possibility of how it can be achieved is through the cybersecurity games that can be used for a university course as well as competition.
Learning is the first important step, the second equally important is an examination or testing. However, it is hard to monitor students, especially when working remotely on their devices connected to the internet. Cybersecurity games used in a mass-attended subject are a great example of the potential risk of cheating caused by playing in a local sandbox and having the same flags or answers for all students. Some literature reports are showing that solution sharing is happening. Students may realise monitoring difficulties and may try to abuse these assignments to share their flags in order to get better results. Despite that it is against the rules, this behaviour was observed in both academic and competitive environment.
Therefore this thesis is focused on solving this problem and offer a fully functional solution that simplifies randomized assignments preparation. It consists of three elements: application, library and plu- gin for CTFd, a popular game platform. All of them were designed to work together to provide the best experience for teachers and stu- dents and eliminate the negative aspect of these game. In advance, it can enhance practising by solving the same problems with different values.
Students can build their own sandbox with personal challenges and individual flags by executing a Python script. Thanks to Pipenv, all required dependencies are automatically installed, including our library. The application uses a library to generate values of a specific data type defined in the sandbox and then build the sandbox by Va- grant. Students check their founded flags by submitting them to a remote server with our CTFd plugin running on. Besides that, the plugin also logs valuable evidence for further analysis.
47

6. Conclusion
Our prototype was applied in practice within PV080 course home- work containing a newly created sandbox using our solution. Firstly the teachers performed a beta testing and reported some issues, plus proposed a few improvements. We implemented all of it and let stu- dents test their cybersecurity skills on their homework that has inte- grated our solution. After all, students did not feel any discomfort at this type of homework and received feedback was mostly positive. The lesson learned from this deployment will be valuable for future work because we can reflect teachers needs better.
6.1 Future work
The current solution can still be improved by enriching log functional- ity or adding new supported generated types. One way to achieve it can be implementing the Faker Python package that offers multiple various data types. Next, teachers would really appreciate the auto- matic cheating detection, which takes into account log all data. If the indicators are straightforward, the teacher will be notified to resolve the case. For example, if two students submit the same flag from the same IP within few minutes, it most likely indicates cheating.
It is expected that the library will be integrated into the KYPO Cyber Range Platform to enjoy the benefit of this solution in the cloud environment. That will bring a more convenient setup for the stu- dents because it need not install anything. Furthermore, teachers can remotely connect and help students with their individual problem.
We also plan to contribute our CTFd plugin to the official public CTFd plugins Git repository. So far, there is no other publicly accessible solution for this popular platform that would offer similar possibilities like creating personalized challenges for each player. The teachers or competition organizers may also use it for their own cybersecurity games or other assignments. They only need to adapt the application for their use case or generate and upload a flag manually.
Improvement can also be made in the application seed comput- ing algorithm to ensure generation of pseudorandom values. It will positively influence the chance that each player will get generated a unique flag. Next, a nice feature would be encrypting the posted data to decrease the chance of leaking the flag.
48
 
A Archive Content
The archive contains implementation described in Chapter 4 licensed under MIT license. The archive is divided into tree directories:
• Application
Command line application written in Python to generate indi-
vidual flags.
Requirements: Python 3.6, Vagrant, Ansible, Pipenv.
• Library
Python library used in application for generating individual
flags.
Requirements: Python 3.6.
• CTFd plugin
Extension that allows to create personalized challenges within
popular CTF platform.
Requirements: Docker (min : 4 GB RAM, 10 GB available disk space, 2 CPU cores).
Recommended: Docker (min : 8 GB RAM, 20 GB available disk space, 4 CPU cores).
49

Bibliography
1. Lack of experts: A serious shortage of cybersecurity experts could cost companies hundreds of millions of dollars [online]. Shirley Tay, 2019- 03-05 [visited on 2021-03-13]. Available from: https://www.cnbc. com/2019/03/06/cybersecurity-expert-shortage-may-cost- companies-hundreds-of-millions.html.
2. Cybersecurity Workforce Study: A serious shortage of cybersecurity experts could cost companies hundreds of millions of dollars [online]. Shirley Tay, 2020 [visited on 2021-03-14]. Available from: https://www.cnbc.com/2019/03/06/cybersecurity-expert- shortage-may-cost-companies-hundreds-of-millions.html.
3. BURKET, Jonathan; CHAPMAN, Peter; BECKER, Tim; GANAS, Chris; BRUMLEY, David. Automatic Problem Generation for Capture-the-Flag Competitions. In: 2015. Available also from: https : / / www . usenix . org / conference / 3gse15 / summit - program/presentation/burket.
4. VYKOPAL, Jan; ŠVÁBENSKÝ, Valdemar; CHANG, Ee-Chien. Benefits and Pitfalls of Using Capture the Flag Games in Univer- sity Courses. In: Proceedings of the 51st ACM Technical Symposium on Computer Science Education. Portland, OR, USA: Association for Computing Machinery, 2020, pp. 752–758. SIGCSE ’20. isbn 9781450367936. Available from doi: 10.1145/3328778.3366893.
5. KYPO: KYPO Cyber Range Platform [online]. Masaryk University, 2020 [visited on 2021-03-14]. Available from: https://docs.crp. kypo.muni.cz.
6. VYKOPAL., Jan; OSLEJSEK., Radek; CELEDA., Pavel; VIZ- VARY., Martin; TOVARNAK., Daniel. KYPO Cyber Range: Design and Use Cases. In: Proceedings of the 12th International Conference on Software Technologies - Volume 1: ICSOFT, SciTePress, 2017, pp. 310–321. isbn 978-989-758-262-2. Available from doi: 10.5220/0006428203100321.
7. LUGMAYR, Artur; SUTINEN, Erkki; SUHONEN, Jarkko; ISLAS SEDANO, Carolina; HLAVACS, Helmut; SUERO MONTERO, Calkin. Serious storytelling - a first definition and review. Multi-
51

BIBLIOGRAPHY
media Tools and Applications. 2017, vol. 76, pp. 15707–15733. Avail-
able from doi: 10.1007/s11042-016-3865-5.
8. Serious Games: Eight examples that explain all you need to know about serious games and game-based learning [online]. Gamelearn team, 2019-09-18 [visited on 2021-04-16]. Available from: https://www. game-learn.com/all-you-need-to-know-serious-games- game-based-learning-examples/.
9. SAMČOVIĆ, Andreja. Serious games in military applications. Vojnotehnicki glasnik. 2018, vol. 66, pp. 597–613. Available from doi: 10.5937/vojtehg66-16367.
10. BROOKHART, Susan M. Formative Assessment Strategies for Every Classroom, 2nd Edition. ASCD, 2010. isbn 9781416610830. Available also from: https : / / books . google . de / books ? hl = sk & lr = &id = RdJIjmQjGJwC & oi = fnd & pg = PP10 & dq = BROOKHART , +Susan + +formative & ots = QWMcjTxaZO & sig = X5DK1WZwzUEQ0q3Y3FzMo1huyQc & redir _ esc = y # v = onepage & q = BROOKHART%2C%20Susan%20%20formative&f=false.
11. SUSI, Tarja; JOHANNESSON, Mikael; BACKLUND, Per. Serious Games: An Overview. 2007. IKI Technical Reports. Available also from: http://urn.kb.se/resolve?urn=urn:nbn:se:his:diva- 1279.
12. Capture the Flag (CTF): Beginner’s Guide to Capture the Flag (CTF) [online]. Siddarth Singh Negi, 2020-09-23 [visited on 2021-04- 16]. Available from: https://medium.com/@thehackersmeetup/ beginners-guide-to-capture-the-flag-ctf-71a1cbd9d27c.
13. KUCEK, Stela; LEITNER, Maria. An Empirical Survey of Func- tions and Configurations of Open-Source Capture the Flag (CTF) Environments. Journal of Network and Computer Applications. 2020, vol. 151, p. 102470. issn 1084-8045. Available from doi: https: //doi.org/10.1016/j.jnca.2019.102470.
14. DESPEISSE, Mélanie. GAMES AND SIMULATIONS IN INDUS- TRIAL ENGINEERING EDUCATION: A REVIEW OF THE COG- NITIVE AND AFFECTIVE LEARNING OUTCOMES. In: Gothen- burg, Sweden, 2018, pp. 4046–4057. WSC ’18. Available from doi: 10.1109/WSC.2018.8632285.
52
 
BIBLIOGRAPHY
15. TRICKEL, Erik; DISPERATI, Francesco; GUSTAFSON, Eric; KALANTARI, Faezeh; MABEY, Mike; TIWARI, Naveen; SAFAEI, Yeganeh; DOUPÉ, Adam; VIGNA, Giovanni. Shell We Play A Game? CTF-as-a-service for Security Education. In: 2017. Available also from: https://www.usenix.org/conference/ ase17/workshop-program/presentation/trickel.
16. SONG, Jia; ALVES-FOSS, Jim. The DARPA cyber grand challenge: A competitor’s perspective. IEEE Security & Privacy. 2015, vol. 13, pp. 72–76. Available from doi: 10.1109/MSP.2015.132.
17. CTFtime: CTF archive and scoreboard [online]. CTFtime team, 2021 [visited on 2021-04-13]. Available from: https://ctftime.org/.
18. CYBER SECURITY COMPETITIONS: A COMPREHENSIVE LIST OF CYBER SECURITY COMPETITIONS [online]. Cyber Security Degrees, 2021 [visited on 2021-04-05]. Available from: https: //www.cybersecuritydegrees.com/faq/comprehensive-list- of-cyber-security-competitions/.
19. WILIAM, Dylan. Formative Assessment: Getting the Focus Right. Educational Assessment. 2006, vol. 11, pp. 283–289. Available from doi: 10.1207/s15326977ea1103&4_7.
20. FORMATIVE ASSESSMENT: 7 Smart, Fast Ways to Do Formative Assessment [online]. Laura Thomas, 2019-04-26 [visited on 2021- 04-13]. Available from: https://www.edutopia.org/article/7- smart-fast-ways-do-formative-assessment.
21. ŠVÁBENSKÝ, Valdemar. Toward an Automated Feedback System in Educational Cybersecurity Games [online]. 2019. Available also from: Dostupn%C3%A9%20z%20WWW%20%3Chttps://theses.cz/ id/klihrn/%3E.
22. SZABO, Claudia; FALKNER, Nickolas. Silence, Words, or Grades: The Effects of Lecturer Feedback in Multi-Revision Assignments. In: Proceedings of the 2017 ACM Conference on Innovation and Tech- nology in Computer Science Education. Bologna, Italy: Association for Computing Machinery, 2017, pp. 293–298. ITiCSE ’17. isbn 9781450347044. Available from doi: 10.1145/3059009.3059030.
53
 
BIBLIOGRAPHY
23. Summative Assessment: Summative assessments are used to evaluate student learning, skill acquisition, and academic achievement at the conclusion of a defined instructional period [online]. Sean Scribner, 2013-08-23 [visited on 2021-04-15]. Available from: https://www. edglossary.org/summative-assessment/.
24. Summative Assessment: 9 Summative Assessment Examples to Try This School Year [online]. Jordan Nisbet, 2019-01-30 [visited on 2021-04-15]. Available from: https://www.prodigygame.com/ main-en/blog/summative-assessment/.
25. VYKOPAL, Jan; VIZVARY, Martin; OSLEJSEK, Radek; CELEDA, Pavel; TOVARNAK, Daniel. Lessons learned from complex hands- on defence exercises in a cyber range. In: 2017 IEEE Frontiers in Education Conference (FIE). 2017, pp. 1–8. Available from doi: 10.1109/FIE.2017.8190713.
26. NATVIG, Kurt. Sandbox technology inside AV scanners. VIRUS. 2001, vol. 475. Available also from: https://vxug.fakedoma. in / archive / other / VxHeavenPdfs / Sandbox % 20Technology % 20Inside%20AV%20Scanners.pdf.
27. KYPO Cyber Range Platform: Documentation [online]. Masaryk University, 2020 [visited on 2021-04-28]. Available from: https: //docs.crp.kypo.muni.cz.
28. VYKOPAL, Jan; BARTÁK, Miloš. On the Design of Security Games: From Frustrating to Engaging Learning. In: 2016 USENIX Workshop on Advances in Security Education (ASE 16). Austin, TX: USENIX Association, 2016. Available also from: https : / / www . usenix . org / conference / ase16 / workshop - program/presentation/vykopal.
29. HASHIMOTO, Mitchell. Vagrant: up and running: create and manage virtualized development environments. " O’Reilly Media, Inc.", 2013. isbn 9781449335830. Available also from: https : //books.google.de/books?hl=sk&lr=&id=7rJqqKCvdagC& oi=fnd&pg=PR2&dq=9781449335830&ots=qDxy_qfSE5&sig= 7Mk33BPs3U6tZ5O5ICZvOPUCcdU & redir _ esc = y # v = onepage & q = 9781449335830&f=false.
54
 
BIBLIOGRAPHY
30. MATHURA ̄MOHANA, Goswa ̄m ̄ı; RAMESH, Raithatha.
Learning Ansible: use Ansible to configure your systems, deploy software, and orchestrate advanced IT tasks. Packt Publish- ing, 2014. isbn 9781783550647. Available also from: https : //books.google.de/books?id=WceiBQAAQBAJ&lpg=PT8&ots= y5PFIjrSDV&dq=RAMESH%2C%20Raithatha&lr&hl=sk&pg=PT8#v= onepage&q=RAMESH,%20Raithatha&f=false.
31. CTFd: Capture The Flag framework [online]. New York City: Kevin Chung, 2017/2020 [visited on 2021-11-03]. Available from: http: //ctfd.io.
32. CHUNG, Kevin. Live lesson: Lowering the barriers to capture the flag administration and participation. In: 2017 {USENIX} Workshop on Advances in Security Education ({ASE} 17). 2017. Available also from: https://www.usenix.org/conference/ ase17/workshop-program/presentation/chung.
33. CTFd plugins: Writing CTFd plugins: a beginner walkthrough [on- line]. Gregoire Lodi, 2019 [visited on 2021-05-11]. Available from: https://medium.com/@gregoire.lodi/writing-ctfd- plugins-a-beginner-walkthrough-7d0b93eb89e7.
34. Flask documentation: Welcome to Flask’s documentation. Get started with Installation and then get an overview with the Quickstart. There is also a more detailed Tutorial that shows how to create a small but complete application with Flask. Common patterns are described in the Patterns for Flask section. The rest of the docs describe each component of Flask in detail, with a full reference in the API section. [Online]. Pallets, 2010 [visited on 2021-05-21]. Available from: https:// flask.palletsprojects.com/en/2.0.x/.
35. Jinja documentation: Jinja is a fast, expressive, extensible templating en- gine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final doc- ument. [Online]. Pallets, 2007 [visited on 2021-05-21]. Available from: https://jinja.palletsprojects.com/en/3.0.x/.
36. SQLAlchemy documentation: The Python SQL Toolkit and Object Relational Mapper [online]. Michael Bayer, 2007 [visited on 2021- 05-21]. Available from: https://www.sqlalchemy.org.
55
 
BIBLIOGRAPHY
37. Pipenv: Python Dev Workflow for Humans [online]. Kenneth Reitz, 2020 [visited on 2021-03-18]. Available from: https://pipenv- fork.readthedocs.io/en/latest/.
38. Argparse documentation: Parser for command-line options, arguments and sub-commands [online]. Steven J. Bethard, 2021 [visited on 2021-05-07]. Available from: https://docs.python.org/3/ library/argparse.html.
39. YAML: YAML Ain’t Markup Language (YAMLTM) [online]. Oren Ben-Kiki, Clark Evans, Ingy döt Net, 2009 [visited on 2021-03-29]. Available from: https://yaml.org/spec/1.2/spec.html# id2759963.
40. JAGANNATAM, Archana. Mersenne Twister – A Pseudo Random Number Generator and its Variants. 2010. Available also from: https://www.researchgate.net/publication/ 267968705 _ Mersenne _ Twister_ - _A _ Pseudo _ Random _ Number _ Generator_and_its_Variants.
41. BAYER, Michael. SQLAlchemy. In: BROWN, Amy; WILSON, Greg (eds.). The Architecture of Open Source Applications Volume II: Structure, Scale, and a Few More Fearless Hacks. aosabook.org, 2012. Available also from: http : / / aosabook . org / en / sqlalchemy . html.
42. CODD, E. F. A Relational Model of Data for Large Shared Data Banks. Commun. ACM. 1970, vol. 13, no. 6, pp. 377–387. issn 0001- 0782. Available from doi: 10.1145/362384.362685.
43. SINGH, Charanjot; GABA, Nikita Seth; KAUR, Manjot; KAUR, Bhavleen. Comparison of Different CI/CD Tools Integrated with Cloud Platform. In: 2019 9th International Conference on Cloud Computing, Data Science Engineering (Confluence). 2019, pp. 7–12. Available from doi: 10.1109/CONFLUENCE.2019.8776985.
44. Docker: Documentation [online]. Docker Inc., 2021 [visited on 2021-05-03]. Available from: https://docs.docker.com.
45. ANDERSON, Charles. Docker [Software engineering]. IEEE Soft- ware. 2015, vol. 32, no. 3, pp. 102–c3. Available from doi: 10.1109/ MS.2015.62.
56
 
BIBLIOGRAPHY
46. Released: Docker Desktop for Mac: Today we are excited to announce the general availability of Docker Desktop for Mac [Apple Silicon], continuing to support developers in our community with their choice of local development environments. [Online]. DIEU CAO, 2021 [visited on 2021-05-03]. Available from: https://www.docker.com/blog/ released-docker-desktop-for-mac-apple-silicon/.
47. os.path documentation: Common pathname manipulations [online]. Python Software Foundation, 2021 [visited on 2021-05-07]. Avail- able from: https://docs.python.org/3/library/os.path. html.
 57

"""
print(qa_model(question = question, context = context))
