"""Massive database of bestseller merch phrase patterns.

These patterns are based on proven bestselling merch designs across
Amazon Merch, Redbubble, TeePublic, and other POD platforms.
"""

# Core pattern templates - {X} is the variable (activity/topic/noun)
# Each pattern has been proven to sell well across multiple niches

BESTSELLER_TEMPLATES = [
    # === THERAPY/ESCAPE PATTERNS ===
    "{X} is my therapy",
    "{X} is cheaper than therapy",
    "I don't need therapy I need {X}",
    "My therapist says I need more {X}",
    "{X} is the best therapy",
    "Who needs therapy when you have {X}",

    # === PREFERENCE/PRIORITY PATTERNS ===
    "I'd rather be {X}",
    "{X} over everything",
    "Less adulting more {X}",
    "All I need is {X}",
    "Just here for the {X}",
    "You had me at {X}",
    "{X} first everything else later",
    "Will cancel plans for {X}",
    "Zero percent chance I'm missing {X}",

    # === IDENTITY/DESTINY PATTERNS ===
    "Born to {X}",
    "Made to {X}",
    "Built for {X}",
    "Living for {X}",
    "Just a girl who loves {X}",
    "Just a boy who loves {X}",
    "Just a guy who loves {X}",
    "Professional {X}",
    "{X} is my personality",
    "Fluent in {X}",
    "Certified {X} addict",
    "{X} is in my DNA",

    # === POWERED BY/FUELED BY PATTERNS ===
    "Powered by {X}",
    "Fueled by {X}",
    "Running on {X}",
    "Runs on {X} and bad decisions",
    "Runs on {X} and sarcasm",
    "{X} is my fuel",
    "Operating on {X} and anxiety",
    "{X} loading please wait",
    "Low on {X}",
    "Need more {X}",

    # === ROUTINE PATTERNS ===
    "Eat sleep {X} repeat",
    "Wake pray {X}",
    "Coffee {X} sleep repeat",
    "Rise and {X}",
    "First {X} then everything else",
    "Sorry can't I have {X}",
    "On my {X} grind",
    "Currently in my {X} era",

    # === LOVE/OBSESSION PATTERNS ===
    "I love {X}",
    "Obsessed with {X}",
    "{X} is my love language",
    "My heart belongs to {X}",
    "{X} has my whole heart",
    "Hopelessly devoted to {X}",
    "Head over heels for {X}",
    "Can't live without {X}",
    "{X} is life",
    "In love with {X}",
    "Here for the {X}",

    # === MOM/DAD PATTERNS ===
    "{X} mom",
    "{X} mama",
    "Proud {X} mom",
    "{X} mom life",
    "Living that {X} mom life",
    "Best {X} mom ever",
    "{X} dad",
    "Proud {X} dad",
    "{X} dad life",
    "World's okayest {X} dad",
    "{X} parent",
    "Raising {X} kids",

    # === HUMOR/SARCASM PATTERNS ===
    "Will work for {X}",
    "Probably thinking about {X}",
    "My brain is 90% {X}",
    "If lost return to {X}",
    "Professional {X} overthinker",
    "Doing {X} things",
    "It's a {X} thing",
    "Hold my {X}",
    "But first {X}",
    "Plot twist {X}",
    "Tell me you love {X} without telling me",
    "This is my {X} shirt",
    "{X} mode activated",
    "Warning may talk about {X}",
    "Sorry I'm late I was {X}",
    "I'm not lazy I'm on {X} mode",
    "Easily distracted by {X}",
    "My {X} brings all the boys to the yard",
    "I paused my {X} to be here",

    # === EXPERT/MASTER PATTERNS ===
    "{X} whisperer",
    "{X} master",
    "{X} king",
    "{X} queen",
    "{X} legend",
    "{X} expert",
    "{X} enthusiast",
    "{X} specialist",
    "Fear the {X}",
    "Respect the {X}",
    "Trust me I'm a {X} person",

    # === COMPARISON PATTERNS ===
    "Less drama more {X}",
    "Less talk more {X}",
    "More {X} less problems",
    "{X} vibes only",
    "Choose {X}",
    "{X} not chaos",
    "Peace love {X}",
    "Happiness is {X}",
    "Life is better with {X}",
    "Keep calm and {X}",

    # === VINTAGE/RETRO PATTERNS ===
    "Vintage {X}",
    "Old school {X}",
    "Classic {X}",
    "Retro {X}",
    "Original {X}",
    "Authentic {X}",
    "Est 19XX {X}",
    "Since forever {X}",

    # === TEAM/GROUP PATTERNS ===
    "Team {X}",
    "{X} squad",
    "{X} crew",
    "{X} gang",
    "{X} club",
    "{X} tribe",
    "Part of the {X} club",

    # === WEATHER/TIME PATTERNS ===
    "{X} weather",
    "{X} season",
    "Always {X} time",
    "'Tis the season for {X}",
    "{X} szn",
    "{X} o'clock somewhere",
    "{X} time is the best time",

    # === SIZE/INTENSITY PATTERNS ===
    "Big {X} energy",
    "Major {X} vibes",
    "100% {X}",
    "Extra {X}",
    "Maximum {X}",
    "Full time {X}",
    "Part time {X}",
    "Professional {X} amateur {X}",
    "Serious {X}",

    # === LOCATION/WHERE PATTERNS ===
    "{X} is my happy place",
    "Take me to {X}",
    "Home is where the {X} is",
    "I left my heart in {X}",
    "Rather be at {X}",
    "{X} calling and I must go",
    "The mountains are calling for {X}",

    # === AGE/TIME PATTERNS ===
    "Retired {X} expert",
    "Been {X} since birth",
    "Old enough to know better still {X}",
    "Age is just a number {X}",
    "Getting better at {X}",
    "Still learning to {X}",
    "Never too old for {X}",
    "Too young to give up on {X}",

    # === WEEKEND/PLANS PATTERNS ===
    "Weekend forecast {X}",
    "Plans tonight {X}",
    "My weekend looks like {X}",
    "Weekends are for {X}",
    "Friday night {X}",
    "Saturday morning {X}",
    "Sunday {X}",

    # === EMOTION/MOOD PATTERNS ===
    "{X} makes me happy",
    "{X} is my mood",
    "{X} state of mind",
    "Feeling {X}",
    "{X} therapy",
    "Mentally I'm {X}",
    "In my {X} feels",

    # === SIMPLE STATEMENT PATTERNS ===
    "I {X}",
    "We {X}",
    "Let's {X}",
    "Just {X}",
    "Stay {X}",
    "Go {X}",
    "Get {X}",
    "Live {X}",
    "Be {X}",
]

