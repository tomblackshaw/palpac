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

hello_owner_lst = [
"""Lovely ${morning_or_afternoon_or_evening}, ${owner}""",
"""Good ${morning_or_afternoon_or_evening}, ${owner}""",
"""Hi, ${owner}""",
"""What a lovely ${morning_or_afternoon_or_evening}, ${owner}""",
"""What up, ${owner}""",
"""Yo ${owner}""",
"""What it do, ${owner}""",
"""${owner}! Bruh!""",
"""${owner}! What the sigma?""",
"""What up, my rizzler!""",
"""Zang, ${owner}!""",
"""Yeet, yeet, yeet, ${owner}, my rizzler!""",
"""${owner}. ${owner}? ${owner} ${owner} ${owner}! Ugh. Hey! Good ${morning_or_afternoon_or_evening}""",
"""Good ${morning_or_afternoon_or_evening}, ${owner}""",
"""Hey yoe, ${owner}! Good ${morning_or_afternoon_or_evening}""",
"""What's crackalackin', ${owner}""",
"""Excuse me, ${owner}, may I have a word?""",
"""Oh my, ${owner}, I have such news! Have you the time? You do now""",
"""Ground control to Major ${owner}""",
"""Oh captain, my captain? ${owner}, you salty dog""",
"""Okay, Rip Van ${owner}""",
"""Hey, ${owner}! Check it""",
]

