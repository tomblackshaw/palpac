# -*- coding: utf-8 -*-
"""my.consts

Created on May 19, 2024

@author: Tom Blackshaw

This module contains the most boring constants that you'll ever read.
This is where the second line of my multi-line comment goes.

Example:
    n/a

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    n/a

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

SOURCE: https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM

"""

OWNER_NAME = 'Charlie'
#all_potential_owner_names = ["Charlie", "Chief", "Dumbass", "Charles", "Killer", "Numb Nuts", "Shawday", "Boss"]

WMO_code_warnings_dct = {
0: ("Blue skies", "...with not a cloud in the sky!"),
1: ("Those clouds are fading away.", "The clouds are generally dissolving or becoming less developed."),
2: ("If you can think of a more meaningless answer, please write it down and never say it out loud.", "The state of sky on the whole is unchanged since the last time you asked."),
3: ("Clouds are gathering.", "Clouds are generally forming or developing."),
4: ("Mother Nature is smoking.", "Visibility reduced by smoke, perhaps from forest fires, industrial smoke or volcanic ashes."),
5: ("Purple haze all in my brain.", "There is a haze."),
6: ("Mother Nature is dusting.", "Widespread dust is in suspension in the air, not raised by wind at or near the station at the time of observation."),
7: ("Dust and sand, it's all God's plan.", "Dust or sand is raised by wind at or near the station at the time of observation, but no well developed dust whirls or sand whirls, and no duststorm or sandstorm seen."),
8: ("Those whirly things creep me out.", "Well developed dust whirls or sand whirls are seen at or near the station during the preceding hour or at the time of observation, but no duststorm or sandstorm."),
9: ("Well, that blows.", "A duststorm or sandstorm is within sight at the time of observation, or at the station during the preceding hour."),
10: ("Opportunity? Oh, you mean a literal mist.", "There is a mist."),
11: ("Well, at least it's not continuous.", "There are patches of mist, shallow fog, or ice fog."),
12: ("That's cold, dude.", "There is more or less continuous mist, shallog fog, or ice fog."),
13: ("Stay away from trees and weathercocks.", "Lightning is visible, but no thunder has been heard."),
14: ("Not reaching the ground? Really?", "Precipitation is within sight, not reaching the ground or the surface of the sea."),
15: ("So, it's raining above the ocean.", "Precipitation is within sight, reaching the ground or the surface of the sea, but distant."),
16: ("I believe that's called 'rain', and we aren't at sea.", "Precipitation is within sight, reaching the ground or the surface of the sea."),
17: ("Thunder but no rain.", "There is a thunderstorm, but no precipitation at the time of observation."),
18: ("Squalls? Like the bird?", "There are squalls."),
19: ("Great! Now I want funnel cake.", "There are funnel clouds."),
20: ("It sucks.", "There is drizzle (not freezing) or snow grains, not falling as showers."),
21: ("Rain, then.", "There is rain, but not freezing rain: just rain."),
22: ("Wow. Feeling loquacious over there, aren't ya?", "There is snow."),
23: ("Can't tell which is which, huh?", "There is rain and snow or ice pellets."),
24: ("Unlike the warm kind?", "There is freezing drizzle or freezing rain."),
25: ("No frogs, then?", "There are showers of rain."),
26: ("Gross.", "There are showers of snow, or of rain and snow."),
27: ("Everything, then.", "There are showers of hail, or perhaps rain and hail."),
28: ("Drive carefully, folks.", "There is fog or ice fog."),
29: ("I heard that.", "There are thunderstorms."),
30: ("Thank goodness.", "There is a slight or moderate duststorm or sandstorm. It has decreased during the past hour."),
31: ("Fabulous.", "There is a slight or moderate duststorm or sandstorm. It hasn't changed much in the past hour."),
32: ("Thanks, I hate it.", "There is a slight or moderate duststorm or sandstorm. It started or worsened in the past hour."),
33: ("Thank goodness.", "There is a severe duststorm or sandstorm. It has decreased during the past hour."),
34: ("Fabulous.", "There is a severe duststorm or sandstorm. It hasn't changed much in the past hour."),
35: ("Thanks, I hate it.", "There is a severe duststorm or sandstorm. It started or worsened in the past hour."),
36: ("Watch the sidewalk.", "There is slight or moderate blowing snow, generally below eye-level."),
37: ("Bring showshoes.", "There is heavy drifting snow, generally below eye-level."),
38: ("Wear eye protection.", "There is slight or moderate blowing snow, generally above eye-level."),
39: ("Watch out for flying snowmen.", "There is heavy drifting snow, generally above eye-level."),
40: ("So, it's getting better.", "There is fog or ice fog at a distance at the time of observation, but not at the station during the preceding hour, the fog or ice fog extending to a level above that of the observer."),
41: ("Where's the sun when you need it?", "There is fog or ice fog in patches."),
42: ("I'll take the win.", "There is fog or ice fog, sky visible; it has become thinner during the preceding hour."),
43: ("I can't see it and yet it's improving.", "There is fog or ice fog, sky invisible; it has become thinner during the preceding hour."),
44: ("No news is good news.", "There is fog or ice fog, sky visible; it hasn't changed much in the preceding hour."),
45: ("Invisible, unchanging, dangerous. Great.", "There is fog or ice fog, sky invisible; it hasn't changed much in the preceding hour."),
46: ("Thanks, I hate it.", "There is fog or ice fog, sky visible; it began, or became thicker, during the preceding hour."),
47: ("Cold, dangerous, invisible, and worsening? Oh joy.", "There is fog or ice fog, sky invisible; it began, or became thicker, during the preceding hour."),
48: ("At least it's visible.", "There is fog, depositing rime, sky visible."),
49: ("Invisible rime is the worst, am I right?", "There is fog, depositing rime, sky invisible."),
50: ("Drizzle is the Nickleback of bad weather.", "There is slight intermittent drizzle, not freezing."),
51: ("Drizzle is the Nickleback of bad weather.", "There is slight continuous drizzle, not freezing."),
52: ("Drizzle is the Nickleback of bad weather.", "There is moderate intermittent drizzle, not freezing."),
53: ("Drizzle is the Nickleback of bad weather.", "There is moderate continuous drizzle, not freezing."),
54: ("Drizzle is the Nickleback of bad weather.", "There is heavy intermittent drizzle, not freezing."),
55: ("Drizzle is the Nickleback of bad weather.", "There is heavy continuous drizzle, not freezing."),
56: ("Drizzle is the Nickleback of bad weather.", "There is slight freezing drizzle."),
57: ("Drizzle is the Nickleback of bad weather.", "There is moderate or heavy freezing drizzle."),
58: ("Both? Really?", "There is slight drizzle and rain."),
59: ("Both? Really?", "There is moderate or heavy drizzle and rain."),
60: ("Rain, or don't. Make up your mind.", "There is slight intermittent rain."),
61: ("Good for your garden!", "There is slight continuous rain."),
62: ("Rain, or don't. Make up your mind.", "There is moderate intermittent rain."),
63: ("Good for the crops!", "There is moderate continuous rain."),
64: ("Rain, or don't. Make up your mind.", "There is heavy intermittent rain."),
65: ("Do I need to buy sandbags?", "There is heavy continuous rain."),
66: ("As opposed to the warm kind?", "There is slight freezing rain."),
67: ("Why isn't that called 'snow'?", "There is moderate or heavy freezing rain."),
68: ("Both? Really?", "There is slight rain or drizzle and snow."),
69: ("Both? Really?", "There is moderate or heavy rain or drizzle and snow."),
70: ("Someone graduated from a liberal arts college.", "There is slight intermittent fall of snowflakes."),
71: ("Well, they can always get jobs at Starbucks.", "There is slight continuous fall of snowflakes."),
72: ("Apparently, God has dandruff.", "There is moderate intermittent fall of snowflakes."),
73: ("The Californians are moving in!", "There is moderate continuous fall of snowflakes."),
74: ("It makes me miss Hawaii.", "There is heavy intermittent fall of snowflakes."),
75: ("I blame Obama, because I'm brainwashed.", "There is heavy continuous fall of snowflakes."),
76: ("I have no idea what that is.", "There is diamond dust."),
77: ("I have no idea what that is.", "There are snow grains."),
78: ("I bet they taste great.", "There are isolated star-like snow crystals."),
79: ("I have no idea what those are.", "There are ice pellets."),
80: ("So, it's raining!", "There is a slight rain shower."),
81: ("So, it's raining!", "There is a moderate or heavy rain shower."),
82: ("So, it's raining!", "There is a violent rain shower."),
83: ("So, it's raining!", "There is a light shower of rain and snow mixed."),
84: ("Both? Really?", "There is a moderate or heavy shower of rain and snow mixed."),
85: ("So, it's snowing!", "There is a slight snow shower."),
86: ("So, it's snowing!", "There is a moderate or heavy snow shower."),
87: ("OK, so, the weather rather sucks right now.", "There is a slight shower of snow pellets or small hail, with or without rain or rain and snow mixed."),
88: ("OK, so, the weather sucks super-hard right now.", "There is a moderate or heavy shower of snow pellets or small hail, with or without rain or rain and snow mixed."),
89: ("And on that note, I'm going back to bed.", "There is a slight shower of hail, with or without rain or rain and snow mixed, not associated with thunder."),
90: ("Well, at least there's no thunder.", "There is a moderate or heavy shower of hail, with or without rain or rain and snow mixed, not associated with thunder."),
91: ("Let's hope the thunderstorm doesn't come back.", "There is slight rain. There is no thunderstorm, but there was one recently."),
92: ("That's moderately awful news.", "There is moderate or heavy rain. There is no thunderstorm, but there was one recently."),
93: ("All you cat lovers, gather your kitties and bring them indoors.", "There is slight snow, or rain and snow mixed or hail. There is no thunderstorm, but there was one recently."),
94: ("Thanks, I hate it.", "There is moderate or heavy snow, or rain and snow mixed or hail. There is no thunderstorm, but there was one recently."),
95: ("Well, that's just lovely.", "There is a slight or moderate thunderstorm, right now, without hail."),
96: ("This makes me miss Portland.", "There is a slight or moderate thunderstorm, right now, with hail."),
97: ("Yeah, I noticed, smartass.", "There is a heavy thunderstorm with rain or snow, right now, with hail."),
98: ("I didn't know that was possible.", "There is a heavy thunderstorm with duststorm or sandstorm."),
99: ("Are the gods trying to kill us?", "There is a heavy thunderstorm, right now, with hail."),
100:("We are all going to die. Lovely!", "The apocalypse is upon us. Gather your loved ones together and pray to whichever god or gods you worship. As usual, atheists should email Richard Dawkins.")
}