# Topics and activities to combine with patterns
TRENDING_TOPICS = [
    # Outdoor/Adventure
    "hiking", "fishing", "camping", "hunting", "kayaking", "climbing",
    "backpacking", "trail running", "mountain biking", "skiing", "snowboarding",
    "surfing", "paddle boarding", "rock climbing", "off roading",

    # Fitness
    "gym", "lifting", "running", "yoga", "crossfit", "weightlifting",
    "marathon", "swimming", "cycling", "working out", "gains",

    # Hobbies
    "gaming", "reading", "cooking", "baking", "gardening", "crafting",
    "painting", "photography", "knitting", "crocheting", "woodworking",
    "pottery", "sewing", "DIY", "collecting", "bird watching",

    # Beverages
    "coffee", "wine", "beer", "tea", "whiskey", "bourbon", "cocktails",
    "espresso", "cold brew", "mimosas", "margaritas",

    # Pets
    "dogs", "cats", "horses", "chickens", "goats", "bees",
    "aquarium", "reptiles", "birds",

    # Jobs/Professions
    "nurse", "teacher", "mechanic", "welder", "trucker", "farmer",
    "carpenter", "electrician", "plumber", "firefighter", "EMT",
    "dispatcher", "server", "bartender", "chef", "hairstylist",

    # Music
    "guitar", "drums", "piano", "bass", "vinyl", "concerts",
    "metal", "country", "rock", "jazz", "blues",

    # Sports
    "baseball", "football", "basketball", "hockey", "golf", "tennis",
    "soccer", "volleyball", "softball", "wrestling", "boxing",

    # Food
    "tacos", "pizza", "bacon", "sushi", "BBQ", "burgers", "steak",
    "ramen", "chocolate", "cheese", "carbs",

    # Lifestyle
    "naps", "sleep", "silence", "alone time", "books", "plants",
    "true crime", "podcasts", "Netflix", "snacks",

    # Moods/Traits
    "sarcasm", "introvert", "overthinking", "anxiety", "chaos",
    "drama", "petty", "savage", "awkward", "weird",
]