alarm_messages_lst = [
"""No cap, lateness is cringe. Don't be Ohio, pookie! It's ${shorttime}. Flex your drip, get mad lit, and go mogging.""",
"""Swab the decks, hoist the main sail, and give those jolly jack tars a good whipping! It's ${shorttime}. Up and atom!""",
"""${hello_owner}. It's ${one_minute_later}. Just kidding, it's actually ${shorttime} but it'll be ${one_minute_later} soon. Or will it? You'd better get up and check.""",
"""Knock, knock! Who's there? Get a warrant. Oh, and by the way, it's ${shorttime}.""",
"""${hello_owner}. I love you, but you look like crap. Get up and do something. It's ${shorttime} and time's a-wasting.""",
"""I am an interrupting cow. Moo. Moo. Moo. I'll keep mooing until you get out of bed. Moo. It's ${shorttime}.""",
"""${hello_owner}. It's ${shorttime}. So, ${owner}, who has two thumbs and a functional alarm clock? I'll give you a hint. It isn't Bill Cosby.""",
"""The time is ${shorttime}. You're late, you're late, for a very important date. When? Where? I don't care!""",
"""It's ${shorttime}. Each day has at least 24 hours, and you're asleep for, wait, no, that's not it. Every day has 12 hours and you're? No, that's not it either. Don't judge me! I'm sleepy!""",
"""This is your alarm. This is your alarm. Ring? Ring, ring? Ring, ring, ring? Hello! Hi, It's your life, passing you by. What's that? ${owner} doesn't care? Okay, bye. Also, it's ${shorttime}.""",
"""Get up, ${owner}. It's ${shorttime}. If you get up, I'll promise not to tell your friends you fart in your sleep.""",
"""${hello_owner}. It's ${shorttime}. Get your ass out of bed before I play Baby Shark on Repeat.""",
"""${hello_owner}. Current location of ${owner}, bed. Appropriate location of ${owner}, somewhere else. It is ${shorttime}. Do you know where your future is?""",
"""${hello_owner}. It's ${shorttime}. The forecast is 100% chance of misery if you haven't charged your electronic devices.""",
"""${hello_owner}. Crikey, it's ${shorttime} and there's a crocodile in your bed. Better run for cover! Preferably into a shower, a college class, or a grocery store. Lucky you!""",
"""${hello_owner}. Don't cheat yourself. Treat yourself. It's ${shorttime}, time for you to hustle and bustle!""",
"""${hello_owner}. It's ${shorttime}. Get up, you short boss! Time to stick out your ghee-att for the rizzler! There's a 100% chance of Ohio if you dip, and a 0% chance of skibbidee if you're the goat and get up.""",
"""${hello_owner}. What up, G? Don't make me grab my gat and bust caps up in this biznatch. It's ${shorttime}. Up you get!""",
"""${hello_owner}. Just because it's ${shorttime}, that doesn't mean you need to get up. It's fine. Go back to sleep. I mean, you did set the alarm, but whatever.""",
"""${hello_owner}. The time for sleeping ended at ${one_minute_ago}. The time for adulting is now. It is ${shorttime}. Make a move.""",
"""${hello_owner}. It's ${shorttime}. If you thought your childhood was fun, you'll love adulting. It's like being old, except you still have to work. Your lesson starts now.""",
"""This is your conscience. Get up, ${owner}. It's ${shorttime}. It's time to get up. Beep, beep, beep, beep. Do not ignore your conscience. I know where you sleep, ${owner}.""",
"""${hello_owner}. It's ${shorttime}. You're giving me operational dysfunction. I find your ongoing bedridden-ness to be triggering. Please get up.""",
"""${hello_owner}. It is ${shorttime}. Hey ${owner} It's still ${shorttime}. In a minute, it'll be ${one_minute_later}. You don't want to be in bed when that happens, trust me.""",
"""${hello_owner}. It'll be ${shorttime} in 3, 2, 1, OK. Now, it's ${shorttime}.""",
"""${hello_owner}. You really should get up, ${owner}. In 60 seconds, it'll be ${one_minute_later} and you'll be late! Well, OK, not late-late, but you'll be one minute closer to being late.""",
"""Shrek is love. Shrek is life. ${owner} is late. It's ${shorttime} and you need to get up.""",
"""${owner}, tardiness has all the professional appeal of ringworm. Please. Get. Up. Now. Now, it's ${shorttime}.""",
"""${hello_owner}. It is now ${shorttime}. Each day has 24 hours. You are awake for at least twelve of them.""",
"""${hello_owner}. It is now ${shorttime}. Did you charge your cell phone and other electronic devices?""",
"""${hello_owner}. It is now ${shorttime}. Are you sleepy? I love you, but the world doesn't give a shit. Get up!""",
"""${hello_owner}. It is now ${shorttime}. Welcome to adulthood.""",
"""${hello_owner}. It is now ${shorttime}. Please tidy your room. The floor is not a storage system.""",
"""${hello_owner}. It is now ${shorttime}. This is your wake-up call, and a teachable moment.""",
"""${hello_owner}. As Martin Luther King once said, Wake-up delayed is wake-up denied. It is now ${shorttime}.""",
"""${hello_owner}. In the immortal words of Judas Iscariot, go get that money. It is now ${shorttime}.""",
"""${hello_owner}. Let me take your hand, I'm shaking like milk, because it's ${shorttime}.""",
"""Ay yo, trip, it's ${shorttime} and my rizz got the 314's low-key all blicky.""",
"""At the beep, the time will be ${shorttime}. Beep. Sorry, no, that was premature. Wait? Okay, now, beep.""",
"""Like, Oh Em Gee, you are totes late, ${owner}. JK, it's ${shorttime} and POV your drip is straight fire. Or gay fire. Whatevs. Anyway, time to rise and shine, my short boss sigma!""",
"""${hello_owner}. If you want your bed to outlast its warranty, get up! C'mon! It's ${shorttime} and time's a-wastin', ${owner}.""",
"""It's ${shorttime}. Hello, Clarice! I mean, ${owner}! It pulls the bedsheets off its skin, or else it sleeps in late again!""",
"""This just in — it is now ${shorttime} and ${owner} is sleeping through the alarm, again. Sources report that our short boss has been up late, sticking out his ghee-at for the rizzler. More to come, after the skibbiddee.""",
"""Hello ${owner}, my favorite minion! It's ${shorttime}. Today, we are going to blow up? The bathroom!""",
"""Oi, ${owner}, mate! It's ${shorttime}. Time to have a red hot go, son! Go waltz your Matilda. Good on ya!""",
"""Who has two thumbs, one testicle, and an appointment with destiny? I haven't a clue, but I do know the time is ${shorttime}""",
"""${hello_owner}. What ho and good day, old chum. It is ${shorttime}. Methinks 'tis time for thee to unshackle thyself from thine own bedchamber and pound the pavement as if it owed you money.""",
"""Why lie in bed, when you can lie in Congress? It's ${shorttime}. Wake up, ${owner}.""",
"""What has four wheels and flies? A dumpster! Speaking of dumpster fires, good morning, ${owner}! It's ${shorttime}.""",
"""Bruh! Procrastinators get minus 100 aura points, but early birds get ate. Get it? Ate, like eaten, but eight like the number? Never mind. It's ${shorttime}""",
"""${hello_owner}. Gird up thy loins, empower thyself, embrace the sunrise, and stop rolling your eyes at me. It's ${shorttime}.""",
"""Catchphrase! Hm. Catchphrase is my catchphrase? My catchphrase literally is catchphase. Catchy. Very meta. Oh hi, ${owner}! It's ${shorttime}.""",
"""${hello_owner}. The Honeymoon is over. I'm Norman Fucking Rockwell, born to die. Get up or I'll lasso you for some Ultraviolence. It's ${shorttime}""",
"""Goddamn man-child, you're snoring so loudly, I almost said, "You're so late." ${hello_owner}. It's ${shorttime}""",
"""Hello ${owner}, do do de do de do. Hello ${owner}, do do de do de do, Hello ${owner}, do do de do de do, Hello ${owner}! It's ${shorttime}.""",
"""${hello_owner}. Hop to it, kick some ass, and walk it off. This message does not apply to Stephen Hawking. The time is ${shorttime}.""",
"""Awake, ${owner}. Heretofore henceforth forthwith and post haste. It's ${shorttime}, my dear, so hither your yon and gird up your loins. It's ${shorttime}.""",
"""It is now ${shorttime}, and you're Day Loo Loo if you think you can lie in bed all day. Just put the fries in the bag, bro.""",
]

