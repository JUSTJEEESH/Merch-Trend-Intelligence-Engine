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

# Comprehensive niche data with keywords, competition levels, and topics
# Competition: low (undersaturated), medium (balanced), high (saturated)
NICHE_DATA = {
    # === BEVERAGES ===
    "coffee": {
        "topics": ["coffee", "espresso", "caffeine", "cold brew", "latte", "mocha", "cappuccino", "brew", "barista"],
        "competition": "high",
        "avg_bsr": 15000,
    },
    "tea": {
        "topics": ["tea", "chai", "matcha", "herbal tea", "green tea", "tea lover", "tea time", "steep"],
        "competition": "medium",
        "avg_bsr": 45000,
    },
    "beer": {
        "topics": ["beer", "craft beer", "IPA", "hops", "brewing", "brews", "lager", "ale", "stout", "pilsner"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "wine": {
        "topics": ["wine", "vino", "rosé", "merlot", "cabernet", "sommelier", "wine lover", "red wine", "white wine"],
        "competition": "medium",
        "avg_bsr": 40000,
    },
    "whiskey": {
        "topics": ["whiskey", "bourbon", "scotch", "rye", "whisky", "single malt", "neat", "on the rocks"],
        "competition": "low",
        "avg_bsr": 75000,
    },
    "cocktails": {
        "topics": ["cocktails", "mixology", "bartender", "margarita", "mojito", "martini", "happy hour"],
        "competition": "low",
        "avg_bsr": 85000,
    },

    # === FITNESS ===
    "fitness": {
        "topics": ["gym", "workout", "gains", "lifting", "fit", "exercise", "train", "muscles", "sweat"],
        "competition": "high",
        "avg_bsr": 12000,
    },
    "yoga": {
        "topics": ["yoga", "namaste", "zen", "meditation", "mindfulness", "stretch", "flow", "breathe", "asana"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "running": {
        "topics": ["running", "marathon", "5K", "10K", "runner", "jogging", "track", "pace", "miles"],
        "competition": "medium",
        "avg_bsr": 32000,
    },
    "crossfit": {
        "topics": ["crossfit", "WOD", "box", "AMRAP", "burpees", "kettlebell", "snatch", "clean and jerk"],
        "competition": "low",
        "avg_bsr": 65000,
    },
    "weightlifting": {
        "topics": ["weightlifting", "powerlifting", "deadlift", "squat", "bench", "barbell", "plates", "PR"],
        "competition": "medium",
        "avg_bsr": 42000,
    },
    "bodybuilding": {
        "topics": ["bodybuilding", "physique", "bulk", "cut", "shred", "pump", "gains", "reps"],
        "competition": "medium",
        "avg_bsr": 38000,
    },
    "swimming": {
        "topics": ["swimming", "swim", "pool", "laps", "freestyle", "butterfly", "backstroke", "swimmer"],
        "competition": "low",
        "avg_bsr": 72000,
    },
    "cycling": {
        "topics": ["cycling", "bike", "bicycle", "cyclist", "peloton", "ride", "pedal", "tour"],
        "competition": "medium",
        "avg_bsr": 48000,
    },
    "pilates": {
        "topics": ["pilates", "core", "reformer", "barre", "stretch", "tone", "strengthen"],
        "competition": "low",
        "avg_bsr": 82000,
    },

    # === SPORTS ===
    "golf": {
        "topics": ["golf", "golfer", "tee", "fairway", "birdie", "bogey", "par", "putt", "green", "caddy"],
        "competition": "medium",
        "avg_bsr": 25000,
    },
    "baseball": {
        "topics": ["baseball", "softball", "bat", "diamond", "pitch", "home run", "strikeout", "dugout"],
        "competition": "medium",
        "avg_bsr": 30000,
    },
    "football": {
        "topics": ["football", "touchdown", "gridiron", "quarterback", "tackle", "end zone", "pigskin"],
        "competition": "high",
        "avg_bsr": 18000,
    },
    "basketball": {
        "topics": ["basketball", "hoops", "court", "dunk", "three pointer", "rebound", "fast break"],
        "competition": "high",
        "avg_bsr": 20000,
    },
    "hockey": {
        "topics": ["hockey", "puck", "ice", "rink", "slap shot", "goalie", "hat trick", "zamboni"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "soccer": {
        "topics": ["soccer", "football", "goal", "pitch", "striker", "keeper", "penalty", "match"],
        "competition": "medium",
        "avg_bsr": 33000,
    },
    "tennis": {
        "topics": ["tennis", "racket", "court", "serve", "volley", "ace", "match point", "love"],
        "competition": "low",
        "avg_bsr": 68000,
    },
    "volleyball": {
        "topics": ["volleyball", "spike", "dig", "set", "serve", "net", "beach", "bump"],
        "competition": "low",
        "avg_bsr": 75000,
    },
    "wrestling": {
        "topics": ["wrestling", "mat", "pin", "takedown", "grapple", "singlet", "coach"],
        "competition": "low",
        "avg_bsr": 88000,
    },
    "boxing": {
        "topics": ["boxing", "gloves", "ring", "knockout", "jab", "uppercut", "heavyweight", "rounds"],
        "competition": "medium",
        "avg_bsr": 45000,
    },
    "mma": {
        "topics": ["MMA", "UFC", "jiu jitsu", "octagon", "submission", "tap out", "ground and pound"],
        "competition": "medium",
        "avg_bsr": 42000,
    },
    "pickleball": {
        "topics": ["pickleball", "paddle", "dink", "kitchen", "volley", "court", "pickle"],
        "competition": "low",
        "avg_bsr": 55000,
    },

    # === OUTDOOR ACTIVITIES ===
    "hiking": {
        "topics": ["hiking", "trails", "mountains", "summit", "trek", "backpacking", "outdoors", "nature"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "camping": {
        "topics": ["camping", "campfire", "tent", "wilderness", "s'mores", "stargazing", "camp"],
        "competition": "medium",
        "avg_bsr": 32000,
    },
    "fishing": {
        "topics": ["fishing", "bass", "trout", "casting", "reeling", "tackle", "angler", "reel", "bait", "lure"],
        "competition": "medium",
        "avg_bsr": 22000,
    },
    "hunting": {
        "topics": ["hunting", "deer", "duck", "bow", "rifle", "game", "trophy", "hunter", "season"],
        "competition": "medium",
        "avg_bsr": 25000,
    },
    "kayaking": {
        "topics": ["kayaking", "kayak", "paddle", "rapids", "river", "whitewater", "sea kayak"],
        "competition": "low",
        "avg_bsr": 78000,
    },
    "skiing": {
        "topics": ["skiing", "ski", "slopes", "powder", "moguls", "chairlift", "après-ski", "black diamond"],
        "competition": "medium",
        "avg_bsr": 45000,
    },
    "snowboarding": {
        "topics": ["snowboarding", "shred", "halfpipe", "powder", "terrain park", "carve"],
        "competition": "low",
        "avg_bsr": 65000,
    },
    "surfing": {
        "topics": ["surfing", "waves", "surf", "barrel", "swell", "board", "beach", "ocean"],
        "competition": "medium",
        "avg_bsr": 38000,
    },
    "climbing": {
        "topics": ["climbing", "rock climbing", "bouldering", "belay", "crag", "summit", "send"],
        "competition": "low",
        "avg_bsr": 72000,
    },
    "boating": {
        "topics": ["boating", "boat", "yacht", "sailing", "marina", "captain", "anchor", "nautical"],
        "competition": "low",
        "avg_bsr": 68000,
    },
    "rv": {
        "topics": ["RV", "RVing", "camper", "motorhome", "road trip", "campground", "nomad"],
        "competition": "low",
        "avg_bsr": 58000,
    },
    "offroading": {
        "topics": ["offroading", "4x4", "jeep", "mud", "trail", "crawl", "overland"],
        "competition": "low",
        "avg_bsr": 62000,
    },

    # === PETS ===
    "dogs": {
        "topics": ["dogs", "puppy", "fur baby", "good boy", "doggo", "pupper", "woof", "paws", "fetch"],
        "competition": "high",
        "avg_bsr": 8000,
    },
    "cats": {
        "topics": ["cats", "kitten", "meow", "feline", "kitty", "purr", "whiskers", "paws"],
        "competition": "high",
        "avg_bsr": 10000,
    },
    "horses": {
        "topics": ["horses", "equestrian", "riding", "stable", "mare", "stallion", "gallop", "trot"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "chickens": {
        "topics": ["chickens", "hens", "roosters", "coop", "eggs", "poultry", "flock", "backyard chickens"],
        "competition": "low",
        "avg_bsr": 52000,
    },
    "goats": {
        "topics": ["goats", "farm", "herd", "kids", "billy", "nanny", "goat life"],
        "competition": "low",
        "avg_bsr": 65000,
    },
    "bees": {
        "topics": ["bees", "beekeeping", "honey", "hive", "apiary", "beekeeper", "pollinator"],
        "competition": "low",
        "avg_bsr": 72000,
    },
    "birds": {
        "topics": ["birds", "parrots", "parakeet", "feathers", "aviary", "birder", "finch"],
        "competition": "low",
        "avg_bsr": 78000,
    },
    "reptiles": {
        "topics": ["reptiles", "snakes", "lizards", "gecko", "bearded dragon", "scales"],
        "competition": "low",
        "avg_bsr": 85000,
    },
    "rabbits": {
        "topics": ["rabbits", "bunny", "hop", "hutch", "fluffy", "ears", "carrot"],
        "competition": "low",
        "avg_bsr": 68000,
    },
    "aquarium": {
        "topics": ["aquarium", "fish", "tropical fish", "reef", "tank", "aquarist", "saltwater"],
        "competition": "low",
        "avg_bsr": 75000,
    },

    # === PROFESSIONS ===
    "nursing": {
        "topics": ["nursing", "nurse", "RN", "scrubs", "hospital", "patient care", "night shift", "healthcare"],
        "competition": "high",
        "avg_bsr": 12000,
    },
    "teaching": {
        "topics": ["teaching", "teacher", "classroom", "students", "education", "school", "lesson", "grade"],
        "competition": "high",
        "avg_bsr": 14000,
    },
    "trucking": {
        "topics": ["trucking", "trucker", "semi", "18 wheeler", "haul", "highway", "diesel", "rig"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "firefighter": {
        "topics": ["firefighter", "fireman", "fire department", "rescue", "hose", "ladder", "blaze"],
        "competition": "medium",
        "avg_bsr": 32000,
    },
    "police": {
        "topics": ["police", "cop", "law enforcement", "badge", "patrol", "officer", "thin blue line"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "emt": {
        "topics": ["EMT", "paramedic", "ambulance", "first responder", "emergency", "medic"],
        "competition": "low",
        "avg_bsr": 55000,
    },
    "military": {
        "topics": ["military", "veteran", "army", "navy", "marine", "air force", "service", "deployed"],
        "competition": "medium",
        "avg_bsr": 25000,
    },
    "mechanic": {
        "topics": ["mechanic", "auto", "wrench", "garage", "car", "engine", "fix", "grease"],
        "competition": "medium",
        "avg_bsr": 38000,
    },
    "welder": {
        "topics": ["welder", "welding", "sparks", "metal", "fabricate", "arc", "TIG", "MIG"],
        "competition": "low",
        "avg_bsr": 48000,
    },
    "electrician": {
        "topics": ["electrician", "electrical", "wire", "voltage", "circuit", "power", "spark"],
        "competition": "low",
        "avg_bsr": 52000,
    },
    "plumber": {
        "topics": ["plumber", "plumbing", "pipes", "wrench", "drain", "fix", "water"],
        "competition": "low",
        "avg_bsr": 58000,
    },
    "carpenter": {
        "topics": ["carpenter", "woodworking", "build", "lumber", "saw", "craft", "hammer"],
        "competition": "low",
        "avg_bsr": 55000,
    },
    "farmer": {
        "topics": ["farmer", "farming", "farm", "tractor", "harvest", "crops", "agriculture", "barn"],
        "competition": "medium",
        "avg_bsr": 32000,
    },
    "chef": {
        "topics": ["chef", "cook", "kitchen", "culinary", "recipe", "gourmet", "foodie"],
        "competition": "medium",
        "avg_bsr": 40000,
    },
    "hairstylist": {
        "topics": ["hairstylist", "hairdresser", "salon", "scissors", "style", "beauty", "hair"],
        "competition": "low",
        "avg_bsr": 62000,
    },
    "realtor": {
        "topics": ["realtor", "real estate", "agent", "sold", "closing", "home", "property"],
        "competition": "low",
        "avg_bsr": 68000,
    },
    "lawyer": {
        "topics": ["lawyer", "attorney", "law", "court", "legal", "justice", "case"],
        "competition": "low",
        "avg_bsr": 75000,
    },
    "accountant": {
        "topics": ["accountant", "CPA", "tax", "numbers", "audit", "spreadsheet", "finance"],
        "competition": "low",
        "avg_bsr": 72000,
    },
    "engineer": {
        "topics": ["engineer", "engineering", "design", "build", "problem solve", "technical"],
        "competition": "low",
        "avg_bsr": 65000,
    },
    "programmer": {
        "topics": ["programmer", "developer", "coding", "code", "software", "debug", "compile", "stack overflow"],
        "competition": "medium",
        "avg_bsr": 42000,
    },
    "dispatcher": {
        "topics": ["dispatcher", "911", "dispatch", "radio", "emergency", "calls", "operator"],
        "competition": "low",
        "avg_bsr": 78000,
    },
    "librarian": {
        "topics": ["librarian", "library", "books", "reading", "shush", "catalog", "dewey"],
        "competition": "low",
        "avg_bsr": 82000,
    },
    "pilot": {
        "topics": ["pilot", "aviation", "fly", "cockpit", "altitude", "runway", "captain"],
        "competition": "low",
        "avg_bsr": 68000,
    },
    "dental": {
        "topics": ["dental", "dentist", "hygienist", "teeth", "smile", "floss", "cavity"],
        "competition": "low",
        "avg_bsr": 65000,
    },
    "pharmacy": {
        "topics": ["pharmacy", "pharmacist", "prescription", "pills", "medicine", "dispense"],
        "competition": "low",
        "avg_bsr": 72000,
    },

    # === FAMILY ===
    "mom": {
        "topics": ["mom", "mama", "mother", "mommy", "mom life", "motherhood", "supermom"],
        "competition": "high",
        "avg_bsr": 5000,
    },
    "dad": {
        "topics": ["dad", "father", "daddy", "papa", "dad life", "fatherhood", "dadhood"],
        "competition": "high",
        "avg_bsr": 8000,
    },
    "grandma": {
        "topics": ["grandma", "grandmother", "nana", "granny", "mimi", "gram", "grandkids"],
        "competition": "medium",
        "avg_bsr": 22000,
    },
    "grandpa": {
        "topics": ["grandpa", "grandfather", "papa", "gramps", "grandkids", "pop pop"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "parenting": {
        "topics": ["parenting", "parent", "kids", "toddler", "baby", "children", "raising"],
        "competition": "high",
        "avg_bsr": 15000,
    },
    "pregnancy": {
        "topics": ["pregnancy", "pregnant", "expecting", "baby bump", "maternity", "due date"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "twins": {
        "topics": ["twins", "twin mom", "twin dad", "double trouble", "twinning"],
        "competition": "low",
        "avg_bsr": 58000,
    },
    "aunt": {
        "topics": ["aunt", "auntie", "niece", "nephew", "cool aunt", "funcle"],
        "competition": "low",
        "avg_bsr": 48000,
    },
    "uncle": {
        "topics": ["uncle", "funcle", "niece", "nephew", "cool uncle"],
        "competition": "low",
        "avg_bsr": 52000,
    },
    "sister": {
        "topics": ["sister", "sis", "sibling", "sisters", "sisterhood"],
        "competition": "low",
        "avg_bsr": 55000,
    },
    "brother": {
        "topics": ["brother", "bro", "sibling", "brothers", "brotherhood"],
        "competition": "low",
        "avg_bsr": 58000,
    },

    # === HOBBIES & INTERESTS ===
    "gaming": {
        "topics": ["gaming", "gamer", "video games", "controller", "level up", "respawn", "GG", "noob"],
        "competition": "high",
        "avg_bsr": 15000,
    },
    "reading": {
        "topics": ["reading", "books", "bookworm", "bibliophile", "novel", "pages", "literature"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "cooking": {
        "topics": ["cooking", "cook", "kitchen", "recipe", "chef", "homemade", "from scratch"],
        "competition": "medium",
        "avg_bsr": 38000,
    },
    "baking": {
        "topics": ["baking", "baker", "cupcakes", "cookies", "bread", "oven", "dough"],
        "competition": "medium",
        "avg_bsr": 42000,
    },
    "gardening": {
        "topics": ["gardening", "garden", "plants", "flowers", "grow", "green thumb", "soil"],
        "competition": "medium",
        "avg_bsr": 32000,
    },
    "photography": {
        "topics": ["photography", "photographer", "camera", "photo", "capture", "lens", "shot"],
        "competition": "medium",
        "avg_bsr": 40000,
    },
    "painting": {
        "topics": ["painting", "artist", "art", "canvas", "brush", "create", "colors"],
        "competition": "medium",
        "avg_bsr": 45000,
    },
    "crafting": {
        "topics": ["crafting", "crafter", "DIY", "handmade", "create", "maker", "craft"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "knitting": {
        "topics": ["knitting", "knit", "yarn", "needles", "stitches", "knitter", "wool"],
        "competition": "low",
        "avg_bsr": 55000,
    },
    "crocheting": {
        "topics": ["crocheting", "crochet", "yarn", "hook", "stitches", "amigurumi"],
        "competition": "low",
        "avg_bsr": 52000,
    },
    "sewing": {
        "topics": ["sewing", "sew", "seamstress", "fabric", "thread", "pattern", "stitch"],
        "competition": "low",
        "avg_bsr": 58000,
    },
    "quilting": {
        "topics": ["quilting", "quilt", "quilter", "patchwork", "fabric", "blocks"],
        "competition": "low",
        "avg_bsr": 62000,
    },
    "woodworking": {
        "topics": ["woodworking", "woodworker", "wood", "saw", "build", "lumber", "workshop"],
        "competition": "low",
        "avg_bsr": 48000,
    },
    "pottery": {
        "topics": ["pottery", "ceramics", "clay", "wheel", "glaze", "kiln", "handmade"],
        "competition": "low",
        "avg_bsr": 72000,
    },
    "collecting": {
        "topics": ["collecting", "collector", "collection", "vintage", "rare", "antique"],
        "competition": "low",
        "avg_bsr": 68000,
    },
    "vinyl": {
        "topics": ["vinyl", "records", "turntable", "LP", "analog", "audiophile"],
        "competition": "low",
        "avg_bsr": 55000,
    },
    "birding": {
        "topics": ["birding", "bird watching", "birder", "ornithology", "binoculars", "species"],
        "competition": "low",
        "avg_bsr": 78000,
    },

    # === MUSIC ===
    "guitar": {
        "topics": ["guitar", "guitarist", "acoustic", "electric", "riff", "strings", "chord", "strum"],
        "competition": "medium",
        "avg_bsr": 38000,
    },
    "drums": {
        "topics": ["drums", "drummer", "beat", "sticks", "rhythm", "percussion", "kit"],
        "competition": "low",
        "avg_bsr": 52000,
    },
    "piano": {
        "topics": ["piano", "pianist", "keys", "classical", "melody", "play", "concert"],
        "competition": "low",
        "avg_bsr": 58000,
    },
    "bass": {
        "topics": ["bass", "bassist", "low end", "groove", "slap", "fretless"],
        "competition": "low",
        "avg_bsr": 68000,
    },
    "singing": {
        "topics": ["singing", "singer", "vocals", "voice", "choir", "karaoke", "harmonize"],
        "competition": "low",
        "avg_bsr": 65000,
    },
    "dj": {
        "topics": ["DJ", "turntable", "mix", "beats", "drop", "EDM", "rave"],
        "competition": "low",
        "avg_bsr": 72000,
    },
    "metal": {
        "topics": ["metal", "heavy metal", "headbang", "mosh", "thrash", "shred"],
        "competition": "low",
        "avg_bsr": 48000,
    },
    "country": {
        "topics": ["country", "country music", "nashville", "honky tonk", "twang", "boots"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "hiphop": {
        "topics": ["hip hop", "rap", "MC", "beats", "flow", "rhyme", "bars"],
        "competition": "medium",
        "avg_bsr": 42000,
    },

    # === LIFESTYLE ===
    "introvert": {
        "topics": ["introvert", "antisocial", "alone time", "homebody", "quiet", "solitude"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "sarcasm": {
        "topics": ["sarcasm", "sarcastic", "sass", "snark", "wit", "dry humor"],
        "competition": "high",
        "avg_bsr": 18000,
    },
    "anxiety": {
        "topics": ["anxiety", "anxious", "overthinking", "worry", "stress", "mental health"],
        "competition": "medium",
        "avg_bsr": 32000,
    },
    "truecrime": {
        "topics": ["true crime", "murder mystery", "podcast", "documentary", "serial killer", "case files"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "astrology": {
        "topics": ["astrology", "zodiac", "horoscope", "mercury retrograde", "birth chart", "stars"],
        "competition": "medium",
        "avg_bsr": 38000,
    },
    "tarot": {
        "topics": ["tarot", "tarot cards", "reading", "divination", "spiritual", "deck"],
        "competition": "low",
        "avg_bsr": 55000,
    },
    "witchy": {
        "topics": ["witch", "witchy", "magic", "spells", "coven", "occult", "wicca"],
        "competition": "medium",
        "avg_bsr": 42000,
    },
    "crystals": {
        "topics": ["crystals", "healing crystals", "energy", "amethyst", "quartz", "chakra"],
        "competition": "low",
        "avg_bsr": 58000,
    },
    "minimalist": {
        "topics": ["minimalist", "minimal", "simple", "less is more", "declutter", "essentialism"],
        "competition": "low",
        "avg_bsr": 62000,
    },
    "vegan": {
        "topics": ["vegan", "plant based", "cruelty free", "herbivore", "veganism", "no meat"],
        "competition": "medium",
        "avg_bsr": 45000,
    },
    "keto": {
        "topics": ["keto", "ketogenic", "low carb", "bacon", "fat adapted", "macros"],
        "competition": "low",
        "avg_bsr": 52000,
    },

    # === AGE/MILESTONES ===
    "retirement": {
        "topics": ["retired", "retirement", "retired life", "no alarm clock", "every day is saturday"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "vintage": {
        "topics": ["vintage", "classic", "retro", "oldschool", "throwback", "antique"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "birthday": {
        "topics": ["birthday", "bday", "celebrate", "party", "age", "another year"],
        "competition": "high",
        "avg_bsr": 15000,
    },

    # === FOOD ===
    "tacos": {
        "topics": ["tacos", "taco", "tuesday", "mexican", "salsa", "guac", "burrito"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "pizza": {
        "topics": ["pizza", "pepperoni", "slice", "pie", "cheesy", "italian"],
        "competition": "medium",
        "avg_bsr": 38000,
    },
    "bacon": {
        "topics": ["bacon", "crispy", "breakfast", "pork", "sizzle", "meat candy"],
        "competition": "medium",
        "avg_bsr": 42000,
    },
    "bbq": {
        "topics": ["BBQ", "barbecue", "grill", "smoke", "ribs", "brisket", "pitmaster"],
        "competition": "medium",
        "avg_bsr": 35000,
    },
    "sushi": {
        "topics": ["sushi", "sashimi", "roll", "wasabi", "chopsticks", "omakase"],
        "competition": "low",
        "avg_bsr": 55000,
    },
    "chocolate": {
        "topics": ["chocolate", "cocoa", "sweet", "dessert", "chocoholic", "dark chocolate"],
        "competition": "medium",
        "avg_bsr": 42000,
    },

    # === SEASONAL ===
    "christmas": {
        "topics": ["christmas", "xmas", "santa", "holiday", "festive", "jolly", "merry"],
        "competition": "high",
        "avg_bsr": 8000,
    },
    "halloween": {
        "topics": ["halloween", "spooky", "scary", "witch", "ghost", "pumpkin", "october"],
        "competition": "high",
        "avg_bsr": 10000,
    },
    "fall": {
        "topics": ["fall", "autumn", "pumpkin spice", "leaves", "cozy", "sweater weather"],
        "competition": "medium",
        "avg_bsr": 25000,
    },
    "summer": {
        "topics": ["summer", "beach", "sunshine", "vacation", "pool", "tan", "vibes"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "spring": {
        "topics": ["spring", "flowers", "bloom", "fresh", "renewal", "garden"],
        "competition": "low",
        "avg_bsr": 55000,
    },
    "winter": {
        "topics": ["winter", "snow", "cold", "cozy", "hot cocoa", "frost"],
        "competition": "medium",
        "avg_bsr": 32000,
    },

    # === LOCATION/LIFESTYLE ===
    "beach": {
        "topics": ["beach", "ocean", "sand", "waves", "coastal", "salt life", "shore"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "mountains": {
        "topics": ["mountains", "peaks", "alpine", "summit", "elevation", "highlands"],
        "competition": "medium",
        "avg_bsr": 32000,
    },
    "lake": {
        "topics": ["lake", "lake life", "lakeside", "cabin", "dock", "pontoon"],
        "competition": "low",
        "avg_bsr": 45000,
    },
    "texas": {
        "topics": ["Texas", "Texan", "lone star", "y'all", "howdy", "everything's bigger"],
        "competition": "medium",
        "avg_bsr": 28000,
    },
    "florida": {
        "topics": ["Florida", "sunshine state", "palm trees", "beach", "gator"],
        "competition": "medium",
        "avg_bsr": 32000,
    },
    "midwest": {
        "topics": ["midwest", "corn", "flyover", "heartland", "ope", "you betcha"],
        "competition": "low",
        "avg_bsr": 55000,
    },
}

# Generate TRENDING_TOPICS from all niche data
TRENDING_TOPICS = []
for niche_data in NICHE_DATA.values():
    TRENDING_TOPICS.extend(niche_data["topics"])
TRENDING_TOPICS = list(set(TRENDING_TOPICS))  # Remove duplicates

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

def get_niche_data(niche: str):
    """Get full niche data including topics, competition, and BSR."""
    return NICHE_DATA.get(niche.lower(), None)

def get_niche_topics(niche: str):
    """Get topics for a specific niche."""
    data = NICHE_DATA.get(niche.lower())
    return data["topics"] if data else []

def get_niche_competition(niche: str):
    """Get competition level for a niche (low, medium, high)."""
    data = NICHE_DATA.get(niche.lower())
    return data["competition"] if data else "unknown"

def get_niche_bsr(niche: str):
    """Get average BSR for a niche."""
    data = NICHE_DATA.get(niche.lower())
    return data["avg_bsr"] if data else None

def get_all_niches():
    """Get list of all available niches."""
    return list(NICHE_DATA.keys())

def get_niches_by_competition(competition: str):
    """Get niches filtered by competition level."""
    return [
        niche for niche, data in NICHE_DATA.items()
        if data["competition"] == competition.lower()
    ]

def get_low_competition_niches():
    """Get all low competition niches (gold mines!)."""
    return get_niches_by_competition("low")