# Classic bestsellers - specific phrases that have sold millions
CLASSIC_BESTSELLERS = [
    # Coffee phrases
    "But first coffee",
    "Mama needs coffee",
    "Coffee then adulting",
    "Powered by caffeine and chaos",
    "I run on coffee and cuss words",
    "Coffee because adulting is hard",
    "Don't talk to me until I've had my coffee",
    "Fueled by iced coffee and anxiety",
    "Espresso yourself",
    "Death before decaf",

    # Mom/parenting phrases
    "Mama bear",
    "Tired as a mother",
    "Mom life best life",
    "Hot mess mom",
    "Boy mom",
    "Girl mom",
    "Plant mom",
    "Dog mom",
    "Cat mom",
    "Mom of boys",
    "Raising tiny humans",
    "Motherhood the hustle is real",

    # Dad phrases
    "Dad jokes loading",
    "Best dad ever",
    "Dad bod in progress",
    "Dadlife",
    "Father of dragons",
    "Fatherhood no sleep club",

    # Fitness/gym phrases
    "Gym hair don't care",
    "Strong not skinny",
    "Lift heavy pet dogs",
    "Squat like nobody's watching",
    "Will squat for tacos",
    "Gains all day",
    "Beast mode activated",
    "No days off",
    "Train insane or remain the same",

    # Humor phrases
    "I'm not lazy I'm on energy saving mode",
    "Adulting is hard",
    "Can't adult today",
    "I have no idea what I'm doing",
    "I'm not arguing I'm explaining why I'm right",
    "Not today Satan",
    "Zero fox given",
    "Sorry not sorry",
    "Sarcasm is my love language",
    "Chaos coordinator",
    "Professional overthinker",
    "Fluent in sarcasm",

    # Introvert phrases
    "Introverted but willing to discuss plants",
    "Sorry I'm late I didn't want to come",
    "Cancel plans and watch true crime",
    "Home is my happy place",
    "People exhaust me",
    "Leave me alone I'm reading",

    # Pet phrases
    "My kids have paws",
    "All I need is dogs",
    "Sorry I can't my dog said no",
    "Home is where my dog is",
    "Anti social dog mom club",
    "In a relationship with my cat",
    "Crazy cat lady",
    "Dog hair is my glitter",

    # Outdoor phrases
    "The mountains are calling",
    "Adventure awaits",
    "Happy camper",
    "Take me to the mountains",
    "Lake life",
    "River rat",
    "Beach please",
    "Salt water heals everything",
    "Forest bathing",
    "Into the wild",

    # Profession phrases
    "Nurse fuel",
    "Teacher by day wine mom by night",
    "Nursing is a work of heart",
    "Truckin ain't easy",
    "Diesel therapy",
    "Welder by trade",
    "Blue collar proud",
    "Farming is life",

    # Seasonal
    "Fall vibes only",
    "Sweater weather",
    "Pumpkin everything",
    "Tis the season to be cozy",
    "Summer state of mind",
    "Beach bum",
    "Flip flop season",

    # Age/retirement
    "Retired and loving it",
    "Not old just vintage",
    "Classic not old",
    "Aged to perfection",
    "Over the hill and picking up speed",
    "Old enough to know better",
]