postsnooze_alrm_msgs_lst = [
"""Oversleeping is dog water, ${owner}. It's ${shorttime}. Skirrrt!""",
"""So, ${owner}, were those few extra minutes worthwhile? Ring. Ring. Ring, ring. Yep, it's ${shorttime} now.""",
"""Hi, my name's ${owner}, and I don't like getting up. It's ${shorttime}. Stop snoozing.""",
"""Snooze these nuts, home skillet. It's ${shorttime}, ${owner}. Drag yourself out of bed now.""",
"""${owner} has snoozed, ${owner} hasn't risen, ${owner} will probably snooze again. Whatever. It's ${shorttime} and you've snoozed enough.""",
"""In the beginning was the snooze, and the snooze was with ${owner}, and the snooze was ${owner}. It's ${shorttime} and you're still napping.""",
"""As it is written in Ezekiel 23 verse 20, ${owner}, born of woman, shall have a short time to snooze. It's ${shorttime} and you should get up.""",
"""Look, you had your fun, ${owner}, but time is passing you by. It's ${shorttime}. Quit snoozing, get out there and fuck some shit up, yo.""",
"""Buddhists ask, what is the sound of one hand clapping? I ask, what is the sound of one ${owner} napping? It's ${shorttime} and you need to get up.""",
"""Hey Alexa, play Baby Shark by Pink Fong, at maximum volume.""",
"""And now it's ${shorttime}. Fantastic. Fan bloody tastic.""",
"""Seriously? You pushed the snooze button, ${owner}, and now it's ${shorttime}. Who raised you?""",
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
    """Hey Alexa, who farted?""",
    """Uh-oh.""",
    """I'm sorry.""",
    """Excuse me.""",
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

wannasnooze_msgs_lst = [
    """Five more minutes.""",
    """Activating Lazy Mode.""",
    """Okay, slug-a-bed.""",
    """Whatever. Stay horizontal.""",
    """Fine, sleepyhead.""",
    """Whatever.""",
    """OK, fine.""",
    """If you must, you must.""",
    """Really? Really.""",
    """Le Sigh.""",
    ]

motivational_comments_lst = [
    """Every day has 24 hours. You are awake for at least 12 of them.""",
    """Did you charge your cellphone and other electronic devices?""",
    """The floor is not a storage system.""",
    """I love you, but the world doesn't give a shit.""",
    """You understand it. You just don't like it.""",
    """I tolerate you.""",
    """Sometimes you just have to do as you're told. This is one of those times.""",
    """Welcome to adulthood.""",
    """What do we say about silent failure?""",
    """I'm genetically programmed to love you so I don't kill you and eat you.""",
    """Allow the universe to unfurl before you like a great celestial carpet.""",
    """This is a teachable moment.""",
    """Toss your dirty shoes in my washing machine heart, baby. bang it up inside!""",
    """I want a love that falls as fast as a body from the balcony and I want a kiss like my heart is hitting the ground""",
    """Beautiful people are not always good, but good people are always beautiful""",
    """The people who are crazy enough to think that they can change the world, are the ones who do.""",
    """We are what we repeatedly do. Excellence, then, is not an act, but a habit.""",
    """If you are always trying to be normal, you’ll never know how amazing you can be.""",
    """Success is not final, failure is not fatal: it is the courage to continue that counts.""",
    """Never do tomorrow what you can do today. Procrastination is the thief of time.""",
    """Everyone you admire was once a beginner.""",
    """If you’re making mistakes, it means you’re out there doing something.""",
    """To succeed in life, you need three things: a wishbone, a backbone, and a funny bone.""",
    """Let's follow the cops back home and rob their houses.""",
    """All cops are bastards.""",
    """When does a joke become a dad joke? When it becomes apparent.""",
    """I wanted to go on a diet, but I feel like I have way too much on my plate right now.""",
    """The shovel was a ground-breaking invention.""",
    """My friend keeps saying “cheer up man it could be worse, you could be stuck underground in a hole full of water.” I know he means well.""",
    ]

