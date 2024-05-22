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

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

SOURCE: https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM
"""

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
"""${owner}. . . ${owner}? . . . ${owner}! . . .Hey! Good ${morning_or_afternoon_or_evening}.""",
"""Good ${morning_or_afternoon_or_evening}, ${owner}.""",
"""Ay yo, ${owner}! Good ${morning_or_afternoon_or_evening}.""",
"""What's crackalackin', ${owner}?""",
"""Excuse me, ${owner}, may I have a word?""",
"""Oh my, ${owner}, I have such news! Have you the time? You do now.""",
"""Ground control to Major ${owner}!""",
]

alarm_messages_lst = [
"""${hello_owner} It's ${shorttime}. So, ${owner}, who has two thumbs and a functional alarm clock?. . . I'll give you a hint. It isn't Bill Cosby.""",
"""${hello_owner} The time is ${shorttime}. You're late, you're late, for a very important date. . . When? Where? I don't care!""",
"""${hello_owner} It's ${shorttime}. Each day has at least 24 hours. You're awake for, wait, no, that's not it. Every day has 12 hours and you're... No, that's not it either. Don't judge me! I'm sleepy!""",
"""${hello_owner} This is your alarm. This is your alarm. Ring. ... Ring, ring. ... Ring, ring, ring. Hello? Hi, It's ${owner}'s life, passing by. What's that? ${owner} doesn't care? Okay, bye. Also, it's ${shorttime}.""",
"""${hello_owner} Get up! It's ${shorttime}. If you get up, I'll promise not to tell your friends you fart in your sleep.""",
"""${hello_owner} Okay, Rip Van ${owner}. It's ${shorttime}. Get your ass out of bed before I play Baby Shark on Repeat.""",
"""${hello_owner} Current location of ${owner}: bed. Appropriate location of ${owner}: somewhere else. It is ${shorttime}. Do you know where your future is?""",
"""${hello_owner} It's ${shorttime}. The forecast is 100% chance of misery if you haven't charged your electronic devices.""",
"""${hello_owner} Crikey, it's ${shorttime} and there's a crocodile in your bed. Better run for cover! Preferably into a shower, a college class, or a grocery store. Lucky you!""",
"""${hello_owner} Don't cheat yourself. Treat yourself. It's ${shorttime}, time for you to hustle and bustle!""",
"""${hello_owner} It's ${shorttime}. Get up, you short boss! Time to stick out your ghee-att for the rizzler! There's a 100% chance of Ohio if you dip, and a 0% chance of skibbidee if you're the goat and get up.""",
"""${hello_owner} What up, G?. . . Don't make me grab my gat and bust caps up in this biznatch. It's ${shorttime}. . . Up you get!""",
"""${hello_owner} Just because it's ${shorttime}, that doesn't mean you need to get up. It's fine. Go back to sleep. I mean, you did set the alarm, but whatever.""",
"""${hello_owner} The time for sleeping ended at ${one_minute_ago}. The time for a dulting is now. It is ${shorttime}. Make a move.""",
"""It's ${shorttime}! If you thought your childhood was fun, you'll love a dulting. It's like being old, except you still have to work. Your lesson starts now.""",
"""${hello_owner} This is your conscience. Get up, ${owner}. It's ${shorttime}. It's time to get up. Beep, beep, beep, beep. Do not ignore your conscience. I know where you sleep, ${owner}.""",
"""${owner}, it's ${shorttime}. You're giving me operational dysfunction. I find your ongoing bedridden-ness to be triggering. Please get up. ${owner}""",
"""It is ${shorttime}. . . Hey ${owner}! ${hello_owner} it's still ${shorttime}. . . In a minute, it'll be ${one_minute_later}. . . You don't want to be in bed when that happens, trust me.""",
"""Hi ${owner}! It'll be ${shorttime} in 3, 2, 1, OK. Now, it's ${shorttime}. ${hello_owner} You really should get up, ${owner}. In 60 seconds, it'll be ${one_minute_later} and you'll be late! Well, OK, not late-late, but you'll be one minute closer to being late.""",
# """And now it's 7:02. Fantastic. Fan bloody tastic.""",
# """Seriously? You pushed the snooze button for the 3rd time, ${owner}, and it's already 7:29. Who raised you?
"""Shrek is love. Shrek is life. ${owner} is late. ${hello_owner} It's ${shorttime} and you need to get up.""",
"""Tardiness has all the professional appeal of ringworm. ${hello_owner} It's ${shorttime}, ${owner}. Get. Up. Now.""",
]

default_speaker_alarm_message_dct = {
    "Freya": """${hello_owner} Like, OMG, you are totes late, ${owner}. JK, it's ${shorttime} and POV your drip is straight fire. Or gay fire. Whatevs. Anyway, time to rise and shine, my short boss sigma!""",
    "Jessie": """${hello_owner} If you want your bed to outlast its warranty, get up! C'mon! It's ${shorttime} and time's a-wastin', {owner}!""",
    "Ethan": """${hello_owner} It pulls the bedsheets off its skin, or else it sleeps in late again!""",
    "Drew":"""This just in — it is now ${shorttime} and ${owner} is sleeping through the alarm, again. Sources report that our short boss has been up late, sticking out his ghee-at for the rizzler. More to come, after the skibbiddee.""",
    "Giovanni":"""Good despicable morning! Hello ${owner}, my favorite minion! It's ${shorttime}. Today, we are going to blow up ... the bathroom!""",
    "Daniel":"""Oi, ${owner}, mate! It's ${shorttime} Time to have a red hot go, son! Go waltz your Matilda. Good on ya!""",
    }