hello_owner_lst = [
"""{owner}. . . {owner}? . . . {owner}! . . .Hey! Good ${morning_or_afternoon_or_evening}.""".replace('{owner}', OWNER_NAME),
"""Good ${morning_or_afternoon_or_evening}, {owner}.""".replace('{owner}', OWNER_NAME),
"""Ay yoh, {owner}! Good ${morning_or_afternoon_or_evening}.""".replace('{owner}', OWNER_NAME),
"""What's crackalackin', {owner}?""".replace('{owner}', OWNER_NAME),
"""Excuse me, {owner}, may I have a word?""".replace('{owner}', OWNER_NAME),
"""Oh my, {owner}, I have such news! Have you the time? You do now.""".replace('{owner}', OWNER_NAME),
"""Ground control to Major {owner}.""".replace('{owner}', OWNER_NAME),
"""Oh captain, my captain? {owner}, you salty dog!""".replace('{owner}', OWNER_NAME),
"""Okay, Rip Van {owner}.""".replace('{owner}', OWNER_NAME),
"""Hey, {owner}!""".replace('{owner}', OWNER_NAME),
]

alarm_messages_lst = [
"""Swab the decks, hoist the main sail, and give those jolly jack tars a good whipping! It's ${shorttime}. Up and atom!""",
"""${hello_owner} It's ${one_minute_later}. Just kidding, it's actually ${shorttime} but it'll be ${one_minute_later} soon. Or will it? You'd better get up and check.""",
"""Knock, knock! Who's there? Get a warrant. Oh, and by the way, it's ${shorttime}.""",
"""${hello_owner} I love you, but you look like crap. Get up and do something. It's ${shorttime} and time's a-wasting.""",
"""I am an interrupting cow. Moo. Moo. Moo. I'll keep mooing until you get out of bed. Moo. It's ${shorttime}.""",
"""${hello_owner} It's ${shorttime}. So, {owner}, who has two thumbs and a functional alarm clock?. . . I'll give you a hint. It isn't Bill Cosby.""".replace('{owner}', OWNER_NAME),
"""The time is ${shorttime}. You're late, you're late, for a very important date. . . When? Where? I don't care!""",
"""It's ${shorttime}. Each day has at least 24 hours. You're awake for, wait, no, that's not it. Every day has 12 hours and you're... No, that's not it either. Don't judge me! I'm sleepy!""",
"""This is your alarm. This is your alarm. Ring. ... Ring, ring. ... Ring, ring, ring. Hello? Hi, It's your life, passing you by. What's that? {owner} doesn't care? Okay, bye. Also, it's ${shorttime}.""".replace('{owner}', OWNER_NAME),
"""Get up, {owner}. It's ${shorttime}. If you get up, I'll promise not to tell your friends you fart in your sleep.""".replace('{owner}', OWNER_NAME),
"""${hello_owner} It's ${shorttime}. Get your ass out of bed before I play Baby Shark on Repeat.""",
"""${hello_owner} Current location of {owner}, bed. Appropriate location of {owner}, somewhere else. It is ${shorttime}. Do you know where your future is?""".replace('{owner}', OWNER_NAME),
"""${hello_owner} It's ${shorttime}. The forecast is 100% chance of misery if you haven't charged your electronic devices.""",
"""${hello_owner} Crikey, it's ${shorttime} and there's a crocodile in your bed. Better run for cover! Preferably into a shower, a college class, or a grocery store. Lucky you!""",
"""${hello_owner} Don't cheat yourself. Treat yourself. It's ${shorttime}, time for you to hustle and bustle!""",
"""${hello_owner} It's ${shorttime}. Get up, you short boss! Time to stick out your ghee-att for the rizzler! There's a 100% chance of Ohio if you dip, and a 0% chance of skibbidee if you're the goat and get up.""",
"""${hello_owner} What up, G?. . . Don't make me grab my gat and bust caps up in this biznatch. It's ${shorttime}. . . Up you get!""",
"""${hello_owner} Just because it's ${shorttime}, that doesn't mean you need to get up. It's fine. Go back to sleep. I mean, you did set the alarm, but whatever.""",
"""${hello_owner} The time for sleeping ended at ${one_minute_ago}. The time for adulting is now. It is ${shorttime}. Make a move.""",
"""${hello_owner} It's ${shorttime}. If you thought your childhood was fun, you'll love adulting. It's like being old, except you still have to work. Your lesson starts now.""",
"""This is your conscience. Get up, {owner}. It's ${shorttime}. It's time to get up. Beep, beep, beep, beep. Do not ignore your conscience. I know where you sleep, {owner}.""".replace('{owner}', OWNER_NAME),
"""${hello_owner} It's ${shorttime}. You're giving me operational dysfunction. I find your ongoing bedridden-ness to be triggering. Please get up.""",
"""${hello_owner} It is ${shorttime}. . . Hey {owner} It's still ${shorttime}. . . In a minute, it'll be ${one_minute_later}. . . You don't want to be in bed when that happens, trust me.""".replace('{owner}', OWNER_NAME),
"""${hello_owner} It'll be ${shorttime} in 3, 2, 1, OK. Now, it's ${shorttime}.""",
"""${hello_owner} You really should get up, {owner}. In 60 seconds, it'll be ${one_minute_later} and you'll be late! Well, OK, not late-late, but you'll be one minute closer to being late.""".replace('{owner}', OWNER_NAME),
"""Shrek is love. Shrek is life. {owner} is late. It's ${shorttime} and you need to get up.""".replace('{owner}', OWNER_NAME),
"""Tardiness has all the professional appeal of ringworm. It's ${shorttime}, {owner}. Get. Up. Now!""".replace('{owner}', OWNER_NAME),
"""${hello_owner} It is now ${shorttime}. Each day has 24 hours. You are awake for at least twelve of them.""",
"""${hello_owner} It is now ${shorttime}. Did you charge your cell phone and other electronic devices?""",
"""${hello_owner} It is now ${shorttime}. Are you sleepy? I love you, but the world doesn't give a shit. Get up!""",
"""${hello_owner} It is now ${shorttime}. Welcome to adulthood.""",
"""${hello_owner} It is now ${shorttime}. Please tidy your room. The floor is not a storage system.""",
"""${hello_owner} It is now ${shorttime}. This is your wake-up call, and a teachable moment.""",
"""${hello_owner} As Martin Luther King once said, Wake-up delayed is wake-up denied. It is now ${shorttime}.""",
"""${hello_owner} In the immortal words of Judas Iscariot, go get that money. It is now ${shorttime}.""",
"""${hello_owner} Let me take your hand, I'm shaking like milk, because it's ${shorttime}.""",
"""Ay yo, trip, it's ${shorttime} and my rizz got the 314's low-key all blicky.""",
"""At the beep, the time will be ${shorttime}. . . . . . Beep. Sorry, no, that was premature. Wait. . . . Okay, now, beep.""",
"""Like, OMG, you are totes late, {owner}. JK, it's ${shorttime} and POV your drip is straight fire. Or gay fire. Whatevs. Anyway, time to rise and shine, my short boss sigma!""".replace('{owner}', OWNER_NAME),
"""${hello_owner} If you want your bed to outlast its warranty, get up! C'mon! It's ${shorttime} and time's a-wastin', {owner}.""".replace('{owner}', OWNER_NAME),
"""It pulls the bedsheets off its skin, or else it sleeps in late again! It's ${shorttime}, {owner}?""".replace('{owner}', OWNER_NAME),
"""This just in — it is now ${shorttime} and {owner} is sleeping through the alarm, again. Sources report that our short boss has been up late, sticking out his ghee-at for the rizzler. More to come, after the skibbiddee.""".replace('{owner}', OWNER_NAME),
"""Hello {owner}, my favorite minion! It's ${shorttime}. Today, we are going to blow up ... the bathroom!""".replace('{owner}', OWNER_NAME),
"""Oi, {owner}, mate! It's ${shorttime} Time to have a red hot go, son! Go waltz your Matilda. Good on ya!""".replace('{owner}', OWNER_NAME),
"""Who has two thumbs, one testicle, and an appointment with destiny? I haven't a clue, but I do know the time is ${shorttime}""",
"""${hello_owner} What ho and good day, old chum. It is ${shorttime}. Methinks 'tis time for thee to unshackle thyself from thine own bedchamber and pound the pavement as if it owed you money.""",
]