# Niche-specific bestsellers
NICHE_BESTSELLERS = {
    "fishing": [
        "Gone fishing be back never",
        "Hooked on fishing",
        "Reel cool dad",
        "Born to fish forced to work",
        "Fishing is calling",
        "Tight lines",
        "Fish fear me women want me",
        "I fish therefore I am",
        "A bad day fishing beats a good day at work",
        "Fishing legend",
        "Master baiter",
        "Bass hunter",
        "Catch and release",
        "Living the reel life",
        "Weekend hooker",
    ],
    "hunting": [
        "Bow hunter",
        "Deer hunter",
        "Duck hunter",
        "Hunt eat sleep repeat",
        "Born to hunt",
        "If it flies it dies",
        "Buck commander",
        "Trophy hunter",
        "Hunting widow",
        "Hunting season loading",
    ],
    "nursing": [
        "Nurse life",
        "Night shift warrior",
        "Nursing is my cardio",
        "Coffee scrubs and rubber gloves",
        "Cute enough to stop your heart skilled enough to restart it",
        "Have no fear the nurse is here",
        "Nurses call the shots",
        "Nurse mode on",
        "Off duty nurse",
        "Powered by coffee and compassion",
    ],
    "teaching": [
        "Teacher mode",
        "Teaching is my superpower",
        "Teacher off duty",
        "Teach love inspire",
        "The influence of a good teacher",
        "Teaching tiny humans",
        "Caffeinated and educated",
        "Teacher life",
        "Future teacher",
        "100 days smarter",
    ],
    "coffee": [
        "Espresso yourself",
        "Death before decaf",
        "Livin la vida mocha",
        "You mocha me crazy",
        "Coffee is always a good idea",
        "Life begins after coffee",
        "Coffee then chaos",
        "Powered by plants and coffee",
        "Coffee addict",
        "Cold brew crew",
    ],
    "dogs": [
        "Dog mom life",
        "Who rescued who",
        "Life is better with a dog",
        "Dogs over people",
        "My therapist has four legs",
        "Home is where my dog is",
        "Dog hair dont care",
        "Pawsitively obsessed",
        "Dog dad",
        "Crazy dog lady",
    ],
    "cats": [
        "Cat mom",
        "Crazy cat lady",
        "Cat dad",
        "Pawsitively purrfect",
        "Home is where my cat is",
        "Cat hair dont care",
        "I was normal three cats ago",
        "All you need is love and a cat",
        "Not all heroes wear capes some just adopt cats",
        "Professional cat herder",
    ],
    "gaming": [
        "Game over",
        "Level up",
        "Player one ready",
        "Gamer dad",
        "Gamer mom",
        "Eat sleep game repeat",
        "I paused my game to be here",
        "One more game",
        "Achievement unlocked",
        "Respawn in progress",
    ],
    "fitness": [
        "No pain no gain",
        "Train like a beast",
        "Lift heavy",
        "Gym is my therapy",
        "Muscles in progress",
        "Sweat is fat crying",
        "Strong is the new pretty",
        "Getting ripped",
        "Iron therapy",
        "Gym rat",
    ],
    "camping": [
        "Happy camper",
        "Camping is my therapy",
        "Life is better around the campfire",
        "Home is where you pitch it",
        "Take me camping",
        "Camp more worry less",
        "Adventure awaits",
        "Campfire and chill",
        "Tent life",
        "Glamping queen",
    ],
    "beer": [
        "Hold my beer",
        "Beer me",
        "Craft beer snob",
        "In dog beers I've only had one",
        "Beer is proof that god loves us",
        "Save water drink beer",
        "Beer thirty",
        "IPA lot when I drink",
        "Hoppy hour",
        "Beer makes me hoppy",
    ],
    "wine": [
        "Wine time",
        "Wine not",
        "You had me at merlot",
        "Wine is my valentine",
        "Partners in wine",
        "Will give medical advice for wine",
        "Wines well with others",
        "Wine down",
        "Rosé all day",
        "Sip happens",
    ],
}

# Word variations for generating new combinations
WORD_VARIATIONS = {
    "love": ["adore", "obsessed with", "living for", "can't get enough of"],
    "need": ["require", "must have", "can't live without", "gotta have"],
    "hate": ["can't stand", "over", "done with", "avoiding"],
    "happy": ["blessed", "grateful", "living my best life", "thriving"],
    "tired": ["exhausted", "running on empty", "barely functioning", "done"],
    "coffee": ["caffeine", "espresso", "cold brew", "joe", "brew"],
    "dog": ["pupper", "doggo", "good boy", "fur baby", "pup"],
    "cat": ["kitty", "floof", "furball", "feline", "meow"],
    "weekend": ["Saturday", "Sunday", "time off", "days off"],
    "work": ["job", "grind", "hustle", "9 to 5", "adulting"],
}

def get_all_bestseller_phrases():
    """Get combined list of all bestseller phrases."""
    phrases = list(CLASSIC_BESTSELLERS)
    for niche_phrases in NICHE_BESTSELLERS.values():
        phrases.extend(niche_phrases)
    return phrases

def get_all_templates():
    """Get all template patterns."""
    return BESTSELLER_TEMPLATES

def get_all_topics():
    """Get all trending topics."""
    return TRENDING_TOPICS

def get_niche_bestsellers(niche: str):
    """Get bestsellers for a specific niche."""
    return NICHE_BESTSELLERS.get(niche.lower(), [])
