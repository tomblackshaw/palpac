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