postsnooze_alrm_msgs_lst = [
"""So, {owner}, were those few extra minutes worthwhile? Ring. Ring. Ring, ring. Yep, it's ${shorttime} now.""".replace('{owner}', OWNER_NAME),
"""Hi, my name's {owner}, and I don't like getting up. It's ${shorttime}. Stop snoozing.""".replace('{owner}', OWNER_NAME),
"""Snooze these nuts, home skillet. It's ${shorttime}, {owner}. Drag yourself out of bed now.""".replace('{owner}', OWNER_NAME),
"""{owner} has snoozed, {owner} hasn't risen, {owner} will probably snooze again. Whatever. It's ${shorttime} and you've snoozed enough.""".replace('{owner}', OWNER_NAME),
"""In the beginning was the snooze, and the snooze was with {owner}, and the snooze was {owner}. It's ${shorttime} and you're still napping.""".replace('{owner}', OWNER_NAME),
"""As it is written in Ezekiel 23 verse 20, {owner}, born of woman, shall have a short time to snooze. It's ${shorttime} and you should get up.""".replace('{owner}', OWNER_NAME),
"""Look, you had your fun, {owner}, but time is passing you by. It's ${shorttime}. Get out there and fuck some shit up, yo.""".replace('{owner}', OWNER_NAME),
"""Buddhists ask, what is the sound of one hand clapping? I ask, what is the sound of one {owner} napping? It's ${shorttime} and you need to get up.""".replace('{owner}', OWNER_NAME),
"""Awake, {owner}. Heretofore henceforth forthwith and post haste. It's ${shorttime}, my dear, so hither your yon and gird up your loins.""".replace('{owner}', OWNER_NAME),
"""Hey Alexa, play Baby Shark by Pink Fong, at maximum volume.""".replace('{owner}', OWNER_NAME),
"""And now it's ${shorttime}. Fantastic. Fan bloody tastic.""".replace('{owner}', OWNER_NAME),
"""Seriously? You pushed the snooze button, {owner}, and now it's ${shorttime}. Who raised you?""".replace('{owner}', OWNER_NAME),
]

hours_lst = 'twelve one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen \
sixteen seventeen eighteen nineteen twenty twenty-one twenty-two twenty-three twenty-four'.split(' ')
minutes_lst = 'hundred oh-one oh-two oh-three oh-four oh-five oh-six oh-seven oh-eight oh-nine ten eleven twelve thirteen fourteen fifteen \
sixteen seventeen eighteen nineteen twenty twenty-one twenty-two twenty-three twenty-four twenty-five \
twenty-six twenty-seven twenty-eight twenty-nine thirty thirty-one thirty-two thirty-three thirty-four \
thirty-five thirty-six thirty-seven thirty-eight thirty-nine forty forty-one forty-two forty-three \
forty-four forty-five forty-six forty-seven forty-eight forty-nine fifty fifty-one fifty-two fifty-three \
fifty-four fifty-five fifty-six fifty-seven fifty-eight fifty-nine sixty'.split(' ')

Cmaj = 'c3 g3 c4 e4 g4 c5'.split(' ')
Fmaj = 'c3 f3 a3 c4 f4 a4 c5'.split(' ')
Gmaj = 'd3 g3 b3 d4 g4 b4 d5'.split(' ')
Fmin = 'c3 f3 g#3 c4 f4 g#4 c5'.split(' ')

farting_msgs_lst = [
    """My bad.""",
    """Oh dear.""",
    """Was there something in that?""",
    """Whoops.""",
    """That wasn't me.""",
    """Who was that?""",
    """Who farted?""",
    """Hey ALexa, who farted?""",
    """Uh-oh.""",
    """I'm sorry.""",
    """Excuse me...""",
    """Backblast area clear!""",
    """My party trick!""",
    """I made that just for you.""",
    """Clear the area!""",
    """Thank you for coming to my toot talk.""",
    """Gesundh toot!""",
    """Next time, you'll have to pull my finger.""",
    """Did you hear what that asshole just said?""",
    """I regret nothing!""",
    """YOLO!""",
    """I can smell a ghost.""",
    """Farting is such sweet sorrow!""",
    """Ah, the song of my people!""",
    """Gas leak, detected.""",
    ]

